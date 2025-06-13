from flask import Flask, request, jsonify
from flask_cors import CORS
from crawler import get_government_news

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data.get("message", "").strip()
        if not query:
            return jsonify({"success": False, "message": "질문이 비어 있습니다."}), 400

        results = get_government_news(query)
        return jsonify({"success": True, "results": results})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

