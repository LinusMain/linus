import datetime
import os
import pickle
import re
import urllib.parse
import warnings

import pytz
from w3lib.html import replace_entities
from .poroclasses import Skill, Refine, Seal, Hero, SkillReq, Availability

def removeEmptyStrings(arr):
    return [a for a in arr if not a == ""]

def parseRawSkill(rawSkill):
    s = Skill()
    s.name = rawSkill['Name']
    s.wikiName = rawSkill['WikiName']
    s.isRefine = not '' == rawSkill['RefinePath']
    s.refineType = rawSkill['RefinePath']
    s.isPrf = '1' == rawSkill['Exclusive'] and not s.isRefine
    s.cost = tryStrToInt(rawSkill['SP'])
    s.range = tryStrToInt(rawSkill['UseRange'])
    # TODO: prettify it later
    s.desc = replace_entities(rawSkill['Description'].replace("&lt;br&gt;", "\n"))
    s.slot = rawSkill['Scategory']   
    if s.slot == "sacredseal":
        s.isSeal = True 
    s.cd = tryStrToInt(rawSkill['Cooldown'])
    s.page = rawSkill['Page']
    s.url = "https://feheroes.gamepedia.com/" + urllib.parse.quote(s.page)
    # split because Aether <= Sol,Luna
    s.required = re.split("\\s*,\\s*", rawSkill['Required'])
    s.required = removeEmptyStrings(s.required)
    s.next = re.split("\\s*,\\s*", rawSkill['Next'])
    s.next = removeEmptyStrings(s.next)
    s.movePerms = re.split("\\s*,\\s*", rawSkill['CanUseMove'])
    s.movePerms = removeEmptyStrings(s.movePerms)
    s.weaponPerms = re.split("\\s*,\\s*", rawSkill['CanUseWeapon'])
    s.weaponPerms = removeEmptyStrings(s.weaponPerms)
    s.properties = re.split("\\s*,\\s*", rawSkill['Properties'])
    s.properties = removeEmptyStrings(s.properties)
    s.isEnemyOnly = "enemy_only" in s.properties
    s.stats = rawSkill['StatModifiers']
    return s

def parseRawUpgrade(rawUpgrade, allSkills):
    baseWeapKey = rawUpgrade['BaseWeapon']
    intoWeapKey = rawUpgrade['UpgradesInto']
    r = Refine()
    baseWeap = allSkills[baseWeapKey]
    intoWeap = allSkills[intoWeapKey]
    r.skill = intoWeap
    r.refineType = intoWeap.refineType
    r.statChange = rawUpgrade['StatModifiers']
    r.desc = replace_entities(rawUpgrade['AddedDesc'].replace("&lt;br&gt;", "\n"))
    intoWeap.baseWeap = baseWeap
    baseWeap.refines.append(r)
    return r

def parseRawEvolution(rawEvolution, allSkills):
    baseWeapKey = rawEvolution['BaseWeapon']
    intoWeapKey = rawEvolution['EvolvesInto']    
    baseWeap = allSkills[baseWeapKey]
    intoWeap = allSkills[intoWeapKey]
    baseWeap.evolutions.append(intoWeap)

def parseRawSeal(rawSeal, allSkills):
    skillName = rawSeal['Skill']
    # unfortunately we have to search the names
    # since wikiName is not stored on page
    found = False
    seal = Seal()
    for skill in allSkills.values():
        if found:
            break
        if skill.name == skillName:
            skill.isSeal = True
            seal.skill = skill
            seal.badgeColor = rawSeal['BadgeColor']
            seal.badgeCost = tryStrToInt(rawSeal['BadgeCost'])
            seal.greatbadgeCost = tryStrToInt(rawSeal['GreatBadgeCost'])
            seal.coinCost = tryStrToInt(rawSeal['SacredCoinCost'])
            found = True
    if not found:
        warnings.warn("no seal: " + rawSeal)
        return None
    return seal

