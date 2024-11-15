import sys
import os
import PyPDF2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from rasa.core.agent import Agent
import requests
import nlpaug.augmenter.word as naw
from PyDictionary import PyDictionary

# Set up the path for the Rasa chatbot model
MODEL_PATH = 'models/dialogue/2024-11-15-12-30-00.tar.gz'  # Specify the path to the trained model
dictionary = PyDictionary()

class PDFManager:
    """
    PDF Manager handles PDF file uploads, keyword searches, summarization, and definitions.
    """
    def __init__(self):
        self.pdf_text = ""

    def upload_pdf(self, file_path):
        """Upload and read PDF file."""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            self.pdf_text = text

    def search_keyword(self, keyword):
        """Search for keywords in the PDF text."""
        matches = []
        lines = self.pdf_text.split("\n")
        for line in lines:
            if keyword.lower() in line.lower():
                matches.append(line)
        return matches

    def summarize_pdf(self):
        """Generate a summary of the PDF text."""
        lines = self.pdf_text.split("\n")
        summary = "\n".join(lines[:5])  # Simple summary (first 5 lines)
        return summary

    def get_definition(self, word):
        """Get definition for a word using PyDictionary."""
        definition = dictionary.meaning(word)
        return definition


class RasaChatbot:
    """
    RasaChatbot integrates the Rasa chatbot to handle user interactions.
    """
    def __init__(self, model_path):
        """Initialize the RasaChatbot with the trained model."""
        self.agent = Agent.load(model_path)

    def get_response(self, message):
        """Get the response from the Rasa chatbot for a given message."""
        responses = self.agent.handle_text(message)
        return responses[0]['text'] if responses else "Sorry, I didn't understand that."


class MainWindow(QMainWindow):
    """
    Main window for the PyQt5 application.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF and Chatbot Manager")
        self.setGeometry(100, 100, 800, 600)

        # Create a layout and widgets
        self.layout = QVBoxLayout()
        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.layout.addWidget(self.text_display)

        self.pdf_manager = PDFManager()
        self.chatbot = RasaChatbot(MODEL_PATH)

        # Buttons for PDF actions
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

        # Set the main widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def upload_pdf(self):
        """Handle PDF upload action."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload PDF", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.pdf_manager.upload_pdf(file_path)
            self.text_display.setText(f"Uploaded PDF: {file_path}\n\n{self.pdf_manager.pdf_text[:1000]}...")  # Show a preview

    def summarize_pdf(self):
        """Handle PDF summarization."""
        summary = self.pdf_manager.summarize_pdf()
        self.text_display.setText(f"Summary:\n\n{summary}")

    def search_keyword(self):
        """Handle keyword search in the PDF."""
        keyword, ok = QInputDialog.getText(self, "Search Keyword", "Enter keyword:")
        if ok and keyword:
            matches = self.pdf_manager.search_keyword(keyword)
            if matches:
                self.text_display.setText(f"Keyword matches:\n\n" + "\n".join(matches))
            else:
                self.text_display.setText(f"No matches found for '{keyword}'.")

    def chat_with_bot(self):
        """Handle chat interaction with Rasa chatbot."""
        user_input, ok = QInputDialog.getText(self, "Chat with Bot", "You:")
        if ok and user_input:
            bot_response = self.chatbot.get_response(user_input)
            self.text_display.setText(f"You: {user_input}\nBot: {bot_response}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
