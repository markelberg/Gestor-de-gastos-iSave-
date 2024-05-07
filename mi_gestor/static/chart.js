document.addEventListener("DOMContentLoaded", function() {
    // Datos de ejemplo (reemplazar con tus datos reales)
    var datosGastos = {
        enero: 500,
        febrero: 600,
        marzo: 700,
    };

    var meses = Object.keys(datosGastos);
    var gastos = Object.values(datosGastos);

    // Configurar y dibujar el gráfico de barras
    var ctx = document.getElementById('barChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: meses,
            datasets: [{
                label: 'Gastos por Mes',
                data: gastos,
                backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color de fondo de las barras
                borderColor: 'rgba(255, 99, 132, 1)', // Color del borde de las barras
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true // Iniciar eje y desde cero
                }
            }
        }
    });
});
