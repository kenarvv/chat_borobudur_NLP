class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input')
        node.addEventListener("keyup", ({key}) => {
            if (key == "Enter"){
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;
        
        if(this.state) {
            chatbox.classList.add('chatbox--active')
            this.addInitialMessages(chatbox);
        } else{
            chatbox.classList.remove('chatbox--active')
        }
    }
    addInitialMessages(chatbox) {
        if (this.messages.length === 0) {
            // Array pesan pembuka
            const openingMessages = [
                "Hai! Saya adalah Asisten Virtual Desa Borobudur. Ada yang bisa saya bantu?",
                "Halo! Butuh informasi tentang Desa Borobudur? Saya siap membantu!",
                "Selamat datang! Ada yang ingin Anda ketahui tentang Desa Borobudur?",
                "Hai! Saya di sini untuk membantu Anda menjelajahi Desa Borobudur.",
                "Halo! Bagaimana saya bisa membantu perjalanan Anda di Desa Borobudur hari ini?",
                "Selamat datang di Chatbot Desa Borobudur! Apa yang bisa saya bantu?",
                "Hai! Penasaran tentang tiket, fasilitas, atau lokasi di Desa Borobudur? Saya siap menjawab!",
                "Halo! Apa kabar? Saya di sini untuk mempermudah pencarian informasi Anda tentang Desa Borobudur.",
                "Selamat datang! Ingin tahu lebih banyak tentang Candi Borobudur dan sekitarnya?",
                "Hai! Ada yang bisa saya bantu hari ini? Jelajahi Desa Borobudur bersama saya!"
            ];
    
            // Pilih pesan pembuka secara acak
            const randomMessage = openingMessages[Math.floor(Math.random() * openingMessages.length)];
    
            // Tambahkan pesan pembuka ke dalam `this.messages`
            this.messages.push({ name: "Sam", message: randomMessage });
    
            // Suggested responses
            const suggestedResponses = [
                "Harga tiket Candi Borobudur",
                "Lokasi hotel di Desa Borobudur",
                "Kuliner di Desa Borobudur",
                "Fasilitas di Candi Borobudur"
            ];
    
            // Render suggestions box
            this.suggestionsBox = `
                <strong>Suggested:</strong>
                ${suggestedResponses.map(resp => `<button class="suggested-btn">${resp}</button>`).join(' ')}
            `;
    
            this.messages.push({ name: "Sam", message: this.suggestionsBox });
    
            // Render pesan
            this.updateChatText(chatbox);
    
            // Tambahkan event listener untuk tombol suggested responses
            this.addSuggestionsListeners(chatbox);
        }
    }

    addSuggestionsListeners(chatbox) {
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.querySelectorAll('.suggested-btn').forEach(button => {
            // Cegah duplikasi event listener
            if (button.dataset.listenerAdded === "true") return;
    
            button.addEventListener('click', () => {
                const selectedMessage = button.textContent;
    
                // Kirim pesan dari suggestion
                this.messages.push({ name: "User", message: selectedMessage });
    
                // Hapus suggestions box dari pesan
                this.messages = this.messages.filter(
                    msg => !msg.message.includes('<button') // Filter out suggestions box
                );
    
                // Render ulang chat
                this.updateChatText(chatbox);
    
                // Kirim ke backend (jika diperlukan)
                fetch($SCRIPT_ROOT + '/predict', {
                    method: 'POST',
                    body: JSON.stringify({ message: selectedMessage }),
                    mode: 'cors',
                    headers: { 'Content-Type': 'application/json' }
                })
                    .then(response => response.json())
                    .then(data => {
                        this.messages.push({ name: "Sam", message: data.answer });
                        this.updateChatText(chatbox);
                    })
                    .catch(error => console.error('Error:', error));
            });
    
            // Tandai tombol sebagai telah ditambahkan listener
            button.dataset.listenerAdded = "true";
        });
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const text = textField.value;
    
        if (text === "") {
            return;
        }
    
        // Tambahkan pesan pengguna
        this.messages.push({ name: "User", message: text });
    
        // Render ulang chat tanpa menghapus suggestions
        this.updateChatText(chatbox);
    
        // Bersihkan input
        textField.value = '';
    
        // Kirim ke backend (jika diperlukan)
        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text }),
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                this.messages.push({ name: "Sam", message: data.answer });
                this.updateChatText(chatbox);
            })
            .catch(error => console.error('Error:', error));
    }

    updateChatText(chatbox) {
        let html = '';
        this.messages.slice().reverse().forEach(item => {
            if (item.name === "Sam" && item.message.includes('<button')) {
                // Suggestions box tetap muncul
                html += `<div class="messages__item messages__item--visitor suggestions">${item.message}</div>`;
            } else if (item.name === "Sam") {
                html += `<div class="messages__item messages__item--visitor">${item.message}</div>`;
            } else {
                html += `<div class="messages__item messages__item--operator">${item.message}</div>`;
            }
        });
    
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    
        // Tambahkan event listener ulang untuk tombol suggestions (jika belum ada)
        this.addSuggestionsListeners(chatbox);
    }
}

const chatbox = new Chatbox();
chatbox.display()