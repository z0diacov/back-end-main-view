from unidecode import unidecode

def transcript_to_eng(other_language_str: str) -> str:
    english_sstr = unidecode(other_language_str)
    return english_sstr