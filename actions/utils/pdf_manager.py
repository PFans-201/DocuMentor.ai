from PyPDF2 import PdfReader
from collections import defaultdict

class PDFManager:
    '''A class for managing PDF files'''

    def __init__(self):
        self.pdf_files = []
        self.pdf_contents = defaultdict(str)

    def upload_pdf(self, file_path: str):
        '''
        Upload a PDF file and store its contents.

        Args:
            file_path (str): Path to the PDF file.
        '''
        self.pdf_files.append(file_path)
        self.pdf_contents[file_path] = self.read_pdf(file_path)

    def read_pdf(self, file_path: str):
        '''
        Read the contents of a PDF file.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            str: The text content of the PDF.
        '''
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text

    def summarize_pdf(self, file_path: str, num_sentences: int = 3):
        '''
        Summarize the contents of a PDF file.

        Args:
            file_path (str): Path to the PDF file.
            num_sentences (int): The number of sentences to include in the summary.

        Returns:
            str: The summarized text.
        '''
        text = self.pdf_contents[file_path]
        sentences = text.split('. ')
        summarized_text = '. '.join(sentences[:num_sentences]) + '.'
        return summarized_text

    def search_keywords(self, user_input: str):
        '''
        Search for keywords in the PDF files.

        Args:
            user_input (str): The keyword to search for.

        Returns:
            dict: A dictionary containing file paths and matching sentences.
        '''
        definitions = {}
        for file_path, content in self.pdf_contents.items():
            if user_input.lower() in content.lower():
                sentences = [sentence + '.' for sentence in content.split('. ') if user_input.lower() in sentence.lower()]
                definitions[file_path] = ' '.join(sentences)
        return definitions

    def get_definitions(self, terms: list):
        '''
        Get definitions for terms.

        Args:
            terms (list): A list of terms to get definitions for.

        Returns:
            dict: A dictionary containing terms and their definitions.
        '''
        definitions = {}
        for term in terms:
            definition = PyDictionary().meaning(term)
            if definition:
                formatted_definition = ', '.join(definition.get('Noun', ['No definition found']))
                definitions[term] = formatted_definition
            else:
                definitions[term] = "No definition found"
        return definitions
