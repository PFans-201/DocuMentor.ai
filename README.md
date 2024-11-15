# PDF Manager and Rasa Chatbot Integration

This is a PyQt5-based desktop application designed to integrate multiple advanced features, including PDF file management, keyword search, summarization, and chatbot-based assistance. The app also uses the Rasa framework to provide chatbot functionality for user queries, along with natural language processing (NLP) tools for rephrasing and translation.

## App Structure

Here is an overview of the directory structure for the app:

<pre>
    DocuMentor_ai/
├── actions/                          # Custom actions for the chatbot
│   ├── actions.py                    # All actions, including Translate, Rephrase, SummarizePDF, etc.
│   └── utils/                        # Utility functions for actions
│       ├── mymemory_translator.py    # Translator logic using MyMemory API
│       ├── nlpaug_rephraser.py      # Text rephraser using NLP-Augment
│       └── pdf_manager.py           # PDF file management logic
├── data/                             # Training data for the Rasa chatbot
│   ├── nlu.yml                      # NLU training data for Rasa chatbot
│   ├── stories.yml                  # Stories for Rasa dialogue management
│   └── rules.yml                    # Rasa rule-based dialogue handling
├── models/                           # Rasa dialogue models (trained models)
│   └── dialogue/                    # Trained dialogue models
│       └── <model_name>.tar.gz   # Trained Rasa model file
├── config.yml                        # Bot pipeline and policies configuration
├── domain.yml                        # Bot domain configuration
├── endpoints.yml                     # Rasa endpoints for API interaction
├── main.py                           # Main entry point for running the app
└── README.md                         # Documentation for the project
</pre>

## Features

### 1. **PDF File Management**
- **Upload PDFs**: Upload and read PDF files from the local filesystem.
- **Summarize PDFs**: Automatically summarize the contents of PDF files into short summaries.
- **Keyword Search**: Search for keywords or terms within the PDF files and retrieve the matching sentences.
- **Get Definitions**: Retrieve definitions for keywords or concepts using the PyDictionary library.

### 2. **Chatbot Integration with Rasa**
- **Chatbot Responses**: Use `rasa` to interact with users and provide context-based responses to queries related to the PDF content or other topics.
- **Rasa Training**: The app leverages Rasa's NLU (Natural Language Understanding) and dialogue management to respond intelligently to user inputs.

### 3. **Natural Language Processing (NLP) Tools**
- **Text Rephrasing**: Using the `nlpaug` library, the app can rephrase user input to generate alternative wordings for text.
- **Translation**: Translate text between languages using the MyMemory API.

### 4. **User-Friendly GUI with PyQt5**
- **Intuitive UI**: A `PyQt5` interface allows users to upload PDFs, search keywords, get summaries, and interact with the chatbot through a single, simple interface.
- **PDF Summarization**: Display a summary of uploaded PDFs to the user in a concise format.

## Reason for Abandonment

The original goal of this project was to build a chatbot from scratch using Rasa, combined with advanced NLP techniques for processing PDFs and user queries. While the project demonstrated the complexity and power of building a custom solution with Rasa and various NLP tools (such as rephrasing and translation), I realized that there was a more efficient and powerful way to achieve similar results using Large Language Models (LLMs), such as GPT-based models.

### Key Insights:
1. **Building a Chatbot from Scratch is Complex**: While Rasa is a powerful framework for building chatbots, it requires a significant amount of training data, dialogue design, and configuration to make it perform well across a variety of topics.
2. **LLMs for Powerful and Flexible Responses**: Large Language Models (LLMs) like GPT-3 and GPT-4 offer much more power and flexibility with minimal setup. They can understand complex queries and generate contextually rich responses without needing to predefine explicit intents or dialogue flows.
3. **More Efficient Development**: By leveraging LLMs, it's easier to scale the chatbot's capabilities, adapt to different domains, and handle a wider variety of queries without needing to invest as much in the architecture and rule-based systems like Rasa.
4. **Better Resource Utilization**: LLMs like GPT can be fine-tuned on domain-specific data and are capable of processing large amounts of unstructured data, like PDFs, much more effectively than traditional NLP methods.

### Conclusion

Given the significant advancements in LLMs for conversational AI, I decided to abandon this project in favor of exploring LLM-based chatbot solutions that offer more flexibility, scalability, and power, without the need to manually define every possible scenario and dialogue flow. These models can also be used for more advanced applications, such as code generation, creative writing, and decision support, making them a more future-proof choice for building a chatbot.

## Installation and Usage

1. Clone the repository:

    ```bash
    git clone <https://github.com/PFans-201/DocuMentor.ai.git>
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python app.py
    ```

## Dependencies

- PyQt5
- Rasa (for chatbot)
- PyDictionary
- PyPDF2
- nltk
- nlpaug
- requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

