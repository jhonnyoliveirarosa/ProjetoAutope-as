// static/js/itens_nota.js
document.addEventListener("DOMContentLoaded", function () {
  console.log("📦 Script itens_nota.js carregado!");

  // jQuery wrapper pro select e input
  const $selectProduto = $('#produto');
  const $campoPreco = $('#preco_unitario');
  const $form = $('#form-item');

  if (!$selectProduto.length || !$campoPreco.length || !$form.length) {
    console.warn("⚠️ Elementos não encontrados (produto/preco/form). Verifique IDs em itens.html.");
    return;
  }

  // Inicializa Select2 (se estiver disponível)
  try {
    if ($.fn.select2) {
      $selectProduto.select2({
        placeholder: "🔍 Buscar produto...",
        allowClear: true,
        width: '100%'
      });
    } else {
      console.log("ℹ️ Select2 não encontrado — select seguirá padrão HTML.");
    }
  } catch (err) {
    console.warn("Erro ao inicializar Select2:", err);
  }

  // Função que atualiza o campo de preço com base na opção selecionada
  function atualizarPreco() {
    // pega a option selecionada via jQuery
    const $option = $selectProduto.find('option:selected');
    const preco = $option.data('preco'); // jQuery .data('preco') lê "data-preco"
    // Se undefined, coloca vazio
    $campoPreco.val(preco !== undefined ? preco : '');
    console.log("🛒 Produto selecionado:", $option.text(), "→ Preço:", preco);
  }

  // Atualiza assim que carregar (caso venha com valor já selecionado)
  atualizarPreco();

  // Quando o select mudar (Select2 dispara change normalmente)
  $selectProduto.on('change', atualizarPreco);

  // Validação no submit (evita enviar sem preco/quantidade)
  $form.on('submit', function (e) {
    const quantidade = Number($form.find('input[name="quantidade"]').val());
    const precoVal = $campoPreco.val();

    if (! $selectProduto.val()) {
      e.preventDefault();
      alert("Selecione um produto antes de adicionar.");
      return false;
    }

    if (!quantidade || quantidade <= 0) {
      e.preventDefault();
      alert("Informe uma quantidade válida (maior que zero).");
      return false;
    }

    if (!precoVal || precoVal === "") {
      // Se preco vazio, tenta extrair da option — última tentativa
      atualizarPreco();
      if (!$campoPreco.val()) {
        e.preventDefault();
        alert("Preço unitário não definido. Verifique o produto selecionado.");
        return false;
      }
    }

    // tudo ok -> permite o envio
    console.log("Enviando formulário — produto_id:", $selectProduto.val(), "quantidade:", quantidade, "preco:", $campoPreco.val());
    return true;
  });
});
