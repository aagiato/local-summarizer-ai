import os
import uuid
import json
import time
from datetime import datetime
from flask import Flask, request, render_template
from fpdf import FPDF
import fitz             # PyMuPDF
import requests
from prompts import get_summary_prompt, get_label_prompt

# === ABSOLUTE PATHS CONFIG ===
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "storage", "uploads")
SUMMARY_FOLDER= os.path.join(BASE_DIR, "storage", "summaries")
EXPORT_FOLDER = os.path.join(BASE_DIR, "storage", "exports")
FONT_PATH     = os.path.join(BASE_DIR, "fonts", "DejaVuSans", "ttf", "DejaVuSans.ttf")

for d in (UPLOAD_FOLDER, SUMMARY_FOLDER, EXPORT_FOLDER):
    os.makedirs(d, exist_ok=True)

app = Flask(__name__)

# === CORE HELPERS ===
def extract_text(path: str) -> str:
    if path.lower().endswith(".pdf"):
        doc = fitz.open(path)
        return "\n\n".join(page.get_text() for page in doc)
    else:
        return open(path, "r", encoding="utf-8").read()

def summarize_with_ollama(prompt: str, model: str, temperature: float) -> str:
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
    )
    return res.json().get("response", "[no response]")

def export_to_pdf(data: dict, out_path: str):
    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.multi_cell(0,10, f"Filename: {data['filename']}")
    pdf.multi_cell(0,10, f"Label:    {data['label']}")
    pdf.multi_cell(0,10, f"Model:    {data['model']}    Temp: {data['temperature']}")
    pdf.multi_cell(0,10, f"Uploaded: {data['uploaded_at']}\n")

    for idx, s in enumerate(data["summaries"], start=1):
        pdf.multi_cell(0,10, f"--- Summary {idx} ---\n{s}\n")

    pdf.output(out_path)

# === ROUTES ===

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        file        = request.files.get("file")
        temperature = float(request.form.get("temperature", 0.3))
        model       = request.form.get("model", "llama3")
        export_fmt  = request.form.get("export", "both")

        # 1) save upload
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        upload_path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(upload_path)

        # 2) extract + chunk (just first chunk for now)
        full_text = extract_text(upload_path)
        chunk     = full_text.split("\n\n")[0]

        # 3) get label + summary
        label    = summarize_with_ollama(get_label_prompt(chunk),    model, temperature).strip()
        summary  = summarize_with_ollama(get_summary_prompt(chunk),  model, temperature).strip()

        # 4) assemble metadata
        data = {
            "filename":    file.filename,
            "label":       label,
            "summaries":   [summary],
            "model":       model,
            "temperature": temperature,
            "uploaded_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # 5) write JSON record
        json_path = os.path.join(SUMMARY_FOLDER, unique_name + ".json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=2)

        # 6) write TXT + PDF
        base        = os.path.splitext(unique_name)[0]
        txt_path    = os.path.join(EXPORT_FOLDER, f"{base}.txt")
        pdf_path    = os.path.join(EXPORT_FOLDER, f"{base}.pdf")

        # TXT
        with open(txt_path, "w", encoding="utf-8") as tf:
            tf.write(summary)

        # PDF
        export_to_pdf(data, pdf_path)

        # 7) pass back absolute paths
        data["export_paths"] = {
            "txt": txt_path,
            "pdf": pdf_path
        }

        return render_template("index.html", done=True, summary=data)

    # GET
    return render_template("index.html", done=False)


# === LAUNCH ===
if __name__ == "__main__":
    app.run(debug=True)
