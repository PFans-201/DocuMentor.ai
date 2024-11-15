import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QInputDialog, QMessageBox
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from PyDictionary import PyDictionary
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
import nlpaug.augmenter.word as naw
import requests
from collections import defaultdict

# Ensure NLTK packages are downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

MODEL_PATH = 'models/dialogue/2024-11-15-12-30-00.tar.gz'  # Specify the path to the trained Rasa model
dictionary = PyDictionary()

# Rasa Chatbot Class
class RasaChatbot:
    def __init__(self, model_directory):
        self.interpreter = RasaNLUInterpreter(model_directory)
        self.agent = Agent.load(model_directory, interpreter=self.interpreter)

    def get_response(self, message):
        responses = self.agent.handle_text(message)
        return responses[0]['text']

# NLP Augmentation Rephraser Class
class NLPAugRephraser:
    def __init__(self):
        self.aug = naw.SynonymAug(aug_src='wordnet')

    def rephrase(self, text):
        return self.aug.augment(text)

# MyMemory Translator Class
class MyMemoryTranslator:
    def translate(self, text, source_lang, target_lang):
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
        response = requests.get(url)
        data = response.json()
        return data['responseData']['translatedText']

# PDF Manager Class
class PDFManager:
    def __init__(self):
        self.pdf_text = ""
        self.pdf_contents = defaultdict(str)

    def upload_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            self.pdf_text = text
            self.pdf_contents[file_path] = text

    def summarize_pdf(self, file_path, num_sentences=3):
        text = self.pdf_contents.get(file_path, "")
        sentences = text.split('. ')
        return '. '.join(sentences[:num_sentences]) + '.' if sentences else "No content to summarize."

    def search_keywords(self, keyword):
        matches = []
        for file_path, content in self.pdf_contents.items():
            if keyword.lower() in content.lower():
                sentences = [sentence for sentence in content.split('. ') if keyword.lower() in sentence.lower()]
                matches.extend(sentences)
        return matches

    def get_definitions(self, terms):
        definitions = {}
        for term in terms:
            definition = dictionary.meaning(term)
            if definition:
                definitions[term] = ', '.join(definition.get('Noun', ['No definition found']))
            else:
                definitions[term] = "No definition found"
        return definitions

# Main Window Class (PyQt5 GUI)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Manager and Rasa Chatbot")
        self.setGeometry(100, 100, 800, 600)

        # Layout and Widgets
        self.layout = QVBoxLayout()
        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.layout.addWidget(self.text_display)

        # Initialize managers and services
        self.pdf_manager = PDFManager()
        self.rasa_chatbot = RasaChatbot(MODEL_PATH)
        self.nlpaug_rephraser = NLPAugRephraser()
        self.mymemory_translator = MyMemoryTranslator()

        # Buttons
        self.upload_button = QPushButton("Upload PDF", self)
        self.upload_button.clicked.connect(self.upload_pdf)
        self.layout.addWidget(self.upload_button)

        self.summary_button = QPushButton("Summarize PDF", self)
        self.summary_button.clicked.connect(self.summarize_pdf)
        self.layout.addWidget(self.summary_button)

        self.keyword_button = QPushButton("Search Keyword", self)
        self.keyword_button.clicked.connect(self.search_keyword)
        self.layout.addWidget(self.keyword_button)

        self.chat_button = QPushButton("Chat with Bot", self)
        self.chat_button.clicked.connect(self.chat_with_bot)
        self.layout.addWidget(self.chat_button)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def upload_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.pdf_manager.upload_pdf(file_path)
            self.text_display.setText(f"Uploaded PDF: {file_path}\n\n{self.pdf_manager.pdf_text[:1000]}...")

    def summarize_pdf(self):
        summary = self.pdf_manager.summarize_pdf(self.pdf_manager.pdf_contents.keys()[0])
        self.text_display.setText(f"Summary:\n\n{summary}")

    def search_keyword(self):
        keyword, ok = QInputDialog.getText(self, "Search Keyword", "Enter keyword:")
        if ok and keyword:
            matches = self.pdf_manager.search_keywords(keyword)
            if matches:
                self.text_display.setText(f"Keyword matches:\n\n" + "\n".join(matches))
            else:
                self.text_display.setText(f"No matches found for '{keyword}'.")

    def chat_with_bot(self):
        user_input, ok = QInputDialog.getText(self, "Chat with Bot", "You:")
        if ok and user_input:
            bot_response = self.rasa_chatbot.get_response(user_input)
            self.text_display.setText(f"You: {user_input}\nBot: {bot_response}")

# Main Function to Start the Application
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
