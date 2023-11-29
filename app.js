// script.js

function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    document.getElementById('chat').innerHTML += '<div class="user-message">User: ' + userInput + '</div>';

    // Fetch response from the server
    fetch('/get?msg=' + userInput)
        .then(response => response.text())
        .then(data => {
            document.getElementById('chat').innerHTML += '<div class="bot-message">TherapistBot: ' + data + '</div>';
        });

    // Clear the input field
    document.getElementById('user-input').value = '';
}

// Call the sendMessage function when Enter key is pressed
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
