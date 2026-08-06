# Sentiment Analysis Studio

A lightweight, high-performance Sentiment Analysis API and web application built from scratch in Python. It utilizes **NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner)** model to classify text into **Positive**, **Negative**, or **Neutral** sentiments.

This project features a fully responsive, modern glassmorphism web interface and a robust HTTP API backend, built with **zero third-party web framework dependencies** (no Flask/FastAPI required) to ensure maximum compatibility and zero compile-time dependencies.

---

## Features
- **NLP Sentiment Engine**: Classifies sentences using NLTK VADER compound polarity thresholds.
- **Robust Input Validation**: Basic checks for empty strings, whitespace-only, and non-string inputs at both engine and API levels (returns `400 Bad Request`).
- **Interactive Web Interface**: Beautiful, responsive dark-themed dashboard featuring real-time analysis, score gauges, and a validation test suite launcher.
- **Terminal Evaluation Suite**: Command-line validation script (`evaluate.py`) that tests 12 benchmark sentences, measures model accuracy, and checks type-handling constraints.

---

## Tech Stack
- **Backend API**: Python 3 (built-in `http.server` module for HTTP routing and API serving)
- **NLP Library**: `nltk` (using the `vader_lexicon` package)
- **Frontend UI**: Vanilla HTML5, modern CSS3 (custom CSS variables, background glow effects, micro-animations, glassmorphic card panels), and Vanilla JavaScript (Fetch API)

---

## Installation & Setup

1. **Clone the Repository** (or navigate to the project directory):
   ```bash
   cd sentiment-analysis
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: This project only requires `nltk` as an external dependency).*

3. **Download the NLTK VADER Lexicon**:
   Run the following command to download the VADER lexicon database:
   ```bash
   python -c "import nltk; nltk.download('vader_lexicon')"
   ```

---

## How to Run

### 1. Launch the Web Interface & API
Run the main server script:
```bash
python app/main.py
```
Once started, open your web browser and navigate to:
👉 **[http://localhost:8000](http://localhost:8000)**

From this interface, you can:
- Type any custom text and click **Analyze Sentiment** to get real-time score breakdowns.
- Run individual tests from the validation table.
- Click **Run Full Test Suite** to run all 12 validation sentences and view a live accuracy dashboard.

### 2. Run the Evaluation Script (CLI)
To run the automated validation tests and edge-case validation checks in the terminal:
```bash
python evaluate.py
```

---

## Test Evaluation Results

The terminal evaluation suite (`evaluate.py`) yields the following output:

```text
======================================================================
 SENTIMENT ANALYSIS MODEL EVALUATION SUITE
======================================================================
No.  | Sentence (truncated)                | Expected   | Predicted  | Status
----------------------------------------------------------------------
1    | I love this product, it works pe... | Positive   | Positive   | PASS  
2    | An absolutely wonderful experien... | Positive   | Positive   | PASS  
3    | The customer support team was in... | Positive   | Positive   | PASS  
4    | This is a great achievement and ... | Positive   | Positive   | PASS  
5    | This is the worst service I have... | Negative   | Negative   | PASS  
6    | I am highly disappointed with th... | Negative   | Negative   | PASS  
7    | The app keeps crashing every tim... | Negative   | Negative   | PASS  
8    | This was a complete waste of tim... | Negative   | Negative   | PASS  
9    | The package arrived at 3 PM yest... | Neutral    | Neutral    | PASS  
10   | This book contains ten chapters ... | Neutral    | Neutral    | PASS  
11   | I am planning to go for a walk i... | Neutral    | Neutral    | PASS  
12   | The meeting will take place in t... | Neutral    | Neutral    | PASS  
----------------------------------------------------------------------
Accuracy: 12/12 (100.00%)
======================================================================

======================================================================
 TESTING INPUT VALIDATION CHECKS
======================================================================
1. Testing empty input check:
   [SUCCESS] Raised expected ValueError: 'Input text cannot be empty or whitespace-only.'

2. Testing non-string input check (integer):
   [SUCCESS] Raised expected TypeError: 'Input must be a string.'

3. Testing non-string input check (list):
   [SUCCESS] Raised expected TypeError: 'Input must be a string.'
======================================================================
```

---

## Incorrect/Uncertain Prediction Analysis

While NLTK's VADER achieved **100% accuracy** on the 12 standard benchmark sentences, lexicon-based NLP models have inherent limitations. Below is an analysis of two tricky sentences tested on the analyzer:

### Tricky Sentence 1: *"The movie was not bad, but I'd never watch it again."*
- **Expected Sentiment**: Neutral or slightly Negative (due to "never watch it again").
- **Model Prediction**: **Positive** (Compound Score: `0.2323`, Positive: `0.161`, Negative: `0.000`)
- **Analysis**: VADER successfully handles the negation "not bad" (turning "bad" into positive), but completely ignores the negative implication of "never watch it again". The word "never" acts as a modifier, but "watch" and "again" carry no negative lexicon weight in VADER. Consequently, the positive compound score of "not bad" dominates, leading to a false Positive classification.

### Tricky Sentence 2: *"Oh great, another delay in our project."*
- **Expected Sentiment**: Negative (sarcastic tone).
- **Model Prediction**: **Positive** (Compound Score: `0.4215`, Positive: `0.360`, Negative: `0.202`)
- **Analysis**: This is a classic failure case of **sarcasm**. VADER evaluates sentiment by summing up the pre-defined valence weights of words. The word "great" is heavily weighted as positive (`+0.360`), whereas "delay" is moderately negative (`-0.202`). Because VADER does not understand context or tone, it mathematically sums these and predicts a Positive sentiment, completely missing the negative sarcasm.

---

## Project Structure
```
sentiment-analysis/
│
├── app/
│   ├── __init__.py
│   ├── analyzer.py       # VADER sentiment engine & type checkers
│   ├── main.py           # HTTP server, routing, static server, and API
│   └── static/           # UI Assets
│       ├── index.html    # Frontend structure
│       ├── style.css     # Glassmorphic layout stylesheet
│       └── app.js        # DOM interactions and batch validation logic
│
├── evaluate.py           # CLI validation suite
├── requirements.txt      # nltk dependency
└── README.md             # This document
```
