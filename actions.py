from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from mymemory_translator import MyMemoryTranslator
from nlpaug_rephraser import NLPAugRephraser
from pdf_manager import PDFManager

class ActionTranslate(Action):
    def name(self) -> str:
        return "action_translate"

    def __init__(self):
        self.translator = MyMemoryTranslator()

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        text_to_translate = tracker.get_slot('text_to_translate')
        target_language = tracker.get_slot('target_language')

        if text_to_translate and target_language:
            translated_text = self.translator.translate(text_to_translate, 'en', target_language)
            dispatcher.utter_message(text=f"Translated Text: {translated_text}")
            return [SlotSet("translated_text", translated_text)]
        else:
            dispatcher.utter_message(text="Sorry, I couldn't translate that text.")
            return []

class ActionRephrase(Action):
    def name(self) -> str:
        return "action_rephrase"

    def __init__(self):
        self.rephraser = NLPAugRephraser()

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        text_to_rephrase = tracker.get_slot('text_to_rephrase')

        if text_to_rephrase:
            rephrased_text = self.rephraser.rephrase(text_to_rephrase)
            dispatcher.utter_message(text=f"Rephrased Text: {rephrased_text}")
            return [SlotSet("rephrased_text", rephrased_text)]
        else:
            dispatcher.utter_message(text="Sorry, I couldn't rephrase that text.")
            return []

class ActionSummarizePDF(Action):
    def name(self) -> str:
        return "action_summarize_pdf"

    def __init__(self):
        self.pdf_manager = PDFManager()

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        pdf_path = tracker.get_slot('pdf_path')

        if pdf_path:
            summary = self.pdf_manager.summarize_pdf(pdf_path)
            dispatcher.utter_message(text=f"Summary of the PDF: {summary}")
            return [SlotSet("pdf_summary", summary)]
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the PDF to summarize.")
            return []