def parseRawUnit(rawUnit):
    h = Hero()
    h.name = rawUnit['Name']
    h.mod = rawUnit['Title'].replace('&quot;', '"')
    h.full_name = h.name + ":" + h.mod
    h.wikiName = rawUnit['WikiName']
    h.page = rawUnit['Page']
    h.pageID = rawUnit['PageID']
    h.url = "https://feheroes.gamepedia.com/" + urllib.parse.quote(h.page)
    h.origin = rawUnit['Origin']
    h.releaseDate = rawUnit['ReleaseDate']
    h.desc = replace_entities(rawUnit['Description'].replace("&lt;br&gt;", "\n"))
    h.weapon = rawUnit['WeaponType']
    h.gender = rawUnit['Gender']
    h.artist = rawUnit['Artist']
    h.move = rawUnit['MoveType']
    h.color = h.weapon.split(" ")[0]
    properties = re.split("\\s*,\\s*", rawUnit['Properties'])
    properties = removeEmptyStrings(properties)
    h.properties = properties
    if "refresher" in properties:
        h.isDancer = True 
    if "tempest" in properties:
        h.heroSrc = "TT"
        h.rarities = [4,5]
    elif "ghb" in properties:
        h.heroSrc = "GHB"
        h.rarities = [3,4]
    elif "duo" in properties:
        h.heroSrc = "Duo"
    elif "legendary" in properties:
        h.heroSrc = "Legendary"
    elif "mythic" in properties:
        h.heroSrc = "Mythic"
    elif "story" in properties:
        h.heroSrc = "Story"
    # will get overwritten by duo/leg/mythic
    # if for some reason theres an inconsistency
    # in the properties
    elif "special" in h.properties:
        h.heroSrc = "Special"
    else:
        h.heroSrc = "Normal"         
    return h 

def parseRawUnitStat(rawUnitStat, allUnits):
    # print(rawUnitStat)
    heroKey = rawUnitStat['WikiName']
    # because some elements in the table might be borken
    if not heroKey in allUnits:
        heroKey = heroKey + " ENEMY"
    h = allUnits[heroKey]
    stats = ['HP', 'Atk', 'Spd', 'Def', 'Res']
    # convert middle stat to bane/neut/boon
    lvl1BB = lambda x : (x-1,x,x+1)
    # black magic fuckery, smurt
    lvl15Stats = [
        lvl1BB(tryStrToInt(rawUnitStat['Lv1%s5'%(stat)])) for stat in stats
    ] 
    h.lvl_1_Stats[4] = lvl15Stats
    h.lvl_1_Stats[2] = [lvl1BB(v[1]-1) for v in h.lvl_1_Stats[4]]
    h.lvl_1_Stats[0] = [lvl1BB(v[1]-2) for v in h.lvl_1_Stats[4]]

    # to find the biggest nonhp stats
    sd = {}
    for i in range(1,5):
        sd[100*lvl15Stats[i][1] - i] = i
    ssd = sorted(sd)
    bigStat1, bigStat2 = sd[ssd.pop()], sd[ssd.pop()]
    # copy the lower array first
    h.lvl_1_Stats[1] = [lvl1BB(v[1]) for v in h.lvl_1_Stats[0]]
    h.lvl_1_Stats[3] = [lvl1BB(v[1]) for v in h.lvl_1_Stats[2]]
    # then increase the two biggest non hp stats
    h.lvl_1_Stats[1][bigStat1] = lvl1BB(h.lvl_1_Stats[1][bigStat1][1] + 1)
    h.lvl_1_Stats[1][bigStat2] = lvl1BB(h.lvl_1_Stats[1][bigStat2][1] + 1)
    h.lvl_1_Stats[3][bigStat1] = lvl1BB(h.lvl_1_Stats[3][bigStat1][1] + 1)
    h.lvl_1_Stats[3][bigStat2] = lvl1BB(h.lvl_1_Stats[3][bigStat2][1] + 1)

    gr3 = [tryStrToInt(rawUnitStat['%sGR3'%(stat)]) for stat in stats]
    # rarity, growth rate
    rgr3ToGV = lambda r, gr3 : int(0.39 * int(gr3 * (0.79 + 0.07 * r)))
    for star in range(1,6):
        # calc the growth rates and collect baneboon info as we go
        hasBane = False
        numBanes = 0
        hasBoon = False
        numBoons = 0
        totalStat = 0
        for stat in range(5):
            grneut = gr3[stat]
            neutStat = rgr3ToGV(star,grneut) + h.lvl_1_Stats[star-1][stat][1]
            baneStat = rgr3ToGV(star,grneut-5) + h.lvl_1_Stats[star-1][stat][0]
            boonStat = rgr3ToGV(star,grneut+5) + h.lvl_1_Stats[star-1][stat][2]
            h.lvl_40_Stats[star-1][stat] = (baneStat, neutStat, boonStat)
            totalStat += neutStat
            if (neutStat-baneStat) > (boonStat-neutStat):
                hasBane = True
                numBanes += 1
            elif (boonStat-neutStat) > (neutStat-baneStat):
                hasBoon = True
                numBoons += 1
        if hasBane and not (numBoons == 4):
            totalBane = totalStat - 1
        else:
            totalBane = totalStat
        if hasBoon and not (numBanes == 4):
            totalBoon = totalStat + 1
        else:
            totalBoon = totalStat 
        # finalize the totals
        h.lvl_40_Stats[star-1][5] = (totalBane, totalStat, totalBoon)    

    # fill in the last entry with total bst
    h.statArray = [t[1] for t in h.lvl_40_Stats[4]]

    # print(h)
    # [print(s) for s in h.lvl_1_Stats]
    # [print(s) for s in h.lvl_40_Stats]
    # print(h.statArray)

    return

