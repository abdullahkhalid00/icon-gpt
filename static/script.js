document.getElementById('queryForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const queryInput = document.getElementById('queryInput').value;
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    
    if (!queryInput.trim()) {
        resultsDiv.innerText = 'Please enter a keyword.';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/search', {
            method: 'POST',
            body: JSON.stringify({
                query: queryInput,
                top_k: 3
            }),
            headers: {
                'Content-type': 'application/json'
            }
        })

        data = await response.json()
        
        data.results.forEach(result => {
            const emojiDiv = document.createElement('div')
            emojiDiv.innerHTML = `<p>${result.emoji} - ${result.short_description}</p>`
            resultsDiv.appendChild(emojiDiv)
        })
    } catch(e) {
        resultsDiv.innerText = `An error occurred: ${e.message}`
    }
});
