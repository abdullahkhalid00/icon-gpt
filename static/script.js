document.getElementById('queryForm').addEventListener('submit', async function(event) {
    event.preventDefault()

    const queryInput = document.getElementById('queryInput').value.trim()
    const resultsTable = document.getElementById('resultsTable')
    const resultsTableBody = resultsTable.querySelector('tbody')
    resultsTableBody.innerHTML = ''

    if (!queryInput) {
        alert('Please enter a keyword.')
        return
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/search', {
            method: 'POST',
            body: JSON.stringify({ query: queryInput }),
            headers: {
                'Content-type': 'application/json'
            }
        })

        const data = await response.json()

        data.results.forEach((result) => {
            const row = document.createElement('tr')

            const iconCell = document.createElement('td')
            iconCell.innerHTML = `
                ${result.emoji} 
                <span class="copy-icon" onclick="navigator.clipboard.writeText('${result.emoji}')">📋</span>
            `
            row.appendChild(iconCell)

            const tagsCell = document.createElement('td')
            tagsCell.textContent = result.tags.slice(0, 3).join(', ')
            row.appendChild(tagsCell)

            resultsTableBody.appendChild(row)
        })

        resultsTable.style.display = 'table'
    } catch (e) {
        alert(`An error occurred: ${e.message}`)
    }
})