def parseRawUnitSkill(rawUnitSkill, allSkills, allUnits):
    heroKey = rawUnitSkill['WikiName']
    skillKey = rawUnitSkill['skill']   
    # because some elements in the table might be borken
    if not heroKey in allUnits:
        heroKey = heroKey + " ENEMY"
    if not heroKey in allUnits:
        warnings.warn(rawUnitSkill['WikiName'] + " is not in allUnits yet")
    if not skillKey in allSkills:
        warnings.warn(skillKey + " is not in allSkills yet")
        return
    h = allUnits[heroKey]
    s = allSkills[skillKey]
    sr = SkillReq()
    sr.skill = s
    sr.slot = s.slot
    sr.defaultRarity = tryStrToInt(rawUnitSkill['defaultRarity'])
    sr.unlockRarity = tryStrToInt(rawUnitSkill['unlockRarity'])
    # print(h,sr)
    h.skillReqs.append(sr)
    return 


def parseRawLeg(rawLegHero, allUnitPages):
    page = rawLegHero['Page']
    if not page in allUnitPages:
        page = page.encode('raw_unicode_escape').decode()
        if not page in allUnitPages:
            warnings.warn(
                page + " is not in unit pages, and unicode escape failed"
            )
            return
    hero = allUnitPages[page]
    hero.heroSrc = "Legendary"
    hero.duel = rawLegHero['Duel']
    hero.season = rawLegHero['LegendaryEffect']
    return

def parseRawDuo(rawDuoHero, allUnitPages):
    page = rawDuoHero['Page']
    if not page in allUnitPages:
        page = page.encode('raw_unicode_escape').decode()
        if not page in allUnitPages:
            warnings.warn(
                page + " is not in unit pages, and unicode escape failed"
            )
            return
    hero = allUnitPages[page]
    hero.heroSrc = "Duo"
    hero.duoSkill = rawDuoHero['DuoSkill']
    hero.duel = rawDuoHero['Duel']
    return

def parseRawMythic(rawMythicHero, allUnitPages):
    page = rawMythicHero['Page']
    if not page in allUnitPages:
        page = page.encode('raw_unicode_escape').decode()
        if not page in allUnitPages:
            warnings.warn(
                page + " is not in unit pages, and unicode escape failed"
            )
            return
    hero = allUnitPages[page]
    hero.heroSrc = "Mythic"
    hero.season = rawMythicHero['MythicEffect']
    return

def parseRawHarmonized(rawHarmonizedHero, allUnitPages):
    page = rawHarmonizedHero['Page']
    if not page in allUnitPages:
        page = page.encode('raw_unicode_escape').decode()
        if not page in allUnitPages:
            warnings.warn(
                page + " is not in unit pages, and unicode escape failed"
            )
            return
    hero = allUnitPages[page]
    hero.heroSrc = "Harmonized"
    hero.harmonizedSkill = rawMythicHero['HarmonizedSkill']
    return

def parseRawFocus(rawFocus, allUnits):
    heroKey = rawFocus['Unit']
    if not heroKey in allUnits:
        warnings.warn(heroKey + " not in units")
        return
    hero = allUnits[heroKey]
    rarity = tryStrToInt(rawFocus['Rarity'])
    if not rarity in hero.rarities:
        hero.rarities.append(rarity)
    return

