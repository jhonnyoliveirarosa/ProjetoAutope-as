$(document).ready(function() {
  $('#select-produto').select2({
    placeholder: 'Digite o nome ou código do produto...',
    ajax: {
      url: '/buscar_produtos',
      dataType: 'json',
      delay: 250,
      data: function (params) {
        return { q: params.term };
      },
      processResults: function (data) {
        return { results: data };
      },
      cache: true
    },
    minimumInputLength: 1,
    language: {
      inputTooShort: function() {
        return 'Digite pelo menos 1 caractere para buscar';
      },
      noResults: function() {
        return 'Nenhum produto encontrado';
      }
    }
  });
});
