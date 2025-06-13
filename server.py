# backend/server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from crawler import crawl_government_data
import openai
import os

app = Flask(__name__)
CORS(app)

# OpenAI API 키 (환경변수로 설정)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Step 1: 크롤링
    crawled_items = crawl_government_data(user_message)

    if not crawled_items:
        return jsonify({"response": "관련된 정보를 찾지 못했습니다."})

    # Step 2: GPT 요약 요청
    summary_prompt = "다음은 정부 지원금/공모사업 관련 정보입니다. 각 항목은 제목, 요약, 날짜, 링크를 포함하여 간결하고 자연스럽게 설명해주세요:\n\n"

    for item in crawled_items:
        summary_prompt += f"- 제목: {item['title']}\n  내용: {item['desc']}\n  날짜: {item['date']}\n  링크: {item['link']}\n\n"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 정부 정보 요약 챗봇이야."},
            {"role": "user", "content": summary_prompt}
        ],
        temperature=0.7
    )

    gpt_output = response['choices'][0]['message']['content']
    return jsonify({"response": gpt_output})

if __name__ == "__main__":
    app.run(debug=True)
