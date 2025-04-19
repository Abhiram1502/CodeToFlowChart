import os
from flask import Flask, render_template, request
import google.generativeai as genai
from flask_cors import CORS
from converter import python_to_mermaid

app = Flask(__name__)
CORS(app)

# Configure Gemini - will use Render's environment variables
try:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    print(f"Gemini init error: {str(e)}")
    model = None

@app.route("/", methods=["GET", "POST"])
def index():
    code = mermaid_code = explanation = ""
    
    if request.method == "POST":
        code = request.form.get("code", "")
        mermaid_code = python_to_mermaid(code)
        
        if model and code.strip():
            try:
                response = model.generate_content(
                    f"Explain this Python code:\n\n{code}\n\n"
                    "Focus on:\n1. Purpose\n2. Key components\n3. Flow"
                )
                explanation = response.text
            except Exception as e:
                explanation = f"Explanation error: {str(e)}"

    return render_template("index.html",
        code=code,
        mermaid_code=mermaid_code,
        explanation=explanation
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 10000)))