def parseRawAvailability(rawHeroAvail, allUnitPages, timeNow):
    # print(rawHeroAvail)
    page = rawHeroAvail['Page']
    if not page in allUnitPages:
        page = page.encode('raw_unicode_escape').decode()
        if not page in allUnitPages:
            warnings.warn(
                page + " is not in unit pages, and unicode escape failed"
            )
            return
    hero = allUnitPages[page]
    rarity = tryStrToInt(rawHeroAvail['Rarity'])       
    startStr = rawHeroAvail['StartTime']
    startTime = datetime.datetime.strptime(startStr, "%Y-%m-%d %H:%M:%S")
    startTime = pytz.utc.localize(startTime) 
    endStr = rawHeroAvail['EndTime']
    endTime = datetime.datetime.strptime(endStr, "%Y-%m-%d %H:%M:%S") 
    endTime = pytz.utc.localize(endTime)
    avail = Availability()
    avail.rarity = rarity
    avail.startTime = startTime
    avail.endTime = endTime
    # HACK: zero out the hero rarities
    # if theres available hero info
    if hero.avails == []:
        hero.rarities = []
    hero.avails.append(avail)
    if (startTime < timeNow and timeNow < endTime):
        hero.rarities.append(rarity)
    # print(hero, rarity, startTime, "to", endTime)
    return

def finalizeUnitSkills(unit): 
    # print(unit, unit.skillReqs)
    for sr in unit.skillReqs:
        if sr.slot == "weapon":
            weap = sr.skill
            for evo in weap.evolutions:
                evoSR = SkillReq()
                evoSR.skill = evo
                evoSR.slot = "weapon"
                evoSR.defaultRarity = sr.defaultRarity
                evoSR.unlockRarity = sr.unlockRarity
                # for-iterator will visit this newly
                # appended item because python;
                # this is desirable in case 
                # evolved weaps can evolve again
                unit.skillReqs.append(evoSR)
            if sr.unlockRarity == 5:
                #print(sr)
                sr.isMax = True
    slots = ["special", "assist", "passivea", "passiveb", "passivec"]
    for slot in slots:
        slotsrs = [slotsr for slotsr in unit.skillReqs if slotsr.slot == slot] 
        if slotsrs == []:
            continue
        # print(slotsrs)
        maxRarity = max([slotsr.unlockRarity for slotsr in slotsrs])
        for slotsr in slotsrs:
            if slotsr.unlockRarity == maxRarity:
                slotsr.isMax = True

def tryStrToInt(intStr):
    if re.match("(-|)[0-9]+", intStr):
        return int(intStr)
    elif intStr == "" or intStr == None:
        return 0
    else:
        warnings.warn("Bad intStr submitted to tryStrToInt", stacklevel=2)     
        return 0

