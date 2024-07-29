document.getElementById('flashcard').addEventListener('click', function () {
    this.classList.toggle('flipped');
});

document.getElementById('refresh-btn').addEventListener('click', function() {
    const mode = "{{ mode }}";
    fetch(`/get_random_question/${mode}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('front-middle').innerText = data[1];
            document.getElementById('front-bottom').innerText = data[0];
            document.getElementById('back-middle').innerText = data[2];
        });
});
