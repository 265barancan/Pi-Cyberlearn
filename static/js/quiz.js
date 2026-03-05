document.addEventListener('DOMContentLoaded', () => {
    let currentQuestionIndex = 0;
    let score = 0;
    let questions = [];

    const elements = {
        loadingSpinner: document.getElementById('loading-spinner'),
        questionArea: document.getElementById('question-area'),
        questionText: document.getElementById('question-text'),
        optionsContainer: document.getElementById('options-container'),
        feedbackArea: document.getElementById('feedback-area'),
        feedbackMessage: document.getElementById('feedback-message'),
        feedbackExplanation: document.getElementById('feedback-explanation'),
        nextBtn: document.getElementById('next-btn'),
        questionCounter: document.getElementById('question-counter'),
        quizFooter: document.getElementById('quiz-footer'),
        resultArea: document.getElementById('result-area'),
        finalScore: document.getElementById('final-score'),
    };

    // Soruları yükle
    fetch(`/quiz/api/questions/${MODULE_ID}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            questions = data;
            elements.loadingSpinner.classList.add('hidden');
            if (questions.length > 0) {
                elements.questionArea.classList.remove('hidden');
                elements.quizFooter.classList.remove('hidden');
                loadQuestion(currentQuestionIndex);
            } else {
                elements.questionArea.innerHTML = "<p class='text-center text-gray-400'>Bu modül için soru bulunamadı.</p>";
                elements.questionArea.classList.remove('hidden');
            }
        })
        .catch(error => {
            console.error('Soru çekme hatası:', error);
            alert('Sorular yüklenirken hata oluştu');
        });

    function loadQuestion(index) {
        const q = questions[index];
        elements.questionCounter.textContent = `Soru ${index + 1} / ${questions.length}`;
        elements.questionText.textContent = q.question;
        elements.optionsContainer.innerHTML = '';
        elements.feedbackArea.classList.add('hidden');
        elements.nextBtn.disabled = true;

        q.options.forEach((option, idx) => {
            const btn = document.createElement('button');
            btn.className = 'w-full text-left px-5 py-3 rounded border border-gray-600 bg-gray-700 hover:bg-gray-600 text-white transition focus:outline-none';
            btn.textContent = option;
            btn.onclick = () => submitAnswer(q.id, idx, btn);
            elements.optionsContainer.appendChild(btn);
        });
    }

    function submitAnswer(questionId, selectedIdx, clickedBtn) {
        // Tüm seçenekleri devre dışı bırak
        const allButtons = elements.optionsContainer.querySelectorAll('button');
        allButtons.forEach(btn => btn.disabled = true);

        fetch('/quiz/api/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                module_id: MODULE_ID,
                question_id: questionId,
                selected_index: selectedIdx
            })
        })
        .then(response => response.json())
        .then(result => {
            elements.feedbackArea.classList.remove('hidden');
            elements.feedbackExplanation.textContent = result.explanation;

            // Renklendirme
            if (result.is_correct) {
                clickedBtn.classList.remove('bg-gray-700', 'hover:bg-gray-600', 'border-gray-600');
                clickedBtn.classList.add('bg-green-600', 'border-green-500', 'text-white');
                elements.feedbackArea.className = 'mt-6 p-4 rounded-md bg-green-900/50 border border-green-800 text-green-200';
                elements.feedbackMessage.textContent = "✅ Doğru Cevap!";
                score++;
            } else {
                clickedBtn.classList.remove('bg-gray-700', 'hover:bg-gray-600', 'border-gray-600');
                clickedBtn.classList.add('bg-red-600', 'border-red-500', 'text-white');
                elements.feedbackArea.className = 'mt-6 p-4 rounded-md bg-red-900/50 border border-red-800 text-red-200';
                elements.feedbackMessage.textContent = "❌ Yanlış Cevap!";
                
                // Doğruyu göster
                allButtons[result.correct_index].classList.remove('bg-gray-700');
                allButtons[result.correct_index].classList.add('bg-green-900', 'border-green-700');
            }

            elements.nextBtn.disabled = false;
        });
    }

    elements.nextBtn.addEventListener('click', () => {
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            loadQuestion(currentQuestionIndex);
        } else {
            showResults();
        }
    });

    function showResults() {
        elements.questionArea.classList.add('hidden');
        elements.quizFooter.classList.add('hidden');
        elements.questionCounter.textContent = 'Sonuç Ekranı';
        elements.resultArea.classList.remove('hidden');
        
        const percentage = Math.round((score / questions.length) * 100);
        elements.finalScore.textContent = `${score} / ${questions.length} (%${percentage})`;
    }
});
