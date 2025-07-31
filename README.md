Local Summarizer AI

A local-first document summarization tool that processes .pdf or .txt files using a locally running LLM through Ollama. It returns concise summaries in PDF or TXT format — securely, privately, and entirely offline.
Features

    Upload .pdf or .txt files

    Summarize with a local LLM (LLaMA 3, Mistral, etc.)

    Control temperature (creativity level)

    Choose between TXT and PDF output

    Secure, offline-only processing

    Simple HTML frontend for upload and configuration

Folder Structure

local-summarizer-ai/
├── app/
│ ├── fonts/
│ │ └── DejaVuSans/ttf/DejaVuSans.ttf
│ ├── templates/
│ │ └── index.html
│ └── main.py
├── storage/
│ ├── uploads/
│ ├── summaries/
│ └── exports/
├── requirements.txt
└── README.md
Getting Started
1. Clone the Repository

git clone https://github.com/aagiato/local-summarizer-ai.git
cd local-summarizer-ai
2. (Recommended) Create a Virtual Environment

python -m venv venv
source venv/bin/activate (on Windows: venv\Scripts\activate)
3. Install Dependencies

pip install -r requirements.txt
4. Install and Run Ollama

Download from https://ollama.com and install for your OS.
Then run:

ollama serve
ollama run llama3

Optional: preload other models like mistral, qwen, or deepseek.
5. Run the Flask App

python app/main.py

Then visit:
http://localhost:5000
Usage

    Upload a .pdf or .txt file

    Choose a model (llama3, mistral, etc.)

    Set temperature (creativity level)

    Choose output format: TXT, PDF, or both

    Click Summarize

    Download your result once processing completes

requirements.txt

Flask==2.3.2
requests==2.31.0
PyMuPDF==1.23.7
fpdf==1.7.2

To install manually:
pip install Flask requests PyMuPDF fpdf
Notes

    Ensure Ollama is running at http://localhost:11434

    Ensure the model (e.g., llama3) is installed and active

    Exported PDFs are stored in storage/exports/

    JSON summaries are saved in storage/summaries/

    Fonts for PDF export are stored in app/fonts/DejaVuSans/ttf/

License

MIT License