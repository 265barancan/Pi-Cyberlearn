document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const messagesContainer = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');

    if (!form || !input) return; // API yapılandırılmamışsa çalışmayabilir

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = input.value.trim();
        if (!message) return;

        // Kullanıcı mesajını ekle
        appendMessage('user', message);
        input.value = '';
        input.disabled = true;
        sendBtn.disabled = true;

        // "Yazıyor..." göstergesi ekle
        const typingId = appendTypingIndicator();

        try {
            const response = await fetch('/ai/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            removeElement(typingId);

            const data = await response.json();

            if (!response.ok) {
                appendMessage('error', data.error || 'Bir hata oluştu.');
            } else {
                appendMessage('ai', data.response);
            }
        } catch (error) {
            removeElement(typingId);
            appendMessage('error', 'Sunucuya bağlanılamadı. İnternet bağlantınızı kontrol edin.');
            console.error('Chat API Error:', error);
        } finally {
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
        }
    });

    function appendMessage(role, text) {
        const div = document.createElement('div');
        div.className = 'flex items-start';

        let html = '';

        if (role === 'user') {
            div.className += ' justify-end';
            html = `
                <div class="mr-3 bg-green-700/80 rounded-2xl rounded-tr-sm px-4 py-3 text-sm text-gray-100 shadow max-w-[80%] border border-green-600">
                    <p>${escapeHTML(text)}</p>
                </div>
                <div class="flex-shrink-0 w-8 h-8 rounded-full bg-green-900 border border-green-500 flex items-center justify-center mt-1 text-xs font-bold text-green-300">
                    SEN
                </div>
            `;
        } else if (role === 'ai') {
            // Basit markdown işleme (bold, listeler ve kod satırları)
            let formattedText = escapeHTML(text)
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/`(.*?)`/g, '<code class="bg-gray-800 text-yellow-300 px-1 rounded">$1</code>')
                .replace(/\n/g, '<br>');

            html = `
                <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-900 border border-blue-500 flex items-center justify-center mt-1">
                    <svg class="w-5 h-5 text-blue-300" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"></path></svg>
                </div>
                <div class="ml-3 bg-gray-700/80 rounded-2xl rounded-tl-sm px-4 py-3 text-sm text-gray-200 shadow max-w-[80%] border border-gray-600">
                    <p>${formattedText}</p>
                </div>
            `;
        } else if (role === 'error') {
            html = `
                <div class="mx-auto bg-red-900/50 rounded-lg px-4 py-2 text-sm text-red-200 shadow border border-red-800 text-center">
                    <p>⚠️ ${escapeHTML(text)}</p>
                </div>
            `;
        }

        div.innerHTML = html;
        messagesContainer.appendChild(div);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.className = 'flex items-start';

        div.innerHTML = `
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-900 border border-blue-500 flex items-center justify-center mt-1">
                <svg class="w-5 h-5 text-blue-300" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"></path></svg>
            </div>
            <div class="ml-3 bg-gray-700/80 rounded-2xl rounded-tl-sm px-4 py-3 shadow max-w-[80%] border border-gray-600 flex space-x-1 items-center h-10">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
        `;

        messagesContainer.appendChild(div);
        scrollToBottom();
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g,
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});
