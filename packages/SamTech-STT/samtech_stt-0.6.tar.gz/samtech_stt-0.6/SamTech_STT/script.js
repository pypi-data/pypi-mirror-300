const output =document.getElementById('output');
const startButton = document.getElementById('startButton');
let finalTranscript ="";

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition =new SpeechRecognition();
recognition.lang = "en-US";
recognition.interimResults = true;

startButton.addEventListener("click",()=>{
    finalTranscript = '',
    output.textContent = '',
    recognition.start();
    startButton.textContent = 'listning...';

});

recognition.addEventListener('result',(e) =>{
    const transcript = Array.from(e.results)
       .map(result => result[0])
       .map(result => result.transcript)
       .join('');

       if(e.results[0].isFinal){
        finalTranscript = transcript;
        output.textContent = finalTranscript;
       }
});

recognition.addEventListener('end',() => {
    startButton.textContent = 'startButton';
    recognition.start();
});

document.addEventListener('keydown',(e) => {
    if (e.key == 'ESC') {
        recognition.stop();
        startButton.textContent = 'startButton';
    }
});