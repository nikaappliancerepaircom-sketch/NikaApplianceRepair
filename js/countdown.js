// Countdown Timer
function startCountdown(minutesId, secondsId) {
    let minutes = 14;
    let seconds = 45;
    
    const minutesEl = document.getElementById(minutesId);
    const secondsEl = document.getElementById(secondsId);
    
    if (!minutesEl || !secondsEl) return;
    
    const timer = setInterval(() => {
        if (seconds === 0) {
            if (minutes === 0) {
                clearInterval(timer);
                // Reset timer
                minutes = 14;
                seconds = 45;
                startCountdown(minutesId, secondsId);
                return;
            }
            minutes--;
            seconds = 59;
        } else {
            seconds--;
        }
        
        minutesEl.textContent = minutes.toString().padStart(2, '0');
        secondsEl.textContent = seconds.toString().padStart(2, '0');
    }, 1000);
}

// Start countdown timers when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Start both countdown timers if they exist
    if (document.getElementById('minutes') && document.getElementById('seconds')) {
        startCountdown('minutes', 'seconds');
    }
    if (document.getElementById('minutes-2') && document.getElementById('seconds-2')) {
        startCountdown('minutes-2', 'seconds-2');
    }
});