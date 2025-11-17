document.addEventListener("DOMContentLoaded", () => {
    const filtro = document.getElementById("filtro");
    const tabela = document.getElementById("tabela-clientes").getElementsByTagName("tbody")[0];

    filtro.addEventListener("keyup", () => {
        const termo = filtro.value.toLowerCase();

        Array.from(tabela.rows).forEach(row => {
            const texto = row.innerText.toLowerCase();
            row.style.display = texto.includes(termo) ? "" : "none";
        });
    });
});
