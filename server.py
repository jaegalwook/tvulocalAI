from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route("/crawl", methods=["POST"])
def crawl():
    url = request.json.get("url")
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []
        for item in soup.select('.list_item')[:5]:  # 예: 최근 5개
            title = item.select_one('a').text.strip()
            link = item.select_one('a')['href']
            date = item.select_one('.date').text.strip()

            # AI 요약 요청
            prompt = f"다음 정부 보도자료 제목을 간단히 요약하세요:\n제목: {title}"
            ai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
            )
            summary = ai_response.choices[0].message.content.strip()

            results.append({
                "title": title,
                "date": date,
                "link": link,
                "summary": summary
            })
        return jsonify(success=True, data=results)
    except Exception as e:
        return jsonify(success=False, message=str(e))

if __name__ == "__main__":
    app.run()
