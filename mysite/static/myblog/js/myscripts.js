document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.close-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            this.parentElement.style.opacity = '0';
            setTimeout(() => {
                this.parentElement.remove();
            }, 300);
        });
    });

    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});