from flask import Flask, request, jsonify
from flask_cors import CORS
from crawler import get_government_news

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        if not data or "message" not in data:
            return jsonify({"success": False, "message": "입력 값이 없습니다."}), 400

        query = data["message"]
        results = get_government_news(query)
        return jsonify({"success": True, "results": results})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

