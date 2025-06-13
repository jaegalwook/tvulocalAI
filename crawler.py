import requests
from bs4 import BeautifulSoup

# 부처명과 URL 매핑
PRESS_URLS = {
    "행안부": "https://www.mois.go.kr/frt/bbs/type001/commonSelectBoardList.do?bbsId=BBSMSTR_000000000014",
    "복지부": "https://www.mohw.go.kr/react/al/sal0301ls.jsp?PAR_MENU_ID=04&MENU_ID=0403",
    "국토부": "https://www.molit.go.kr/USR/BORD0201/m_69/list.do?bbsId=BBSMSTR_000000000023",
    "문체부": "https://www.mcst.go.kr/kor/s_notice/press/pressList.jsp",
    "환경부": "https://www.me.go.kr/home/web/board/list.do?menuId=10392",
}

def extract_ministry_name(user_input):
    for keyword in PRESS_URLS:
        if keyword in user_input:
            return keyword
    return None

def crawl_press_release(user_input):
    ministry = extract_ministry_name(user_input)
    if not ministry:
        return "지원하는 부처명을 찾을 수 없습니다. 예: '행안부 보도자료 보여줘'"

    url = PRESS_URLS[ministry]
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # 부처별 HTML 구조에 맞춰 커스터마이징 필요
        # 여기서는 행안부(mois.go.kr) 구조 기준 예시
        items = soup.select("table tbody tr")[:5]

        results = []
        for row in items:
            title_tag = row.select_one("td.subject a")
            date_tag = row.select_one("td.date")
            if not title_tag:
                continue
            title = title_tag.text.strip()
            link = "https://www.mois.go.kr" + title_tag.get("href")
            date = date_tag.text.strip() if date_tag else "날짜 없음"
            results.append(f"📌 {title}\n🕒 {date}\n🔗 {link}")

        return "\n\n".join(results) if results else "보도자료를 찾을 수 없습니다."
    except Exception as e:
        return f"크롤링 중 오류 발생: {str(e)}"
