import os
from flask import Flask, render_template, request
import google.generativeai as genai
from flask_cors import CORS
from converter import python_to_mermaid

app = Flask(__name__)
CORS(app)

# Configure Gemini - Updated for 2.0 Flash
try:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated for Flash model
    print("✅ Gemini 2.0 Flash configured successfully")
except Exception as e:
    print(f"Gemini config failed: {str(e)}")
    model = None

@app.route("/", methods=["GET", "POST"])
def index():
    code = mermaid_code = explanation = ""
    
    if request.method == "POST":
        code = request.form.get("code", "")
        mermaid_code = python_to_mermaid(code)
        
        if model and code.strip():
    try:
        prompt = f"""Analyze this Python code and provide a well-structured explanation:

        {code}

        Format your response EXACTLY as follows:

        [Purpose]
        <1-2 sentence description>

        [Key Components]
        • <component 1> - <description>
        • <component 2> - <description>
        • <component 3> - <description>

        [Execution Flow]
        1. <step 1>
        2. <step 2>
        3. <step 3>

        [Example]
        • Input: <sample input>
        • Output: <expected output>"""
        
        response = model.generate_content(prompt)
        explanation = response.text
            except Exception as e:
                explanation = f"⚠️ Explanation error: {str(e)}"

    return render_template("index.html",
        code=code,
        mermaid_code=mermaid_code,
        explanation=explanation
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 10000)))