def LoadPoro(pkl_output_file = 'poro.pkl'):
    with open(pkl_output_file + ".0", 'rb') as f:
        up = pickle.Unpickler(f)    
        rawSkills = up.load()
        rawUpgrades = up.load()
        rawEvolutions = up.load()        
        rawUnitStats = up.load()
    with open(pkl_output_file + ".1", 'rb') as f:
        up = pickle.Unpickler(f)  
        rawUnitSkills = up.load()
    with open(pkl_output_file + ".2", 'rb') as f:
        up = pickle.Unpickler(f) 
        rawUnits = up.load()
        rawSeals = up.load()
        rawLegHeroes = up.load()
        rawDuoHeroes = up.load()
        rawMythicHeroes = up.load()
        rawHarmonizedHeroes = up.load()
        rawSummonFocusUnits = up.load()
        rawHeroAvails = up.load()

    # dual maps for WikiName/Page
    allSkills = {}
    allSkillPages = {}
    allUnits = {}
    allUnitPages = {}
    allSeals = {}

    timeNow = datetime.datetime.now(datetime.timezone.utc)
    print("Began parsing at", timeNow)
    for wikiName in rawSkills:
        rawSkill = rawSkills[wikiName]
        skill = parseRawSkill(rawSkill)
        allSkills[wikiName] = skill
        allSkillPages[skill.page] = skill

    for wikiName in rawUpgrades:
        rawUpgrade = rawUpgrades[wikiName]
        parseRawUpgrade(rawUpgrade, allSkills)

    for wikiName1 in rawEvolutions:
        weapEvos = rawEvolutions[wikiName1]
        for wikiName2 in weapEvos:
            rawEvolution = weapEvos[wikiName2]
            parseRawEvolution(rawEvolution, allSkills)

    # allSeals 
    for skillkey in rawSeals:
        rawSeal = rawSeals[skillkey]
        seal = parseRawSeal(rawSeal, allSkills)
        if seal != None:
            allSeals[skillkey] = seal

    #isMax for seals
    sealReqs = set()
    for skillkey in allSeals:
        seal = allSeals[skillkey]
        skill = seal.skill
        if not skill.name == skillkey:
            warnings.warn(skillkey + " seal bug :linusderp: ")
            continue
        for skillname in skill.required:
            sealReqs.add(skillname)
    if "" in sealReqs:
        sealReqs.remove("")

    for skillkey in allSeals:
        seal = allSeals[skillkey]
        skill = seal.skill
        if not skill.name == skillkey:
            warnings.warn(skillkey + " seal bug :linusderp: ")
            continue
        if skill.wikiName in sealReqs:
            seal.isMax = False
        else: 
            seal.isMax = True

    for wikiName in rawUnits:
        rawUnit = rawUnits[wikiName]
        unit = parseRawUnit(rawUnit)
        allUnits[wikiName] = unit
        page = unit.page
        if not ("enemy" in unit.properties or page in allUnitPages):
            allUnitPages[page] = unit
    for wikiName in rawUnitStats:
        rawUnitStat = rawUnitStats[wikiName]
        parseRawUnitStat(rawUnitStat, allUnits)
    for wikiName1 in rawUnitSkills:
        unitSkills = rawUnitSkills[wikiName1]
        for wikiName2 in unitSkills:
            rawUnitSkill = unitSkills[wikiName2]
            parseRawUnitSkill(rawUnitSkill, allSkills, allUnits)

    # skillReqs have been defined by parseRawUnitSkill
    # now do post processing to mark final skills
    # e.g. Fury 3 on Hinata
    # and to add evolutions 
    # e.g. Tobin armorsmasher
    for unitkey in allUnits:
        unit = allUnits[unitkey]
        finalizeUnitSkills(unit) 

    # we can use properties but just in case they fucked up
    for wikipage in rawLegHeroes:
        rawLegHero = rawLegHeroes[wikipage]
        parseRawLeg(rawLegHero, allUnitPages)
    for wikipage in rawDuoHeroes:
        rawDuoHero = rawDuoHeroes[wikipage]
        parseRawDuo(rawDuoHero, allUnitPages)
    for wikipage in rawMythicHeroes:
        rawMythicHero = rawMythicHeroes[wikipage]
        parseRawMythic(rawMythicHero, allUnitPages)
    for wikipage in rawHarmonizedHeroes:
        rawHarmonizedHero = rawHarmonizedHeroes[wikipage]
        parseRawHarmonized(rawHarmonizedHero, allUnitPages)        
    # focus rarities first
    for rid in rawSummonFocusUnits:
        rawFocus = rawSummonFocusUnits[rid]
        parseRawFocus(rawFocus, allUnits)
    # switch to availability table for those that
    # were demoted like Reyson
    for rid in rawHeroAvails:
        rawHeroAvail = rawHeroAvails[rid]
        parseRawAvailability(rawHeroAvail, allUnitPages, timeNow)

    # finalize prf perms by checking which units have them
    # could be faster if we put it into the body of 
    # the skillReq parser but let's keep it (relatively)
    # sane over here and do it at the end
    prfs = [s for s in allSkills.values() if s.isPrf]
    # clear the garbage
    for prf in prfs:
        prf.weaponPerms = []
        prf.movePerms = []
    for unit in allUnits.values():
        wp = unit.weapon
        mp = unit.move
        for prf in unit.getPrfs():
            if not wp in prf.weaponPerms:
                prf.weaponPerms.append(wp)
            if not mp in prf.movePerms:
                prf.movePerms.append(mp)
    
    # returning lists smh leenis so degenerate :alfonsewat:
    return dict(
        skills=list(allSkills.values()),
        heroes=list(allUnits.values()),
        seals =list(allSeals.values()))

# to test image curling
def saveDB(pkl_output_file = 'porodb.pkl'):
    with open(pkl_output_file, 'wb') as f:
        p = pickle.Pickler(f)
        p.dump(LoadPoro())
