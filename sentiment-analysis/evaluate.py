import os
import sys
from app.analyzer import SentimentAnalyzer

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Define evaluation sentences
EVALUATION_SENTENCES = [
    # Positive
    {"text": "I love this product, it works perfectly and exceeded my expectations!", "expected": "Positive"},
    {"text": "An absolutely wonderful experience from start to finish.", "expected": "Positive"},
    {"text": "The customer support team was incredibly helpful and solved my issue immediately.", "expected": "Positive"},
    {"text": "This is a great achievement and we are all very proud.", "expected": "Positive"},
    
    # Negative
    {"text": "This is the worst service I have ever experienced.", "expected": "Negative"},
    {"text": "I am highly disappointed with the quality and want a full refund.", "expected": "Negative"},
    {"text": "The app keeps crashing every time I try to open it, very frustrating.", "expected": "Negative"},
    {"text": "This was a complete waste of time and money.", "expected": "Negative"},
    
    # Neutral
    {"text": "The package arrived at 3 PM yesterday.", "expected": "Neutral"},
    {"text": "This book contains ten chapters of text.", "expected": "Neutral"},
    {"text": "I am planning to go for a walk in the park later today.", "expected": "Neutral"},
    {"text": "The meeting will take place in the main conference room.", "expected": "Neutral"}
]

def run_evaluation():
    print("=" * 70)
    print(" SENTIMENT ANALYSIS MODEL EVALUATION SUITE")
    print("=" * 70)
    
    analyzer = SentimentAnalyzer()
    
    passed = 0
    total = len(EVALUATION_SENTENCES)
    results = []

    # Print Table Header
    print(f"{'No.':<4} | {'Sentence (truncated)':<35} | {'Expected':<10} | {'Predicted':<10} | {'Status':<6}")
    print("-" * 70)

    for idx, item in enumerate(EVALUATION_SENTENCES, 1):
        text = item["text"]
        expected = item["expected"]
        
        # Run analyzer
        res = analyzer.analyze(text)
        predicted = res["sentiment"]
        
        status = "PASS" if predicted == expected else "FAIL"
        if status == "PASS":
            passed += 1
            
        results.append({
            "idx": idx,
            "text": text,
            "expected": expected,
            "predicted": predicted,
            "status": status,
            "compound": res["scores"]["compound"]
        })
        
        # Truncate text for table output
        truncated_text = text if len(text) <= 32 else text[:32] + "..."
        print(f"{idx:<4} | {truncated_text:<35} | {expected:<10} | {predicted:<10} | {status:<6}")

    print("-" * 70)
    accuracy = (passed / total) * 100
    print(f"Accuracy: {passed}/{total} ({accuracy:.2f}%)")
    print("=" * 70)

    # --- Edge Cases & Validation Checks ---
    print("\n" + "=" * 70)
    print(" TESTING INPUT VALIDATION CHECKS")
    print("=" * 70)
    
    # 1. Empty string check
    print("1. Testing empty input check:")
    try:
        analyzer.analyze("")
    except ValueError as ve:
        print(f"   [SUCCESS] Raised expected ValueError: '{ve}'")
    except Exception as e:
        print(f"   [FAILURE] Raised wrong exception: {type(e).__name__} - {e}")
    else:
        print("   [FAILURE] Did not raise exception on empty input.")

    # 2. Non-string check (integer)
    print("\n2. Testing non-string input check (integer):")
    try:
        analyzer.analyze(12345)
    except TypeError as te:
        print(f"   [SUCCESS] Raised expected TypeError: '{te}'")
    except Exception as e:
        print(f"   [FAILURE] Raised wrong exception: {type(e).__name__} - {e}")
    else:
        print("   [FAILURE] Did not raise exception on non-string input.")

    # 3. Non-string check (list)
    print("\n3. Testing non-string input check (list):")
    try:
        analyzer.analyze(["hello", "world"])
    except TypeError as te:
        print(f"   [SUCCESS] Raised expected TypeError: '{te}'")
    except Exception as e:
        print(f"   [FAILURE] Raised wrong exception: {type(e).__name__} - {e}")
    else:
        print("   [FAILURE] Did not raise exception on list input.")
        
    print("=" * 70)
    
    # Let's check if there are any failures or incorrect predictions
    failures = [r for r in results if r["status"] == "FAIL"]
    if failures:
        print("\nIncorrect Predictions:")
        for f in failures:
            print(f"- Text: '{f['text']}'")
            print(f"  Expected: {f['expected']}, Predicted: {f['predicted']} (Compound: {f['compound']})")
    else:
        print("\nAll standard validation sentences predicted correctly!")
        print("VADER analyzer achieved 100% accuracy on this validation suite.")
        
    # Let's also print 2 "borderline" or interesting predictions where scores were low/uncertain
    print("\nAnalysis of borderline or notable sentences:")
    # Sort results by absolute compound score to find the most neutral/uncertain ones
    borderline = sorted(results, key=lambda x: abs(x["compound"]))
    for i in range(min(2, len(borderline))):
        item = borderline[i]
        print(f"- Sentence: '{item['text']}'")
        print(f"  Expected: {item['expected']}, Predicted: {item['predicted']} (Compound: {item['compound']})")
        print(f"  Reason: The compound score of {item['compound']} is close to 0, showing it is neutral or highly balanced.")

if __name__ == "__main__":
    run_evaluation()
