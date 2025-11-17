document.addEventListener("DOMContentLoaded", () => {
  const ctxBar = document.getElementById("graficoMovimentacoes")?.getContext("2d");
  const ctxPie = document.getElementById("graficoPizza")?.getContext("2d");

  if (!ctxBar || !ctxPie) {
    console.warn("Canvas de gráfico não encontrado.");
    return;
  }

  // === GRÁFICO DE BARRAS ===
  new Chart(ctxBar, {
    type: "bar",
    data: {
      labels: dias,
      datasets: [
        { label: "Entradas", data: entradas_por_dia, backgroundColor: "rgba(14,165,233,0.9)" },
        { label: "Saídas", data: saidas_por_dia, backgroundColor: "rgba(248,113,113,0.9)" },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { color: "#cfeeff" },
          grid: { color: "rgba(255,255,255,0.05)" },
        },
        y: {
          ticks: { color: "#cfeeff" },
          grid: { color: "rgba(255,255,255,0.05)" },
          beginAtZero: true,
        },
      },
      plugins: {
        legend: { labels: { color: "#cfeeff" } },
        title: { display: true, text: "Movimentações por Dia", color: "#cfeeff" },
      },
      animation: { duration: 800, easing: "easeOutQuart" },
    },
  });

  // === GRÁFICO DE PIZZA ===
  const entradas = parseFloat(totalEntradas) || 0;
  const saidas = parseFloat(totalSaidas) || 0;

  const dataPizza =
    entradas + saidas > 0 ? [entradas, saidas] : [0.0001, 0.0001]; // evita ficar "travado"

  new Chart(ctxPie, {
    type: "pie",
    data: {
      labels: ["Entradas", "Saídas"],
      datasets: [
        {
          data: dataPizza,
          backgroundColor: ["#0ea5e9", "#f87171"],
          hoverOffset: 10,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom", labels: { color: "#cfeeff" } },
        title: { display: true, text: "Entradas x Saídas", color: "#cfeeff" },
      },
      animation: { animateScale: true, animateRotate: true },
    },
  });
});
