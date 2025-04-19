from flask import Flask, render_template, request, jsonify
from converter import python_to_mermaid
import google.generativeai as genai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_code_explanation(code):
    """Helper function to get explanation from Gemini"""
    prompt = f"""Explain this Python code clearly and concisely:
    
    {code}

    Provide:
    1. What the code does
    2. Key functions/variables
    3. The logical flow
    4. Example use case if applicable"""
    
    response = model.generate_content(prompt)
    return response.text

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    mermaid_code = ""
    explanation = ""
    
    if request.method == "POST":
        code = request.form["code"]
        mermaid_code = python_to_mermaid(code)
        explanation = get_code_explanation(code)  # Generate explanation
        
    return render_template(
        "index.html", 
        code=code, 
        mermaid_code=mermaid_code,
        explanation=explanation
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
