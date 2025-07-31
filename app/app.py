from flask import Flask, request, render_template, send_file
import os
from .load_and_chunk import load_and_chunk_document
from .send_to_claud import summarize_chunks_bedrock

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            chunks = load_and_chunk_document(filepath)
            summaries = summarize_chunks_bedrock(chunks)

            output_path = os.path.join(UPLOAD_FOLDER, "summaries_output.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                for i, summary in enumerate(summaries, 1):
                    f.write(f"\n--- Summary for Chunk {i} ---\n{summary}\n")

            return send_file(output_path, as_attachment=True)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
