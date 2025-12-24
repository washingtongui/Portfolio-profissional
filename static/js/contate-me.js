// Aguarda o carregamento completo do DOM (HTML)
document.addEventListener("DOMContentLoaded", function () {

    // Seleciona todos os alertas (mensagens de sucesso/erro) na página
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(function (alert) {
        // Define um cronômetro para fechar o alerta automaticamente
        setTimeout(function () {
            // Verifica se o Bootstrap está carregado para usar a função de fechar
            if (typeof bootstrap !== 'undefined') {
                let bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                // Caso o Bootstrap falhe, remove o elemento do HTML manualmente
                alert.style.display = 'none';
            }
        }, 5000); // 5000 milissegundos = 5 segundos
    });
});