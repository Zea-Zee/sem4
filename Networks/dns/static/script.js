const input = document.getElementById('url');
const suggestionsContainer = document.getElementById('suggestions');
const submitButton = document.getElementById('parser-submit-button');

let suggestions = []

document.addEventListener("DOMContentLoaded", async function() {
    try {
        const response = await fetch('/check');
        const data = await response.json();
        suggestions = data.suggestions;
        console.log("Pedning and data is", data)
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
});


input.addEventListener('input', async function(event) {
    const inputValue = input.value.trim();
    if (inputValue.length === 0) {
        suggestionsContainer.classList.remove('open');
        return;
    }
    try {
        suggestionsContainer.innerHTML = '';
        const matchingSuggestions = suggestions.filter(suggestion => suggestion.toLowerCase().indexOf(inputValue.toLowerCase()) !== -1);
        matchingSuggestions.forEach((suggestion) => {
            const suggestionElement = document.createElement('div');
            suggestionElement.textContent = suggestion;
            suggestionElement.classList.add('suggestion'); // Добавляем класс для подсказки
            suggestionElement.addEventListener('click', function() {
                input.value = suggestion;
                suggestionsContainer.classList.remove('open');
            });

            suggestionsContainer.appendChild(suggestionElement);
        });

        suggestionsContainer.classList.add('open');
    } catch (error) {
        console.error('Error in rendering suggestions:', error);
    }
});


submitButton.addEventListener('click', async function(event) {
    const inputValue = input.value.trim();
    const isValid = suggestions.some(suggestion => inputValue.startsWith(suggestion));
    if (!isValid) {
        document.body.style.transition = 'background-color 0.2s ease';
        document.body.style.backgroundColor = 'pink';
        setTimeout(() => {
            document.body.style.backgroundColor = '';
        }, 200);
    } else {
        try {
            const response = await fetch(`/parse?url=${inputValue}`);
            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
});
