import re
from typing import List, Dict, Any

def normalize_token(word: str) -> str:
    """Normalize a token for robust comparison: lowercase, strip punctuation, normalize quotes."""
    w = word.strip().lower()
    # Normalize curly apostrophes
    w = w.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # Strip leading/trailing punctuation
    w = re.sub(r"^[^\w']+|[^\w']+$", "", w)
    return w

def tokenize_sentence(sentence: str) -> List[str]:
    """Tokenize a sentence into words while preserving original tokens."""
    # Split by whitespace
    raw_tokens = sentence.split()
    return raw_tokens

def compute_dictation_diff(standard_text: str, user_input: str) -> Dict[str, Any]:
    """
    Perform word-level LCS alignment and classify differences:
    - match: exactly matches (after normalization)
    - missing: in standard text but missing in user input
    - extra: in user input but not in standard text
    - form_diff: base lemmas match or simple plural/tense difference (e.g. s, ed, ing)
    - spelling_diff: Levenshtein distance <= 2
    """
    std_tokens = tokenize_sentence(standard_text)
    user_tokens = tokenize_sentence(user_input)

    std_norm = [normalize_token(t) for t in std_tokens]
    user_norm = [normalize_token(t) for t in user_tokens]

    # Compute LCS dynamic programming table
    n = len(std_norm)
    m = len(user_norm)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if std_norm[i - 1] == user_norm[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to construct alignment diff tokens
    i, j = n, m
    diff_results = []
    matches = 0

    while i > 0 or j > 0:
        if i > 0 and j > 0 and std_norm[i - 1] == user_norm[j - 1]:
            diff_results.append({
                "type": "match",
                "standard": std_tokens[i - 1],
                "user": user_tokens[j - 1]
            })
            matches += 1
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and is_form_or_spelling_variation(std_norm[i - 1], user_norm[j - 1]):
            # Near match: plural, tense, or minor typo
            var_type = "form_diff" if is_form_variation(std_norm[i - 1], user_norm[j - 1]) else "spelling_diff"
            diff_results.append({
                "type": var_type,
                "standard": std_tokens[i - 1],
                "user": user_tokens[j - 1]
            })
            matches += 0.5  # partial credit
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            diff_results.append({
                "type": "extra",
                "standard": "",
                "user": user_tokens[j - 1]
            })
            j -= 1
        else:
            diff_results.append({
                "type": "missing",
                "standard": std_tokens[i - 1],
                "user": ""
            })
            i -= 1

    diff_results.reverse()

    accuracy = round(matches / max(n, 1), 2)
    accuracy = min(1.0, max(0.0, accuracy))

    return {
        "accuracy_score": accuracy,
        "is_perfect": accuracy >= 0.99,
        "diff_tokens": diff_results,
        "stats": {
            "total_words": n,
            "matched_words": sum(1 for d in diff_results if d["type"] == "match"),
            "missing_words": sum(1 for d in diff_results if d["type"] == "missing"),
            "extra_words": sum(1 for d in diff_results if d["type"] == "extra"),
            "form_errors": sum(1 for d in diff_results if d["type"] == "form_diff"),
            "spelling_errors": sum(1 for d in diff_results if d["type"] == "spelling_diff")
        }
    }

def is_form_variation(w1: str, w2: str) -> bool:
    """Check if w1 and w2 are inflectional variations (e.g. finding vs findings, help vs helped, policy vs policies)."""
    if not w1 or not w2:
        return False
    # Plural / 3rd person singular (s, es, ies)
    if w1 + "s" == w2 or w2 + "s" == w1 or w1 + "es" == w2 or w2 + "es" == w1:
        return True
    if (w1.endswith("y") and w1[:-1] + "ies" == w2) or (w2.endswith("y") and w2[:-1] + "ies" == w1):
        return True
    # Past tense (ed, d, ied)
    if w1 + "d" == w2 or w2 + "d" == w1 or w1 + "ed" == w2 or w2 + "ed" == w1:
        return True
    if (w1.endswith("y") and w1[:-1] + "ied" == w2) or (w2.endswith("y") and w2[:-1] + "ied" == w1):
        return True
    # Participle (ing)
    if w1 + "ing" == w2 or w2 + "ing" == w1 or (w1.rstrip("e") + "ing" == w2) or (w2.rstrip("e") + "ing" == w1):
        return True
    return False

def levenshtein_dist(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_dist(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def is_form_or_spelling_variation(w1: str, w2: str) -> bool:
    if is_form_variation(w1, w2):
        return True
    if len(w1) >= 4 and len(w2) >= 4:
        return levenshtein_dist(w1, w2) <= 2
    return False

if __name__ == "__main__":
    std = "The findings have profound implications for public policy."
    user = "The finding has profound implication for public policies."
    res = compute_dictation_diff(std, user)
    print("Diff accuracy:", res["accuracy_score"])
    for tok in res["diff_tokens"]:
        print(f"[{tok['type']}] Std: '{tok['standard']}' | User: '{tok['user']}'")
