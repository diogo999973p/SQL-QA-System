document.getElementById('ask-button').addEventListener('click', function () {
    const question = document.getElementById('question-input').value;

    if (!question) {
        alert('Please enter a question.');
        return;
    }

    // Show the loader
    const loader = document.getElementById('loader');
    loader.style.display = 'block';  // Show the loader

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Json response:", data);  // Check raw output in console
        
        loader.style.display = 'none';  // Hide the loader

        if (data.error) {
            alert(data.error);
            return;
        }

        //formatted_answer = data.answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        document.getElementById('sql-query').textContent = data.sql_query;
        document.getElementById('answer').innerHTML = data.answer;
    })
    .catch(error => {
        console.log('Error:', error);
        loader.style.display = 'none';  // Hide the loader
    });
});

/* fetch('/ask', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question: question }),
})
.then(response => response.text())  // Convert to text instead of JSON
.then(data => {
    console.log("Raw response:", data);  // Check raw output in console
    return JSON.parse(data);  // Now try parsing
})
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
 */