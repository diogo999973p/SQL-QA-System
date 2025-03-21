document.getElementById('ask-button').addEventListener('click', function () {
    const question = document.getElementById('question-input').value;

    if (!question) {
        alert('Please enter a question.');
        return;
    }

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById('sql-query').textContent = data.sql_query;
        document.getElementById('answer').textContent = data.answer;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});