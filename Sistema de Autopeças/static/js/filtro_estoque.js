document.addEventListener("DOMContentLoaded", function () {
const campoFiltro = document.getElementById("filtro");
const tabela = document.getElementById("tabela-estoque").getElementsByTagName("tbody")[0];

campoFiltro.addEventListener("input", function () {
    const termo = this.value.toLowerCase();
    const linhas = tabela.getElementsByTagName("tr");

    for (let linha of linhas) {
    const textoLinha = linha.textContent.toLowerCase();
    linha.style.display = textoLinha.includes(termo) ? "" : "none";
    }
});
});
