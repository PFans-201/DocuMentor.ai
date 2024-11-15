import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QDialog, QLabel, QLineEdit, QInputDialog, QWidget
)
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from PyDictionary import PyDictionary
from collections import defaultdict
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
import nlpaug.augmenter.word as naw
import requests

# Ensure NLTK packages are downloaded
nltk.download('popular', quiet=True)

class RasaChatbot:
    '''A class representing a Rasa chatbot.'''

    def __init__(self, model_directory):
        '''
        Initialize the RasaChatbot.

        Args:
            model_directory (str): Path to the directory containing the Rasa chatbot model.
        '''
        self.interpreter = RasaNLUInterpreter(model_directory)
        self.agent = Agent.load(model_directory, interpreter=self.interpreter)

    def get_response(self, message):
        '''
        Get the response from the Rasa chatbot for a given message.

        Args:
            message (str): Input message.

        Returns:
            str: Response from the Rasa chatbot.
        '''
        responses = self.agent.handle_text(message)
        return responses[0]['text']

class NLPAugRephraser:
    '''A class representing a NLPAug rephraser.'''

    def __init__(self):
        '''Initialize the NLPAugRephraser'''
        self.aug = naw.SynonymAug(aug_src='wordnet')

    def rephrase(self, text):
        '''
        Rephrase the given text.

        Args:
            text (str): Input text to be rephrased.

        Returns:
            str: Rephrased text.
        '''
        return self.aug.augment(text)

class MyMemoryTranslator:
    '''A class representing a MyMemory translator.'''

    def translate(self, text, source_lang, target_lang):
        '''
        Translate the given text from source language to target language using MyMemory translator API.

        Args:
            text (str): Text to be translated.
            source_lang (str): Source language code.
            target_lang (str): Target language code.

        Returns:
            str: Translated text.
        '''
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
        response = requests.get(url)
        data = response.json()
        return data['responseData']['translatedText']

class PDFManager:
    '''A class representing a PDF manager.'''

    def __init__(self):
        '''Initialize the PDFManager.'''
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
            str: Contents of the PDF file.
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
            num_sentences (int): Number of sentences for the summary.

        Returns:
            str: Summary of the PDF file contents.
        '''
        text = self.pdf_contents[file_path]
        sentences = text.split('. ')
        summarized_text = '. '.join(sentences[:num_sentences]) + '.'
        return summarized_text

    def search_keywords(self, user_input: str):
        '''
        Search for keywords in the PDF files.

        Args:
            user_input (str): Keyword to search for.

        Returns:
            dict: Dictionary containing PDF file paths and matching sentences.
        '''
        definitions = {}
        for file_path, content in self.pdf_contents.items():
            if user_input.lower() in content.lower():
                sentences = [sentence + '.' for sentence in content.split('. ') if user_input.lower() in sentence.lower()]
                definitions[file_path] = ' '.join(sentences)
        return definitions

    def get_definitions(self, terms: list):
        '''
        Get definitions for terms using PyDictionary.

        Args:
            terms (list): List of terms to get definitions for.

        Returns:
            dict: Dictionary containing terms and their definitions.
        '''
        dictionary = PyDictionary()
        definitions = {}
        for term in terms:
            definition = dictionary.meaning(term)
            if definition:
                formatted_definition = ', '.join(definition.get('Noun', ['No definition found']))
                definitions[term] = formatted_definition
            else:
                definitions[term] = "No definition found"
        return definitions

class PDFManagerApp(QMainWindow):
    '''A class representing the PDF Manager application.'''

    def __init__(self, rasa_bot_path):
        '''
        Initialize the PDFManagerApp.

        Args:
            rasa_bot_path (str): Path to the Rasa chatbot model directory.
        '''
        super().__init__()

        self.setWindowTitle("PDF Manager")

        self.pdf_manager = PDFManager()
        self.rasa_chatbot = RasaChatbot(rasa_bot_path)
        self.nlpaug_rephraser = NLPAugRephraser()
        self.mymemory_translator = MyMemoryTranslator()

        layout = QVBoxLayout()

        upload_button = QPushButton("Upload PDFs and Summarize")
        upload_button.clicked.connect(self.upload_and_summarize)
        layout.addWidget(upload_button)

        explain_button = QPushButton("Explain a Keyword or Concept")
        explain_button.clicked.connect(self.ask_for_explanation)
        layout.addWidget(explain_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def upload_and_summarize(self):
        '''Upload PDF files and summarize their contents.'''
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_path:
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.pdf'):
                    pdf_path = os.path.join(folder_path, file_name)
                    self.pdf_manager.upload_pdf(pdf_path)
                    summary = self.pdf_manager.summarize_pdf(pdf_path)
                    QMessageBox.information(self, "Summary", f"Summary for {file_name}:\n{summary}")

    def ask_for_explanation(self):
        '''Ask for user input and provide explanations.'''
        keyword, ok = QInputDialog.getText(self, "Input", "Enter the keyword or concept you need help with:")
        if ok and keyword:
            definitions = self.pdf_manager.search_keywords(keyword)
            if definitions:
                message = f"{keyword} found in the following documents:\n\n"
                message += '\n'.join([f"{file_path}: {definition}" for file_path, definition in definitions.items()])
                QMessageBox.information(self, "Explanation", message)
            else:
                definition = self.pdf_manager.get_definitions([keyword])
                QMessageBox.information(self, "Explanation", f"{keyword}: {definition[keyword]}")

            rasa_response = self.rasa_chatbot.get_response(keyword)
            QMessageBox.information(self, "Rasa Chatbot Response", rasa_response)

            rephrased_text = self.nlpaug_rephraser.rephrase(keyword)
            QMessageBox.information(self, "Rephrased Text", rephrased_text)

            translated_text = self.mymemory_translator.translate(keyword, 'en', 'pt')
            QMessageBox.information(self, "Translated Text", translated_text)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = PDFManagerApp('/path/to/your/rasa_bot_model_directory')
    window.show()
    sys.exit(app.exec_())
