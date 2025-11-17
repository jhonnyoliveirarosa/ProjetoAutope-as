document.addEventListener("DOMContentLoaded", function () {
    console.log("Sistema Autopeças carregado com sucesso!");

    // Aqui você pode adicionar funções globais, como menu, alerts etc.
});

// static/js/main.js
$(document).ready(function() {
  // Inicializa o Select2 para busca de produtos
const $select = $('#select-produto');
if ($select.length) {
    $select.select2({
    placeholder: 'Digite o nome ou código do produto...',
    ajax: {
        url: '/buscar_produtos',
        dataType: 'json',
        delay: 250,
        data: function (params) {
          return { q: params.term }; // parâmetro de busca
        },
        processResults: function (data) {
          return { results: data }; // adapta resposta do Flask
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
}
});


