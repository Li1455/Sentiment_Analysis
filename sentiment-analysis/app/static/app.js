// 12 Predefined Validation Sentences
const validationSentences = [
    // Positive (4)
    { id: 1, text: "I love this product, it works perfectly and exceeded my expectations!", expected: "Positive" },
    { id: 2, text: "An absolutely wonderful experience from start to finish.", expected: "Positive" },
    { id: 3, text: "The customer support team was incredibly helpful and solved my issue immediately.", expected: "Positive" },
    { id: 4, text: "This is a great achievement and we are all very proud.", expected: "Positive" },
    
    // Negative (4)
    { id: 5, text: "This is the worst service I have ever experienced.", expected: "Negative" },
    { id: 6, text: "I am highly disappointed with the quality and want a full refund.", expected: "Negative" },
    { id: 7, text: "The app keeps crashing every time I try to open it, very frustrating.", expected: "Negative" },
    { id: 8, text: "This was a complete waste of time and money.", expected: "Negative" },
    
    // Neutral (4)
    { id: 9, text: "The package arrived at 3 PM yesterday.", expected: "Neutral" },
    { id: 10, text: "This book contains ten chapters of text.", expected: "Neutral" },
    { id: 11, text: "I am planning to go for a walk in the park later today.", expected: "Neutral" },
    { id: 12, text: "The meeting will take place in the main conference room.", expected: "Neutral" }
];

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const textInput = document.getElementById("text-input");
    const charCounter = document.getElementById("char-counter");
    const clearBtn = document.getElementById("clear-btn");
    const analyzeBtn = document.getElementById("analyze-btn");
    const errorAlert = document.getElementById("error-alert");
    const errorMsg = document.getElementById("error-msg");
    
    const resultPlaceholder = document.getElementById("result-placeholder");
    const resultContent = document.getElementById("result-content");
    const resultCard = document.getElementById("result-card");
    const sentimentBadge = document.getElementById("sentiment-badge");
    const confidencePercentage = document.getElementById("confidence-percentage");
    const confidenceBar = document.getElementById("confidence-bar");
    
    const posScore = document.getElementById("pos-score");
    const posBar = document.getElementById("pos-bar");
    const negScore = document.getElementById("neg-score");
    const negBar = document.getElementById("neg-bar");
    const neuScore = document.getElementById("neu-score");
    const neuBar = document.getElementById("neu-bar");
    const compoundScore = document.getElementById("compound-score");
    const compoundBar = document.getElementById("compound-bar");
    
    const testTableBody = document.getElementById("test-table-body");
    const runAllTestsBtn = document.getElementById("run-all-tests-btn");
    const testSummaryDashboard = document.getElementById("test-summary-dashboard");
    const summaryAccuracy = document.getElementById("summary-accuracy");
    const summaryPassed = document.getElementById("summary-passed");
    const summaryFailed = document.getElementById("summary-failed");

    // Initialize: Render Validation Table
    renderValidationTable();

    // Event Listeners
    textInput.addEventListener("input", updateCharCount);
    clearBtn.addEventListener("click", clearInput);
    analyzeBtn.addEventListener("click", performCustomAnalysis);
    runAllTestsBtn.addEventListener("click", runAllTests);

    // Helpers
    function updateCharCount() {
        const length = textInput.value.length;
        charCounter.textContent = `${length} / 1000 characters`;
    }

    function clearInput() {
        textInput.value = "";
        updateCharCount();
        hideError();
        resetResultCard();
    }

    function showError(message) {
        errorMsg.textContent = message;
        errorAlert.classList.remove("hidden");
    }

    function hideError() {
        errorAlert.classList.add("hidden");
    }

    function resetResultCard() {
        resultPlaceholder.classList.remove("hidden");
        resultContent.classList.add("hidden");
        // Reset classes on content
        resultContent.classList.remove("positive-result", "negative-result", "neutral-result");
    }

    // Call Sentiment API
    async function analyzeText(text) {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Failed to analyze sentiment.");
        }
        return data;
    }

    // Handle Custom Sentiment Analysis
    async function performCustomAnalysis() {
        const text = textInput.value;
        
        // Front-end check before API call
        if (!text || text.trim() === "") {
            showError("Input text cannot be empty or whitespace-only.");
            return;
        }

        hideError();
        
        // Show loading state
        const loader = analyzeBtn.querySelector(".btn-loader");
        const btnText = analyzeBtn.querySelector("span:not(.btn-loader)");
        loader.classList.remove("hidden");
        btnText.textContent = "Analyzing...";
        analyzeBtn.disabled = true;

        try {
            const result = await analyzeText(text);
            displayResult(result);
        } catch (error) {
            showError(error.message);
            resetResultCard();
        } finally {
            loader.classList.add("hidden");
            btnText.textContent = "Analyze Sentiment";
            analyzeBtn.disabled = false;
        }
    }

    // Render results in the result card
    function displayResult(result) {
        resultPlaceholder.classList.add("hidden");
        resultContent.classList.remove("hidden");

        // Set classes
        resultContent.classList.remove("positive-result", "negative-result", "neutral-result");
        resultContent.classList.add(`${result.sentiment.toLowerCase()}-result`);

        // Badge
        sentimentBadge.textContent = result.sentiment;
        sentimentBadge.className = `sentiment-badge ${result.sentiment.toLowerCase()}`;

        // Confidence
        const confidenceVal = Math.round(result.confidence * 100);
        confidencePercentage.textContent = `${confidenceVal}%`;
        confidenceBar.style.width = `${confidenceVal}%`;

        // Breakdown scores
        posScore.textContent = result.scores.positive.toFixed(3);
        posBar.style.width = `${result.scores.positive * 100}%`;

        negScore.textContent = result.scores.negative.toFixed(3);
        negBar.style.width = `${result.scores.negative * 100}%`;

        neuScore.textContent = result.scores.neutral.toFixed(3);
        neuBar.style.width = `${result.scores.neutral * 100}%`;

        compoundScore.textContent = result.scores.compound.toFixed(4);
        // Map compound score (-1.0 to 1.0) to bar percentage (0% to 100%)
        const compoundPercent = ((result.scores.compound + 1) / 2) * 100;
        compoundBar.style.width = `${compoundPercent}%`;
    }

    // Render Validation Table Rows
    function renderValidationTable() {
        testTableBody.innerHTML = "";
        validationSentences.forEach((item) => {
            const tr = document.createElement("tr");
            tr.id = `test-row-${item.id}`;
            
            const badgeClass = item.expected.toLowerCase();
            
            tr.innerHTML = `
                <td class="table-sentence">${item.text}</td>
                <td class="table-sentiment text-${badgeClass}">${item.expected}</td>
                <td class="predicted-sentiment text-muted">-</td>
                <td><span class="status-badge pending">Pending</span></td>
                <td><button class="btn btn-secondary btn-sm run-single-btn" data-id="${item.id}" style="padding: 0.3rem 0.75rem; font-size: 0.8rem;">Run</button></td>
            `;
            testTableBody.appendChild(tr);
        });

        // Add action listeners to single run buttons
        document.querySelectorAll(".run-single-btn").forEach((btn) => {
            btn.addEventListener("click", async (e) => {
                const id = parseInt(e.target.getAttribute("data-id"));
                const item = validationSentences.find(s => s.id === id);
                textInput.value = item.text;
                updateCharCount();
                
                // Highlight row in UI
                const row = document.getElementById(`test-row-${id}`);
                row.style.backgroundColor = "rgba(139, 92, 246, 0.1)";
                setTimeout(() => {
                    row.style.backgroundColor = "";
                }, 1000);

                // Run API analysis
                await performCustomAnalysis();
                
                // Update table row with prediction
                try {
                    const res = await analyzeText(item.text);
                    updateTableRow(id, res.sentiment, item.expected);
                } catch (err) {
                    console.error(err);
                }
            });
        });
    }

    // Update single table row after check
    function updateTableRow(id, predicted, expected) {
        const row = document.getElementById(`test-row-${id}`);
        const predCell = row.querySelector(".predicted-sentiment");
        const statusCell = row.querySelector(".status-badge");

        predCell.textContent = predicted;
        predCell.className = `predicted-sentiment table-sentiment text-${predicted.toLowerCase()}`;

        const isMatch = (predicted === expected);
        statusCell.textContent = isMatch ? "Pass" : "Fail";
        statusCell.className = isMatch ? "status-badge pass" : "status-badge fail";
    }

    // Run Full Test Suite Sequentially
    async function runAllTests() {
        runAllTestsBtn.disabled = true;
        runAllTestsBtn.textContent = "Running Suite...";
        
        let passedCount = 0;
        
        for (const item of validationSentences) {
            const row = document.getElementById(`test-row-${item.id}`);
            const statusCell = row.querySelector(".status-badge");
            statusCell.textContent = "...";
            statusCell.className = "status-badge pending";
            
            try {
                const res = await analyzeText(item.text);
                updateTableRow(item.id, res.sentiment, item.expected);
                
                if (res.sentiment === item.expected) {
                    passedCount++;
                }
            } catch (err) {
                console.error(`Error validating sentence ${item.id}:`, err);
                statusCell.textContent = "Error";
                statusCell.className = "status-badge fail";
            }
            
            // Subtle delay to make execution visible
            await new Promise(r => setTimeout(r, 100));
        }

        // Render Summary Dashboard
        const total = validationSentences.length;
        const accuracyVal = Math.round((passedCount / total) * 100);
        
        summaryAccuracy.textContent = `${accuracyVal}%`;
        summaryPassed.textContent = `${passedCount} / ${total}`;
        summaryFailed.textContent = total - passedCount;

        testSummaryDashboard.classList.remove("hidden");
        runAllTestsBtn.disabled = false;
        runAllTestsBtn.textContent = "Run Full Test Suite";
    }
});
