from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from collections import Counter

# Import DFA
from dfa import run_dfa

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")
    
    if not text.strip():
        return jsonify({"error": "No text provided"}), 400
    
    # Call DFA
    result = run_dfa(text)
    
    # Format response for frontend
    matches = result["matches"]
    total = result["count"]
    status = "ACCEPTED" if total > 0 else "REJECTED"
    
    # Calculate counts per word
    word_counts = Counter(m["lower"] for m in matches)
    counts = [{"word": w, "count": c} for w, c in word_counts.most_common()]
    
    response = {
        "status": status,
        "total": total,
        "matches": matches,
        "trace": result["trace"],
        "counts": counts
    }
    
    return jsonify(response)

if __name__ == "__main__":
    print("Starting Stop Words DFA server at http://localhost:5000")
    app.run(debug=True, port=5000)