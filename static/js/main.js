document.getElementById('mic').addEventListener('click', function () {
    let userInput = prompt("Speak to the virtual assistant:");

    fetch('/run_virtual_assistant', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
    })
        .then(response => response.json())
        .then(data => {
            alert("Virtual Assistant says: " + data.response);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});
