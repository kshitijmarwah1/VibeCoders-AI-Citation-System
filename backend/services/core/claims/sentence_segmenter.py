"""
Advanced sentence segmentation using NLP techniques.
Properly handles abbreviations, decimal numbers, and complex punctuation.
"""
import re
import logging
from typing import List

logger = logging.getLogger(__name__)

# Common abbreviations that shouldn't end sentences
ABBREVIATIONS = {
    'mr', 'mrs', 'ms', 'dr', 'prof', 'sr', 'jr', 'vs', 'etc', 'e.g', 'i.e',
    'a.m', 'p.m', 'am', 'pm', 'inc', 'ltd', 'corp', 'co', 'st', 'ave', 'blvd',
    'no', 'vol', 'pp', 'fig', 'ed', 'eds', 'approx', 'est', 'min', 'max',
    'dept', 'univ', 'assn', 'gov', 'misc', 'cf', 'ca', 'ex', 'al', 'et', 'al'
}

# Patterns for numbers, URLs, emails that shouldn't be split
NUMBER_PATTERN = r'\d+\.\d+'
URL_PATTERN = r'https?://[^\s]+'
EMAIL_PATTERN = r'\S+@\S+\.\S+'

def is_abbreviation(word: str) -> bool:
    """Check if a word is a common abbreviation."""
    word_clean = word.lower().rstrip('.')
    return word_clean in ABBREVIATIONS or word_clean.endswith(('st', 'nd', 'rd', 'th'))


def smart_sentence_segment(text: str) -> List[str]:
    """
    Intelligently segment text into sentences using NLP-aware rules.
    Handles abbreviations, decimal numbers, URLs, and complex punctuation.
    """
    if not text or not text.strip():
        return []

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Protect URLs and emails from being split
    protected_items = []
    text_with_placeholders = text
    
    # Replace URLs with placeholders
    url_matches = list(re.finditer(URL_PATTERN, text))
    for i, match in enumerate(url_matches):
        placeholder = f"__URL_{i}__"
        protected_items.append(('url', match.group()))
        text_with_placeholders = text_with_placeholders.replace(match.group(), placeholder)
    
    # Replace emails with placeholders
    email_matches = list(re.finditer(EMAIL_PATTERN, text_with_placeholders))
    for i, match in enumerate(email_matches):
        placeholder = f"__EMAIL_{i}__"
        protected_items.append(('email', match.group()))
        text_with_placeholders = text_with_placeholders.replace(match.group(), placeholder)
    
    # Split by sentence endings, but be smart about it
    # Pattern: sentence ending followed by space and capital letter
    # But also handle cases like "Dr. Smith" or "3.14 is pi"
    sentences = []
    current_sentence = []
    words = text_with_placeholders.split()
    
    i = 0
    while i < len(words):
        word = words[i]
        current_sentence.append(word)
        
        # Check if word ends with sentence punctuation
        if re.search(r'[.!?]$', word):
            # Check if it's likely a sentence ending
            is_sentence_end = False
            
            # If next word exists and starts with capital, likely sentence end
            if i + 1 < len(words):
                next_word = words[i + 1]
                # Check if next word starts with capital (but not all caps like acronyms)
                if next_word and next_word[0].isupper() and not next_word.isupper():
                    # Additional check: not an abbreviation
                    if not is_abbreviation(word):
                        is_sentence_end = True
                # Also end if next word is a number (new sentence often starts with number)
                elif next_word and next_word[0].isdigit():
                    is_sentence_end = True
            else:
                # Last word, definitely sentence end
                is_sentence_end = True
            
            # Special cases: don't split on decimal numbers
            if re.match(NUMBER_PATTERN, word):
                is_sentence_end = False
            
            if is_sentence_end:
                sentence_text = ' '.join(current_sentence)
                if sentence_text.strip():
                    sentences.append(sentence_text.strip())
                current_sentence = []
        
        i += 1
    
    # Add remaining sentence
    if current_sentence:
        sentence_text = ' '.join(current_sentence)
        if sentence_text.strip():
            sentences.append(sentence_text.strip())
    
    # Restore protected items
    restored_sentences = []
    for sentence in sentences:
        restored = sentence
        for item_type, original in protected_items:
            if item_type == 'url':
                restored = restored.replace(f"__URL_{sentences.index(sentence) if sentence in sentences else 0}__", original)
            elif item_type == 'email':
                restored = restored.replace(f"__EMAIL_{sentences.index(sentence) if sentence in sentences else 0}__", original)
        restored_sentences.append(restored)
    
    # Final cleanup: merge sentences that are too short (likely false splits)
    final_sentences = []
    for sentence in restored_sentences:
        if len(sentence) < 10 and final_sentences:
            # Merge with previous sentence
            final_sentences[-1] += " " + sentence
        else:
            final_sentences.append(sentence)
    
    return [s.strip() for s in final_sentences if s.strip() and len(s.strip()) >= 10]

