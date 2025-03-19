from flask import Flask, request, jsonify
import os
from docx import Document

app = Flask(__name__)

# Ensure the uploads directory exists
os.makedirs("uploads", exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = f"uploads/{file.filename}"
    file.save(file_path)

    try:
        # Read the .docx file and search for specific content
        search_results = search_in_docx(file_path, "sustainability")
        return jsonify({"message": "File processed successfully", "results": search_results}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def search_in_docx(file_path, keyword):
    # Open the .docx file
    doc = Document(file_path)
    results = []

    # Search for the keyword in each paragraph
    for i, paragraph in enumerate(doc.paragraphs):
        if keyword.lower() in paragraph.text.lower():
            results.append({
                "paragraph": i + 1,
                "text": paragraph.text.strip()
            })

    return results

if __name__ == "__main__":
    app.run(debug=True)