import spacy
import re

# Lazy load the spacy model
_nlp = None

# Common medicine name patterns and suffixes
COMMON_MEDICINE_SUFFIXES = [
    'ine', 'ol', 'ate', 'ide', 'ium', 'um', 'in', 'on', 'an', 'yl',
    'oxazole', 'azole', 'mycin', 'cillin', 'pril', 'sartan', 'vir', 'stat'
]

# Common medicine brands/names database
COMMON_MEDICINES = {
    'aspirin', 'paracetamol', 'ibuprofen', 'naproxen', 'acetaminophen',
    'amoxicillin', 'penicillin', 'cephalexin', 'flucloxacillin',
    'metformin', 'insulin', 'glibenclamide', 'pioglitazone',
    'lisinopril', 'enalapril', 'ramipril', 'losartan', 'amlodipine',
    'atorvastatin', 'simvastatin', 'lovastatin',
    'omeprazole', 'pantoprazole', 'ranitidine', 'famotidine',
    'salbutamol', 'terbutaline', 'beclomethasone', 'fluticasone',
    'fluoxetine', 'sertraline', 'paroxetine', 'citalopram',
    'cetirizine', 'loratadine', 'fexofenadine',
    'amitriptyline', 'nortriptyline', 'doxycycline', 'tetracycline',
    'ciprofloxacin', 'levofloxacin', 'ofloxacin',
    'methotrexate', 'hydroxychloroquine', 'sulfasalazine',
    'theophylline', 'caffeine', 'codeine', 'morphine',
    'diclofenac', 'mefenamic', 'indomethacin',
    'vitamin', 'folic', 'calcium', 'magnesium', 'potassium', 'zinc',
    'glycerin', 'sorbitol', 'lactose', 'sucrose'
}

def _load_nlp_model():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "Spacy model 'en_core_web_sm' not found. "
                "Please install it with: python -m spacy download en_core_web_sm"
            )
    return _nlp

def _extract_by_pattern(text: str) -> list:
    """
    Extract potential medicine names using pattern matching and common suffixes.
    
    Args:
        text: The input text
        
    Returns:
        List of potential medicine names
    """
    medicines = []
    
    # More strict pattern: words that appear before dose information
    # or standalone medicine names
    patterns = [
        r'\b([A-Za-z]+)\s*(?:\d+\s*(?:mg|ml|mcg|units|IU|%))',  # Medicine with dose
        r'\b([A-Z][a-z]{3,})\s+(?:tablet|capsule|injection|ointment|syrup|powder)',  # Medicine with form
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            word = match.group(1).lower().strip()
            if word and word not in excluded_words:
                medicines.append(word)
    
    # Also check common medicines list
    words = re.findall(r'\b[a-z]+\b', text)
    for word in words:
        if word in COMMON_MEDICINES and word not in excluded_words:
            medicines.append(word)
    
    return list(set(medicines))

def extract_medicines(text: str):
    """
    Extract medicine names from text using multiple methods:
    1. Pattern matching against common medicine names
    2. Spacy NER for entities
    3. Suffix-based matching
    
    Args:
        text: The input text to extract medicines from
        
    Returns:
        List of unique medicine names found
    """
    medicines = set()
    
    # Clean text
    text = text.lower()
    
    # Method 1: Pattern-based extraction
    pattern_medicines = _extract_by_pattern(text)
    medicines.update(pattern_medicines)
    
    # Method 2: Spacy NER (fallback for recognized entities)
    try:
        nlp = _load_nlp_model()
        doc = nlp(text)
        
        for ent in doc.ents:
            entity_text = ent.text.lower()
            # Look for potential medicines in entities
            if any(suffix in entity_text for suffix in COMMON_MEDICINE_SUFFIXES):
                if len(entity_text) > 2:
                    medicines.add(entity_text)
    except Exception:
        pass  # Continue even if spacy fails
    
    # Filter out common non-medicine words and clinic/patient related terms
    excluded_words = {
        'time', 'date', 'day', 'morning', 'evening', 'night', 'meal', 'food',
        'clinic', 'hospital', 'doctor', 'patient', 'name', 'age', 'mob', 'mobile',
        'address', 'phone', 'consultant', 'physician', 'md', 'dr', 'ms', 'mr',
        'timing', 'delivery', 'home', 'free', 'daily', 'temp', 'temperature',
        'ram', 'sai', 'shree', 'sri', 'clinic', 'care', 'health', 'medical',
        'diagnosis', 'treatment', 'prescription', 'instructions', 'note', 'notes'
    }
    medicines = {m for m in medicines if m not in excluded_words}
    
    return sorted(list(medicines))