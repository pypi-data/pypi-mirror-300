import string

months = {
    "en": {
        "January": "January", "February": "February", "March": "March",
        "April": "April", "May": "May", "June": "June", "July": "July",
        "August": "August", "September": "September", "October": "October",
        "November": "November", "December": "December",
    },
    "swa": {
        "January": "Januari", "February": "Februari", "March": "Machi",
        "April": "Aprili", "May": "Mei", "June": "Juni", "July": "Julai",
        "August": "Agosti", "September": "Septemba", "October": "Octoba",
        "November": "Novemba", "December": "Desemba",
    },
}



translations = {
    "lesson_title": {
        "en": "LESSON",
        "swa": "SOMO LA",
    },
    "quarter" : {
        "en": "Quarter",
        "swa": "Robo Ya",
    },
    "chapters" : {
        "en": "Chapters",
        "swa": "Sura",
    },
    "Sabbath School Lesson" : {
        "en": "Sabbath School Lesson",
        "swa": "Masomo Ya Shule Ya Sabato",
    },
    "All rights reserved" : {
        "en": "All rights reserved",
        "swa": "Haki zote zimehifadhiwa",
    }
}

def custom_title_case(s):
    words = s.split()
    titled_words = []
    for word in words:
        if "'" in word:
            parts = word.split("'")
            titled_word = parts[0].capitalize() + "'" + parts[1].lower()
        else:
            titled_word = word.capitalize()
        titled_words.append(titled_word)
    return ' '.join(titled_words)

def get_lesson_text(lang, case="title"):
    lesson_text = translations["lesson_title"][lang]
    if case == "title":
        lesson_text = custom_title_case(lesson_text)
    elif case == "upper":
        lesson_text = lesson_text.upper()
    return lesson_text

# def  translate_word(text, lang):
#     if text in translations.keys():
#         return translations[text][lang]
    
#     words = text.split()
    
#     # Translate each word
#     translated_words = []
#     for word in words:
#         # Check if the word has a translation
#         print(word, translations.keys())
#         if word in translations.keys():
#             print("found")
#             translated_word = translations[word].get(lang, word)  # Get translation or keep the original
#             translated_words.append(translated_word)
#         else:
#             translated_words.append(word)  # Keep the original word if no translation found

#     # Join the translated words back into a string
#     return ' '.join(translated_words)

# def translate_word(text, lang):
#     # Normalize case for the translation dictionary
#     normalized_translations = {k.lower(): v for k, v in translations.items()}

#     # Check if the entire text matches any translation directly
#     normalized_text = text.strip(string.punctuation).lower()
#     print("normalized_text", normalized_text)
#     if normalized_text in normalized_translations:
#         return normalized_translations[normalized_text][lang]

#     # Split the text into words
#     words = normalized_text.split()

#     # Translate each word
#     translated_words = []
#     for word in words:
#         # Normalize the word case for translation
#         normalized_word = word.lower()
#         # Check if the word has a translation
#         print(normalized_word)
#         if normalized_word in normalized_translations:
#             print("found")
#             translated_word = normalized_translations[normalized_word].get(lang, word)  # Get translation or keep the original
#             translated_words.append(translated_word)
#         else:
#             translated_words.append(word)  # Keep the original word if no translation found

#     # Join the translated words back into a string
#     return ' '.join(translated_words)

def translate_word(text, lang):
    # Normalize case for the translation dictionary
    normalized_translations = {k.lower(): v for k, v in translations.items()}

    # Remove leading/trailing punctuation and normalize the entire text
    normalized_text = text.strip(string.punctuation).lower()
    
    # Check if the entire text matches any translation directly
    if normalized_text in normalized_translations:
        return normalized_translations[normalized_text][lang]

    # Split the text into sentences (simple split on periods for this example)
    sentences = [sentence.strip() for sentence in text.split('.') if sentence]

    translated_sentences = []
    
    for sentence in sentences:
        # Check if the sentence has a translation
        normalized_sentence = sentence.lower()
        if normalized_sentence in normalized_translations:
            translated_sentences.append(normalized_translations[normalized_sentence][lang] +".")
        else:
            # If no sentence translation, split the sentence into words
            words = sentence.split()
            translated_words = []
            for word in words:
                # Remove punctuation and normalize the word case
                clean_word = word.strip(string.punctuation).lower()
                # Check if the word has a translation
                if clean_word in normalized_translations:
                    translated_word = normalized_translations[clean_word].get(lang, word)  # Get translation or keep the original
                    translated_words.append(translated_word)
                else:
                    translated_words.append(word)  # Keep the original word if no translation found
            # Join translated words back into a sentence
            translated_sentences.append(' '.join(translated_words))

    # Join translated sentences back into a string
    return '. '.join(translated_sentences)