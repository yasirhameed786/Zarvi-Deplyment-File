// Assuming the 'displayMessage' function definition is correct and available

document.getElementById('user-input-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const userInputField = document.getElementById('user-input');
    const userInputText = userInputField.value.trim();

    if (userInputText) {
        displayMessage(userInputText, 'user');
        userInputField.value = ''; // Clear input after sending
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInputText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                displayMessage(data.message, 'bot');
            } else {
                displayMessage('No response from server or undefined message.', 'bot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage('Error in processing your message.', 'bot');
        });
    } else {
        displayMessage('Please enter some text.', 'user');
    }
});

function displayMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = message;
    document.getElementById('chat-box').appendChild(messageDiv);
}
