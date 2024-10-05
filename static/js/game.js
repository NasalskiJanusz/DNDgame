window.onload = function() {
    const backgroundMusic = document.getElementById("backgroundMusic");
    const toggleMusicBtn = document.getElementById("toggleMusicBtn");
    const musicIcon = toggleMusicBtn.querySelector("i");

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

    // Obsługuje kliknięcie przycisku do odtwarzania muzyki
    toggleMusicBtn.onclick = toggleMusic;
};
