function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';
    var text = 'Olá, Bem vindo Vamos conversar!';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];
                container.appendChild(letter);
                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 50);
            }, i * 250);
        })(i);
    }
    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);
    document.querySelector('.show-api.svelte-1rjryqp').style.display = 'none';
     document.querySelector('.built-with.svelte-1rjryqp').style.display = 'none';
    document.querySelector('#component-0 textarea[data-testid="textbox"]').style.display = 'none';
    document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector('.huggingface-space-header');
    if (header) {
        header.style.display = 'none';
      }
    });
    return 'Animation created';
}
