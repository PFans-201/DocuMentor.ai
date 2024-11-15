import requests

class MyMemoryTranslator:
    '''A class for translating text using the MyMemory API'''

    def translate(self, text, source_lang, target_lang):
        '''
        Translate the given text from the source language to the target language.

        Args:
            text (str): The text to be translated.
            source_lang (str): The source language code (e.g., 'en' for English).
            target_lang (str): The target language code (e.g., 'es' for Spanish).

        Returns:
            str: The translated text.
        '''
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
        response = requests.get(url)
        data = response.json()
        return data['responseData']['translatedText']
