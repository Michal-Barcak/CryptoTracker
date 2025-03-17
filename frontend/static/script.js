document.addEventListener('DOMContentLoaded', function() {
    const elements = {
        searchForm: document.getElementById('search-form'),
        resultDiv: document.getElementById('result'),
        actionButton: document.getElementById('action-button'),
        savedCryptosDiv: document.getElementById('saved-cryptos'),
        cryptoIdInput: document.getElementById('crypto-id')
    };
    
    loadSavedCryptocurrencies();
    elements.searchForm.addEventListener('submit', handleSearch);
    
    // Event handlers
    async function handleSearch(e) {
        e.preventDefault();
        const cryptoId = elements.cryptoIdInput.value.trim();
        
        if (!cryptoId) {
            alert('Please enter cryptocurrency ID');
            return;
        }
        
        try {
            const data = await fetchCryptoInfo(cryptoId);
            displayCryptoInfo(data);
            setupActionButtons(data, cryptoId);
        } catch (error) {
            displayError(error.message);
        }
    }
    
    // API functions
    async function fetchCryptoInfo(cryptoId) {
        const response = await fetch(`/cryptocurrency/info/${cryptoId}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error occurred while fetching data');
        }
        
        return await response.json();
    }
    
    async function handleApiOperation(url, method, successMessage, onSuccess) {
        try {
            const response = await fetch(url, { method });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Error during ${method} operation`);
            }
            
            alert(successMessage);
            loadSavedCryptocurrencies();
            if (onSuccess) onSuccess();
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }
    
    async function loadSavedCryptocurrencies() {
        try {
            const response = await fetch('/cryptocurrencies');
            const cryptos = await response.json();
            
            elements.savedCryptosDiv.innerHTML = cryptos.length === 0 
                ? '<p>No saved cryptocurrencies</p>'
                : createCryptoTable(cryptos);
        } catch (error) {
            elements.savedCryptosDiv.innerHTML = `<p>Error loading cryptocurrencies: ${error.message}</p>`;
        }
    }
    
    // UI functions
    function displayCryptoInfo(data) {
        elements.resultDiv.innerHTML = `
            <h3>${data.name} (${data.symbol.toUpperCase()})</h3>
            <p>Price: $${data.price_usd.toLocaleString()}</p>
            <p>Market Cap: $${data.market_cap.toLocaleString()}</p>
            <p>24h Volume: $${data.volume_24h.toLocaleString()}</p>
            <p>24h Change: ${data.price_change_24h !== null ? data.price_change_24h.toFixed(2) : 'N/A'}%</p>
        `;
        elements.resultDiv.style.display = 'block';
    }
    
    function setupActionButtons(data, cryptoId) {
        clearButtons();
        
        // Create new buttons container
        const buttonsContainer = document.createElement('div');
        buttonsContainer.className = 'crypto-buttons';
        buttonsContainer.style.display = 'flex';
        buttonsContainer.style.gap = '10px';
        
        if (data.exists_in_db) {
            // Update button
            elements.actionButton.textContent = 'Update';
            elements.actionButton.onclick = () => handleApiOperation(
                `/cryptocurrency/${cryptoId}`, 
                'PUT', 
                'Cryptocurrency successfully updated!'
            );
            
            // Delete button
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.onclick = () => {
                if (confirm(`Are you sure you want to delete ${data.name}?`)) {
                    handleApiOperation(
                        `/cryptocurrency/${cryptoId}`, 
                        'DELETE', 
                        'Cryptocurrency successfully deleted!',
                        () => {
                            elements.resultDiv.innerHTML += '<p>Cryptocurrency was deleted from database</p>';
                            clearButtons();
                        }
                    );
                }
            };

            buttonsContainer.appendChild(elements.actionButton);
            buttonsContainer.appendChild(deleteButton);

        } else {
            // Save button
            elements.actionButton.textContent = 'Save to DB';
            elements.actionButton.onclick = () => handleApiOperation(
                `/cryptocurrency?crypto_id=${cryptoId}`, 
                'POST', 
                'Cryptocurrency successfully saved!',
                () => handleSearch(new Event('submit'))
            );
            
            buttonsContainer.appendChild(elements.actionButton);
        }
        
        elements.resultDiv.after(buttonsContainer);
        elements.actionButton.style.display = 'block';
    }
    
    function displayError(message) {
        elements.resultDiv.innerHTML = `<p>Error: ${message}</p>`;
        elements.resultDiv.style.display = 'block';
        elements.actionButton.style.display = 'none';
        clearButtons();
    }
    
    function createCryptoTable(cryptos) {
        let html = '<table border="1" style="width:100%; border-collapse: collapse;">';
        html += '<tr><th>Name</th><th>Symbol</th><th>Price (USD)</th><th>Market Cap</th><th>Last Updated</th></tr>';
        
        for (const crypto of cryptos) {
            html += `
                <tr>
                <td>${crypto.name || 'N/A'}</td>
                <td>${crypto.symbol ? crypto.symbol.toUpperCase() : 'N/A'}</td>
                <td>$${crypto.price_usd ? crypto.price_usd.toLocaleString() : 'N/A'}</td>
                <td>$${crypto.market_cap ? crypto.market_cap.toLocaleString() : 'N/A'}</td>
                <td>${formatLocalTime(crypto.last_updated) || 'N/A'}</td>
                </tr>
            `;
        }
        
        return html += '</table>';
    }

    function formatLocalTime(utcTime) {
        if (!utcTime) return 'N/A';
        return new Date(utcTime).toLocaleString();
    }

    function clearButtons() {
        const existingButtonsContainer = document.querySelector('.crypto-buttons');
        if (existingButtonsContainer) {
            existingButtonsContainer.remove();
        }
    }
});
