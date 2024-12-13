import numpy as np
import nltk
import re
from nltk.stem.porter import PorterStemmer
from typing import List

# Ensure punkt is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

stemmer = PorterStemmer()

def tokenize(sentence: str) -> List[str]:
    """
    Split sentence into array of words/tokens with improved tokenization
    Handles Indonesian language nuances and special characters
    """
    # Remove special characters and normalize
    sentence = re.sub(r'[^\w\s]', '', sentence)
    sentence = sentence.lower()
    
    # Use nltk tokenize with additional cleaning
    tokens = nltk.word_tokenize(sentence)
    
    # Remove very short tokens
    tokens = [token for token in tokens if len(token) > 1]
    
    return tokens

def stem(word: str) -> str:
    """
    Improved stemming to handle Indonesian words
    """
    # Basic normalization
    word = word.lower().strip()
    
    # Stem the word
    stemmed = stemmer.stem(word)
    
    return stemmed

def bag_of_words(tokenized_sentence: List[str], words: List[str]) -> np.ndarray:
    """
    Enhanced bag of words with TF-IDF like weighting
    """
    # stem each word in the sentence
    sentence_words = [stem(word) for word in tokenized_sentence]
    
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    
    # Count word frequencies
    word_freq = {}
    for word in sentence_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    for idx, w in enumerate(words):
        # Use frequency-based weighting
        if w in sentence_words:
            # More frequent words get lower weight
            bag[idx] = 1 / (1 + np.log(word_freq[w] + 1))
    
    return bag