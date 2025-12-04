# Final Text Normalization System for Cardinals 0 to 1000

import pynini
import re

# ==============================================================================
# 1. Load the FAR file
# ==============================================================================

with pynini.Far("cardinal_normalization.far") as far:
    fst_0_to_1000 = far["cardinal_0_to_1000"]

# ==============================================================================
# 2. SENTENCE NORMALIZATION LOGIC
# ==============================================================================

def apply_fst(input_string, fst):
   
   # Applies an FST to a numeric input string and returns the shortest path result.
    
    try:
        input_acceptor = pynini.accep(input_string, token_type='utf8')
        result_composition = input_acceptor @ fst
        shortest_path = pynini.shortestpath(result_composition)
        if shortest_path.num_states() > 0:
            return shortest_path.string(token_type='utf8')
        else:
            return None
    except Exception:
        return None

def normalize_sentence(sentence, fst_grammar):
    
    #Takes a sentence, finds all cardinal numbers (0-1000) within it,
    #transduces them to text, and returns the normalized sentence.
    
    # Regex pattern: \b(\d{1,4})\b covers 0 through 1000
    number_pattern = r'\b(\d{1,4})\b'

    def replacement_func(match):
        number_string = match.group(1)
        normalized_text = apply_fst(number_string, fst_grammar)

        # Only replace if the FST successfully transduces the number
        if normalized_text:
            return normalized_text
        else:
            # If out of range (e.g., '1001'), return the original number string
            return number_string

    return re.sub(number_pattern, replacement_func, sentence)

# ==============================================================================
# 3. FINAL DEMONSTRATION
# ==============================================================================

if __name__ == '__main__':
    # Use the fully composed fst_0_to_1000 for final testing
    
    print("--- Final Text Normalization System (0-1000) ---")

    # Test 1: Compound tens and unit
    input1 = "I have 3 dogs and 21 cats."
    output1 = normalize_sentence(input1, fst_0_to_1000)
    print(f"Input:  '{input1}'")
    print(f"Output: '{output1}'")

    # Test 2: Exact hundred and the maximum value
    input2 = "The total cost was 400 dollars, reaching 1000 at the end."
    output2 = normalize_sentence(input2, fst_0_to_1000)
    print(f"Input:  '{input2}'")
    print(f"Output: '{output2}'")

    # Test 3: Hundred and Unit (B.E. 'and' convention) and leading zero
    input3 = "We started with 509 items and lost 07 in the process."
    output3 = normalize_sentence(input3, fst_0_to_1000)
    print(f"Input:  '{input3}'")
    print(f"Output: '{output3}'")

    # Test 4: Number out of range (should NOT be transduced)
    input4 = "We received 1001 boxes, but only 999 were counted."
    output4 = normalize_sentence(input4, fst_0_to_1000)
    print(f"Input:  '{input4}'")
    print(f"Output: '{output4}'")