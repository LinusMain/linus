$(document).ready(function () {
  tippy.delegate('body', {
    target: '[data-tippy-content]'
  });

  $(document).on('input', 'input[type="search"]', function () {
    /**
     * @type {string}
     */
    const value = $(this).val().toLowerCase();
    const wavs = {
      'nino': 'sonia.wav',
      'abi': 'sonia.wav',
      'priestess': 'sonia.wav',
      'sonia': 'sonia.wav',
      'hector': 'hector.wav',
      'bector': 'hector.wav',
      'sharena': 'sharena.wav',
      'rein': 'magic.wav',
      'linus': 'linus.wav',
      'raven': 'linus.wav',
      'poro': 'oliver.wav',
      'oliver': 'oliver.wav',
    };

    if (value in wavs) {
      playWav(wavs[value]);
    }
  });
});
