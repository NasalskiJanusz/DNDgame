window.onload = function() {
    const startGameBtn = document.getElementById("startGameBtn");
    const loadGameBtn = document.getElementById("loadGameBtn");
    const settingsBtn = document.getElementById("settingsBtn");
    const gameArea = document.getElementById("gameArea");
    const menu = document.querySelector(".menu");
    const backToMenuBtn = document.getElementById("backToMenuBtn");
    const canvas = document.getElementById("gameCanvas");
    const context = canvas.getContext("2d");
    const backgroundMusic = document.getElementById("backgroundMusic");
    const toggleMusicBtn = document.getElementById("toggleMusicBtn");
    const musicIcon = toggleMusicBtn.querySelector("i");

    canvas.width = 800;
    canvas.height = 600;

    // Zmienna do sprawdzenia, czy muzyka jest odtwarzana
    let isMusicPlaying = false;

    // Ustaw początkową ikonę
    updateMusicIcon();

    // Funkcja do odtwarzania lub zatrzymywania muzyki
    function toggleMusic() {
        if (isMusicPlaying) {
            backgroundMusic.pause();
        } else {
            backgroundMusic.play().catch(error => {
                console.error("Muzyka nie mogła zostać odtworzona:", error);
            });
        }
        isMusicPlaying = !isMusicPlaying; // Przełącz stan
        updateMusicIcon(); // Zaktualizuj ikonę
    }

    // Funkcja do aktualizacji ikony
    function updateMusicIcon() {
        if (isMusicPlaying) {
            musicIcon.classList.remove("bi-volume-mute");
            musicIcon.classList.add("bi-volume-up");
        } else {
            musicIcon.classList.remove("bi-volume-up");
            musicIcon.classList.add("bi-volume-mute");
        }
    }

    // Funkcja do rozpoczęcia gry
    startGameBtn.onclick = function() {
        menu.style.display = "none";
        gameArea.style.display = "block";
        startGame();
    };

    // Funkcja do powrotu do menu
    backToMenuBtn.onclick = function() {
        gameArea.style.display = "none";
        menu.style.display = "block";
        backgroundMusic.pause(); // Zatrzymaj muzykę przy powrocie do menu
        backgroundMusic.currentTime = 0; // Resetuj czas do początku
        isMusicPlaying = false; // Zresetuj stan odtwarzania
        updateMusicIcon(); // Zaktualizuj ikonę
    };

    // Inicjalizacja gry
    function startGame() {
        context.fillStyle = "green";
        context.fillRect(50, 50, 100, 100); // Przykładowy element gry
    }

    // Obsługuje kliknięcie przycisku do odtwarzania muzyki
    toggleMusicBtn.onclick = toggleMusic;
};
