import os
import fitz  # PyMuPDF for PDFs
from docx import Document  # For DOCX extraction
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Configure Google Gemini API Key
genai.configure(api_key="your api key")

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-pro-latest")


def extract_text(file_path):
    """Extract text from PDF or DOCX resume files."""
    text = ""

    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text("text") + "\n"

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text.strip()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"})

        file = request.files["resume"]
        if file.filename == "":
            return jsonify({"error": "No selected file"})

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Extract text from resume
        resume_text = extract_text(file_path)

        if not resume_text or resume_text.strip() == "":
            return jsonify({"error": "Could not extract text. Try another file."})

        # AI Prompt for Resume Analysis
        prompt = f"""
        You are an AI Resume Evaluator. Analyze the resume below and provide a structured, concise review.

        RESUME CONTENT:
        {resume_text}  

        PROVIDE A REVIEW IN THE FOLLOWING FORMAT:
        
        KEY STRENGTHS:
        - Point 1
        - Point 2
        - Point 3
        - Point 4
        
        AREAS FOR IMPROVEMENT:
        - Point 1
        - Point 2
        - Point 3
        - Point 4
        
        ACTIONABLE SUGGESTIONS:
        - Point 1
        - Point 2
        - Point 3
        - Point 4

        GUIDELINES:
        - Use short, crisp points (avoid long paragraphs).
        - Keep responses structured and minimal.
        - Do not use asterisks ** or extra spacing.

        Now, generate a structured review:
        """

        try:
            response = model.generate_content(prompt)
            result = response.text

            # Ensure proper formatting with newlines for readability
            formatted_result = result.replace("KEY STRENGTHS:", "\nKEY STRENGTHS:\n") \
                                     .replace("AREAS FOR IMPROVEMENT:", "\nAREAS FOR IMPROVEMENT:\n") \
                                     .replace("ACTIONABLE SUGGESTIONS:", "\nACTIONABLE SUGGESTIONS:\n")

        except Exception as e:
            formatted_result = f"Error processing AI response: {e}"

        return jsonify({"result": formatted_result})

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
