# Document Summary Assistant

A web application that generates concise summaries from text and PDF documents using advanced NLP techniques. This tool helps users quickly extract key information from large documents, improving productivity and comprehension.

**Live Demo:** [Access the app here](https://document-summary-assistant-fh2d.onrender.com)

---

## Features

- **Upload PDF or Text Documents:** Easily upload your documents in PDF or text format.
- **OCR for Scanned PDFs:** Extract text from scanned PDFs using `pytesseract`.
- **Automatic Text Summarization:** Generate summaries using NLP algorithms like LexRank and LSA (Latent Semantic Analysis).
- **Clean Interface:** User-friendly web interface built with HTML, CSS, and JavaScript.
- **Multi-format Support:** Works with plain text, scanned PDFs, and standard PDFs.

---

## Tech Stack

- **Backend:** Python, Flask
- **Libraries:** PyPDF2, pytesseract, NLTK, Sumy
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render

---

## Installation (Local Setup)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/samatha-26/document-summary-assistant.git
   cd document-summary-assistant
2.Create a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


3.Install dependencies:

pip install -r requirements.txt


4.Run the application locally:

python app.py


5.Open your browser and go to http://127.0.0.1:5000.

Deployment

The app is deployed on Render and can be accessed using the link above. Render handles hosting, SSL, and scalability automatically.

Usage

Upload a PDF or text file.

Wait for the app to process the document.

View or copy the generated summary.

Repeat for multiple documents.

Contributing

Fork the repository.

Create a new branch (git checkout -b feature-name).

Make your changes and commit (git commit -m 'Add feature').

Push to the branch (git push origin feature-name).

Open a Pull Request.


