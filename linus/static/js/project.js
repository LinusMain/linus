/* Project specific Javascript goes here. */

is_sharena_wav_has_been_played_and_user_is_completely_happy = false

playSharenaWav = function () {
  $('body').on('click', function () {
    if (!is_sharena_wav_has_been_played_and_user_is_completely_happy) {
      is_sharena_wav_has_been_played_and_user_is_completely_happy = true
      if (Math.random() < 0.01) {
        var sharenas = [
          'sharena.wav',
          'sharena2.wav',
          'sharena3.wav',
          'sharena4.wav',
          'sharena5.wav',
          'sharena6.wav',
          'sharena7.wav',
          'sharena8.wav',
          'sharena9.wav',
          'sharena10.wav',
          'sharena11.wav',
          'sharena12.wav',
        ]
        // if (Math.random() < 0.01) {
        var to_play = sharenas[Math.floor(Math.random() * sharenas.length)];
        var audio = new Audio('/static/other/' + to_play);
        audio.play();
        // }
      }
    }
  });
}
