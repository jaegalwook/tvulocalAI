from flask import Flask, request, jsonify
from flask_cors import CORS
from crawler import crawl_government_info

app = Flask(__name__)
CORS(app)  # CORS 허용 (프론트엔드에서 접근 가능하게)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"answer": "질문이 비어 있습니다."})

        # 크롤링 함수 호출
        result = crawl_government_info(user_message)

        return jsonify({"answer": result})
    except Exception as e:
        return jsonify({"answer": f"오류 발생: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)