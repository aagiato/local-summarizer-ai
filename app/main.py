import os
import uuid
import json
from datetime import datetime
from flask import Flask, request, render_template, send_file, url_for
from fpdf import FPDF
import fitz  # PyMuPDF for PDF reading
import requests

# === CONFIG ===
UPLOAD_FOLDER = os.path.join("storage", "uploads")
SUMMARY_FOLDER = os.path.join("storage", "summaries")
EXPORT_FOLDER = os.path.join("storage", "exports")
FONT_PATH = os.path.join("app", "fonts", "DejaVuSans", "ttf", "DejaVuSans.ttf")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

app = Flask(__name__)

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        return "\n".join([page.get_text() for page in doc])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def summarize_with_ollama(prompt, model="llama3", temperature=0.3):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
    )
    result = response.json()
    return result.get("response", "[No response from model]")

def export_summary_to_pdf(summary_data, export_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.multi_cell(0, 10, f"Filename: {summary_data['filename']}")
    pdf.multi_cell(0, 10, f"Uploaded At: {summary_data['uploaded_at']}")
    pdf.multi_cell(0, 10, f"Temperature: {summary_data['temperature']}\n")

    for i, s in enumerate(summary_data['summaries'], 1):
        pdf.multi_cell(0, 10, f"--- Summary {i} ---\n{s}\n")

    pdf.output(export_path)
    print(f"[DEBUG] PDF exported to: {export_path}")
    print(f"[DEBUG] File exists? {os.path.exists(export_path)}")

# === ROUTES ===

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        temperature = float(request.form.get("temperature", 0.3))
        model = request.form.get("model", "llama3")

        if file and file.filename.lower().endswith((".pdf", ".txt")):
            filename = f"{uuid.uuid4()}_{file.filename}"
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            text = extract_text(path)
            chunks = text.split("\n\n")
            print(f"[DEBUG] Loaded {len(chunks)} chunks from the document")
            chunks = chunks[:1]  # Limit to just 1 chunk for testing

            summaries = []
            for i, chunk in enumerate(chunks):
                prompt = (
                    "You are an analyst at a venture debt or venture capital firm. "
                    "Summarize the following document chunk in a factual and concise way. "
                    "Include important dates, discoveries, IP, operational processes, and key product information. "
                    "Act without making assumptions.\n\n"
                    f"{chunk}\n\nSummary:"
                )
                print("=== PROMPT SENT TO OLLAMA ===")
                print(prompt)
                summary = summarize_with_ollama(prompt, model=model, temperature=temperature)
                summaries.append(summary)

            summary_data = {
                "filename": file.filename,
                "summaries": summaries,
                "uploaded_at": datetime.utcnow().isoformat(),
                "temperature": temperature,
                "model": model
            }

            output_json = os.path.join(SUMMARY_FOLDER, f"{filename}.json")
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(summary_data, f, indent=2)

            base_name = os.path.splitext(filename)[0]
            output_pdf = os.path.join(EXPORT_FOLDER, f"{base_name}.pdf")
            pdf_link = None
            try:
                os.makedirs(EXPORT_FOLDER, exist_ok=True)
                export_summary_to_pdf(summary_data, output_pdf)
                pdf_link = url_for("download_file", filename=f"{base_name}.pdf")
            except Exception as e:
                print(f"[ERROR] PDF export failed: {e}")
                pdf_link = None

            return render_template("index.html", summary=summary_data, done=True, txt_link=None, pdf_link=pdf_link)

    return render_template("index.html", done=False)

@app.route("/download/<filename>")
def download_file(filename):
    filepath = os.path.abspath(os.path.join(EXPORT_FOLDER, filename))
    return send_file(filepath, as_attachment=True)

# === MAIN ENTRY ===
if __name__ == "__main__":
    app.run(debug=True)
