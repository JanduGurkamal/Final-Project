document.getElementById('mic').addEventListener('click', function () {
    const userInput = ''

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
