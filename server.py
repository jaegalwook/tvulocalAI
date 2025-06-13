from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 접근 허용

@app.route('/')
def index():
    return "TVU 정부 크롤러 API가 실행 중입니다."

@app.route('/crawl', methods=['POST'])
def crawl():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'success': False, 'message': 'URL이 제공되지 않았습니다.'}), 400

        # HTML 크롤링 (예시: korea.kr 보도자료 페이지)
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []

        for li in soup.select('ul.list li'):
            title_tag = li.select_one('.tit') or li.select_one('a')
            date_tag = li.select_one('.date') or li.select_one('span.date')

            title = title_tag.text.strip() if title_tag else '제목 없음'
            link = title_tag.get('href') if title_tag else '#'
            if link and not link.startswith('http'):
                link = f'https://www.korea.kr{link}'

            date = date_tag.text.strip() if date_tag else '날짜 없음'

            results.append({
                '제목': title,
                '링크': link,
                '날짜': date
            })

        return jsonify({'success': True, 'data': results})

    except Exception as e:
        return jsonify({'success': False, 'message': f'서버 오류: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render가 자동 지정한 포트 사용
    app.run(host='0.0.0.0', port=port)
