function deleteItem(element, name, type) {
    fetch('/update_items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'delete', name: name, type: type })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            element.parentElement.remove(); // Rimuove l'elemento dalla lista
        }
    });
}

function editItem(element, name, type) {
    const newName = prompt("Modifica il nome:", name);
    if (newName && newName !== name) {
        fetch('/update_items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: 'edit', name: name, newName: newName, type: type })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                element.parentElement.querySelector('span').textContent = newName; // Aggiorna il nome visualizzato
            }
        });
    }
}

function reSort() {
    fetch('/re_draw')
        .then(response => response.json())
        .then(data => {
            const results = document.getElementById('results');
            results.innerHTML = '';  // Pulisce i risultati esistenti
            data.pairs.forEach(pair => {
                const li = document.createElement('li');
                li.textContent = `${pair[0]} - ${pair[1]}`;
                results.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
}
