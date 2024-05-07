document.addEventListener("DOMContentLoaded", function() {
    const toggleButton = document.getElementById("toggleButton");
    const gastosTable = document.getElementById("tabla-gastos");

    toggleButton.addEventListener("click", function() {
        if (gastosTable.style.display === "none") {
            gastosTable.style.display = "table";
            toggleButton.textContent = "Ocultar Historial";
        } else {
            gastosTable.style.display = "none";
            toggleButton.textContent = "Mostrar Historial";
        }
    });
});
