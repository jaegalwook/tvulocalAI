from flask import Flask, request, jsonify
from flask_cors import CORS
from crawler import crawl_press_release

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"answer": "질문이 비어 있습니다."})

        # 크롤링 실행
        result = crawl_press_release(user_message)
        return jsonify({"answer": result})
    except Exception as e:
        return jsonify({"answer": f"오류 발생: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
