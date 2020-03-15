# Written by /u/Pororo#5569 (13 March 2020)

# pip install them and stuff
import urllib.parse
import unidecode
import sys, getopt
from operator import itemgetter

STAT_HP = 0
STAT_ATK = 1
STAT_SPD = 2
STAT_DEF = 3
STAT_RES = 4

def getStatString(stat):
    if stat < 0 or stat > 5:
        return None
    else:
        return ["HP", "ATK", "SPD", "DEF", "RES"][stat]

heroList = []
heroDict = {}

# to allow SQL like selection 
attributes = {
   
    "name":         (lambda hero: hero.heroName + ":" + hero.heroMod),
    "source":       (lambda hero: hero.heroSrc),
    "f2pstatus":    (lambda hero: "grail" if hero.isGrail() else "f2p" if hero.isF2P() else "p2w"),
    "move":         (lambda hero: hero.move),
    "weapon":       (lambda hero: hero.weapon),
    "color":        (lambda hero: hero.color),
    "weaponType":   (lambda hero: hero.getWeaponString()),
    "hp":           (lambda hero: hero.getStat(STAT_HP)),
    "atk":          (lambda hero: hero.getStat(STAT_ATK)),
    "spd":          (lambda hero: hero.getStat(STAT_SPD)),
    "def":          (lambda hero: hero.getStat(STAT_DEF)),
    "res":          (lambda hero: hero.getStat(STAT_RES)),
    "bst":          (lambda hero: hero.getBST()),
    "bstBin":       (lambda hero: hero.getAdjustedBST()//5 * 5)
}

# printAttributes(heroList, ["name", "source"])
# is akin to Select NAME, SOURCE from HEROES
def printAttributes(heroes, attrs):
    #shift name to the end
    while ("name" in attrs):
        attrs.remove("name")
    attrs.append("name")
    maxLengthMap = {}
    for attr in attrs:
        if not attr in attributes:
            print("%s is not in defined attributes"%attr)
            continue
        maxLength = 0
        for hero in heroes:
            lenres = len(str(attributes[attr](hero)))
            maxLength = max(maxLength, lenres)
        maxLengthMap[attr] = maxLength
        # print(attr + " " + str(maxLength))
    for hero in heroes:
        heroEntry = ""
        for attr in attrs:
            printLength = maxLengthMap[attr] + 2
            res = str(attributes[attr](hero)).ljust(printLength)
            heroEntry += res
        print(heroEntry)

def sortedPrint(heroes, attrs, rev=False):
    #shift name to the end
    while ("name" in attrs):
        attrs.remove("name")
    attrs.append("name")
    maxLengthMap = {}
    printList = []
    for attr in attrs:
        if not attr in attributes:
            print("%s is not in defined attributes"%attr)
            continue
        maxLength = 0
        for hero in heroes:
            lenres = len(str(attributes[attr](hero)))
            maxLength = max(maxLength, lenres)
        maxLengthMap[attr] = maxLength
        # print(attr + " " + str(maxLength))
    for hero in heroes:
        heroEntry = ""
        for attr in attrs:
            printLength = maxLengthMap[attr] + 2
            res = str(attributes[attr](hero)).ljust(printLength)
            heroEntry += res
        printList.append(heroEntry) 
    printList = sorted(printList, reverse=rev)
    for entry in printList:
        print(entry)   

class Hero:
    def __init__(
        self, 
        heroName,
        heroMod 
    ):
        self.heroName = heroName
        self.heroMod = heroMod
        self.heroSrc = "Normal"
        self.hero3Star = False
        self.hero4Star = False
        self.hero5Star = False
        self.move = ""
        self.weapon = ""
        self.color = ""
        self.releaseDate = "" 
        self.statArrayBane = []
        self.statArrayNeut = []
        self.statArrayBoon = []
        self.statArray = []    
    
    def __str__(self):
        return "%s:%s"%(self.heroName, self.heroMod)
    
    def __repr__(self):
        return "%s:%s"%(self.heroName, self.heroMod)        
    
    def getStatTuple(self, stat, stars = 5, isLvl40 = True):
        rowNum = stat + 5 * (stars-1)
        if (isLvl40):
            rowNum += 25
        return self.statArray[rowNum]

    # 0 = bane, 2 = boon
    def getStat(self, stat, bane_neut_boon=1, stars=5, isLvl40 = True):
        return self.getStatTuple(stat, stars, isLvl40)[bane_neut_boon]

    def getBSTRange(self, stars=5, isLvl40 = True):
        rows = (list(divide_chunks(self.statArray,5)))
        if (isLvl40):
            rowIndex = stars + 4
        else:
            rowIndex = stars - 1
        row = rows[rowIndex]
        biggestBane = 0
        biggestBoon = 0
        bstNeut = 0
        for chunk in row:
            if (chunk[1] - chunk[0] > biggestBane):
                biggestBane = chunk[1] - chunk[0]
            if (chunk[2] - chunk[1] > biggestBoon):
                biggestBoon = chunk[2] - chunk[1]
            bstNeut += chunk[1]
        if (self.isGrail() or self.heroSrc == "Story"):
            return (bstNeut, bstNeut, bstNeut)            
        bstMin = bstNeut - max(0, biggestBane - biggestBoon)
        bstMax = bstNeut + max(0, biggestBoon - biggestBane)
        return (bstMin, bstNeut, bstMax)

    def getBST(self, bane_neut_boon = 1, stars=5, isLvl40 = True):
        return self.getBSTRange(stars, isLvl40)[bane_neut_boon]

    def printStats(self):
        rows = (list(divide_chunks(self.statArray,5)))
        print(rows[9])

    def printInfo(self):
        print("Unit Data for %s:%s"%(self.heroName, self.heroMod))
        print("Unit release date: %s "%(self.releaseDate))
        print("3-5 Star Pullable: [%s, %s, %s]"%(self.hero3Star, self.hero4Star, self.hero5Star))
        print("Source: %s"%self.heroSrc)
        print("move: %s"%self.move)
        print("Color: %s"%self.color)
        print("weapon: %s"%self.weapon)
        rows = (list(divide_chunks(self.statArray,5)))
        rowNumber = 0
        for row in rows:                
            lvl_1_Stat = (rowNumber < 5)
            lvl_40_Stat = (rowNumber >= 5)
            rarityLevel = (rowNumber % 5)                
            rowNumber += 1                
            biggestBane = 0
            biggestBoon = 0
            bstNeut = 0
            for chunk in row:
                if (chunk[1] - chunk[0] > biggestBane):
                    biggestBane = chunk[1] - chunk[0]
                if (chunk[2] - chunk[1] > biggestBoon):
                    biggestBoon = chunk[2] - chunk[1]
                bstNeut += chunk[1]            
            bstMin = bstNeut + max(0, biggestBane - biggestBoon)
            bstMax = bstNeut + max(0, biggestBoon - biggestBane)
            bstStr = str(row).ljust(70, " ")
            if (bstMin == bstMax):
                print("%s BST : %s" %(bstStr, bstNeut))
            else:
                print("%s BST : %s-%s" %(row, bstMin, bstMax))
        print("")

    def getPullableRarities(self):
        ret = []
        if self.hero3Star:
            ret.append(3)
        if self.hero4Star:
            ret.append(4)
        if self.hero5Star:
            ret.append(5)
        return ret

    def isF2P(self):
        rarities = self.getPullableRarities()
        return 3 in rarities or 4 in rarities

    def isGrail(self):
        src = self.heroSrc
        if (src == "GHB" or src == "TT"):
            return True
        return False

    def getStatOrder(self):
        statTuples = [(stat, (5 - stat) + 100 * self.getStat(stat, isLvl40 = False)) for stat in range(5)]
        sortedTuples = sorted(statTuples, key=itemgetter(1), reverse=True)
        return [sortedTuple[0] for sortedTuple in sortedTuples]

    def getStatOrderString(self):
        return [self.getStatString(stat) for stat in self.getStatOrder()]

    def getColor(self):
        return self.color

    def isRed(self):
        return self.getColor() == "Red"
    def isBlue(self):
        return self.getColor() == "Blue"
    def isGreen(self):
        return self.getColor() == "Green"
    def isColourless(self):
        return self.getColor() == "Colourless"

    def getWeaponString(self):
        weap = self.weapon
        if weap == "Sword" or weap == "Axe" or weap == "Lance":
            return weap
        else:
            return self.color + " " + weap

    def getAdjustedBST(self):
        return self.getBST() + 3

    def printArenaInfo(self):
        if self.isGrail():
            availStr = "GRAIL"
        elif self.isF2P():
            availStr = "F2P"
        else:
            availStr = "ORBS"
        print((self.getAdjustedBST()//5) * 5, availStr.ljust(10), self.weapon.ljust(18), self.move.ljust(10), self)

def sortByFoo(heroes, foo, bigToSmall=False):
    heroBST = [(hero, foo(hero)) for hero in heroes]
    heroBST = sorted(heroBST, key=itemgetter(1), reverse=bigToSmall)
    return [tup[0] for tup in heroBST]   

def sortByBst(heroes, bigToSmall=False):
    heroBST = [(hero, hero.getBST()) for hero in heroes]
    heroBST = sorted(heroBST, key=itemgetter(1), reverse=bigToSmall)
    return [tup[0] for tup in heroBST]

def readHeroFile(filepath):
    inputfile = open(filepath, 'r')
    if (inputfile == None):
        return
    heroes = []
    while True:
        hero = digestHero(inputfile)        
        if not hero:
            break;
        heroes.append(hero)
    return heroes



def urlStrip(inStr):
    return unidecode.unidecode(urllib.parse.unquote(inStr))

def divide_chunks(l, n):       
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


# heroName          Linus
# heroMod           Mad Dog
# heroSrc           GHB
# move          Infantry
# weapon        Axe
# releaseDate       2018-06-12
# hero{3,4,5}Star   Pullable rarities
# statArray contains 50 tuples 
# corresponding to (LVL1_1star, LVL1_2star...LVL40_4star, LVL40_5star)
#  statArrayBane, statArrayNeut and statArrayBoon
#   contain respectively the corresponding (0th/1st/2nd)
#   elements of the tuples
def digestHero(inputfile):
    while(True):
        line = inputfile.readline()
        if not line:
            return None
        line = line.rstrip()
        if ":" in line:
            heroName = urlStrip(line.split(":")[0])
            heroMod = urlStrip(line.split(":_")[1]).replace("_", " ")
            hero = Hero(heroName, heroMod)
        elif line.endswith("_Heroes"):
            hero.heroSrc = line.rsplit("_Heroes")[0]
        elif "Grand_Hero_Battle" == line:
            hero.heroSrc = "GHB"
        elif "Tempest_Trials" == line:
            hero.heroSrc = "TT"
        elif "Rarity_3" == line:
            hero.hero3Star = True
        elif "Rarity_4" == line:
            hero.hero4Star = True
        elif "Rarity_5" == line:
            hero.hero5Star = True
        elif "Infantry" == line:
            hero.move = line
        elif "Cavalry" == line:
            hero.move = line
        elif "Armor" == line:
            hero.move = line
        elif "Flying" == line:
            hero.move = line
        elif line.endswith("Beast") or line.endswith("Tome") or line.endswith("bow") or line.endswith("Sword") or line.endswith("Lance") or line.endswith("Axe") or line.endswith("Dagger") or line.endswith("Breath") or line.endswith("Staff"):
            # because not capitalizing bow is stupid
            wt = line.replace("bow", "Bow").replace("_", " ")
            if (wt.startswith("Red") or wt == "Sword"):
                color = "Red"
                wt = wt.rsplit("Red ")[-1]
            elif (wt.startswith("Blue") or wt == "Lance"):
                color = "Blue"
                wt = wt.rsplit("Blue ")[-1]
            elif (wt.startswith("Green") or wt == "Axe"):
                color = "Green"
                wt = wt.rsplit("Green ")[-1]
            else:
                color = "Colorless"
                wt = wt.rsplit("Colorless ")[-1]                
            hero.weapon = wt
            hero.color = color 
        elif line.count("/") == 2:
            [bane, neut, boon] = line.split("/")
            hero.statArrayBane.append(int(bane))
            hero.statArrayNeut.append(int(neut))
            hero.statArrayBoon.append(int(boon))
            hero.statArray.append((int(bane),int(neut),int(boon)))
        elif line.startswith("datetime"):
            hero.releaseDate = line.split("datetime=")[1]
            heroList.append(hero)
            if (heroDict.get(hero.heroName)):
                heroDict[hero.heroName].append(hero)
            else:
                heroDict[hero.heroName] = [hero]
            #hero.printInfo()
            return hero  
    return digestHero(inputfile)

#readHeroFile("heroes_parsed.txt")
