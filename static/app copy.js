class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chat-container'),
            sendButton: document.querySelector('.send-button')
        }
        this.messages = [];
        this.init();
    }

    init() {
        this.addEventListeners();
        this.addInitialMessages();
    }

    addEventListeners() {
        const { sendButton } = this.args;
        const input = document.querySelector('.chat-input input');

        sendButton.addEventListener('click', () => this.onSendButton());
        
        input.addEventListener('keyup', ({ key }) => {
            if (key === 'Enter') {
                this.onSendButton();
            }
        });
    }

    addInitialMessages() {
        const openingMessages = [
            "Hai! Saya di sini untuk membantu Anda menjelajahi Desa Borobudur.",
            "Selamat datang! Ada yang ingin Anda ketahui tentang Desa Borobudur?"
        ];

        const randomMessage = openingMessages[Math.floor(Math.random() * openingMessages.length)];
        this.messages.push({ name: "Sam", message: randomMessage });
        this.updateChatText();
        this.updateSuggestions();
    }

    updateSuggestions() {
        const suggestedResponses = [
            "Harga tiket Candi Borobudur",
            "Lokasi hotel di Desa Borobudur",
            "Kuliner di Desa Borobudur",
            "Fasilitas di Candi Borobudur"
        ];

        const suggestionsWrapper = document.querySelector('.suggestions-wrapper');
        if (suggestionsWrapper) {
            suggestionsWrapper.innerHTML = suggestedResponses
                .map(resp => `<button class="suggested-btn">${resp}</button>`)
                .join('');
            
            this.addSuggestionsListeners();
        }
    }

    addSuggestionsListeners() {
        document.querySelectorAll('.suggested-btn').forEach(button => {
            // Remove existing listeners
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);

            newButton.addEventListener('click', () => {
                const selectedMessage = newButton.textContent;
                this.messages.push({ name: "User", message: selectedMessage });
                this.updateChatText();

                fetch($SCRIPT_ROOT + '/predict', {
                    method: 'POST',
                    body: JSON.stringify({ message: selectedMessage }),
                    mode: 'cors',
                    headers: { 'Content-Type': 'application/json' }
                })
                .then(response => response.json())
                .then(data => {
                    this.messages.push({ name: "Sam", message: data.answer });
                    this.updateChatText();
                })
                .catch(error => console.error('Error:', error));
            });
        });
    }

    onSendButton() {
        const input = document.querySelector('.chat-input input');
        const text = input.value.trim();

        if (text === "") return;

        this.messages.push({ name: "User", message: text });
        input.value = '';
        this.updateChatText();

        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text }),
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            this.messages.push({ name: "Sam", message: data.answer });
            this.updateChatText();
        })
        .catch(error => console.error('Error:', error));
    }

    updateChatText() {
        const messagesWrapper = document.querySelector('.messages-wrapper');
        let html = '';

        this.messages.forEach(item => {
            if (item.name === "Sam") {
                html += `<div class="messages__item messages__item--visitor">${item.message}</div>`;
            } else {
                html += `<div class="messages__item messages__item--operator">${item.message}</div>`;
            }
        });

        messagesWrapper.innerHTML = html;
        
        // Auto scroll to bottom
        const chatMessages = document.querySelector('.chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const chatbox = new Chatbox();
});