import requests
from bs4 import BeautifulSoup

def crawl_mois_press():
    url = "https://www.mois.go.kr/frt/bbs/type001/commonSelectBoardList.do?bbsId=BBSMSTR_000000000012"
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".board_list tbody tr")

    results = []
    for item in items[:5]:  # 최근 5개만
        title_tag = item.select_one("td.title a")
        if not title_tag:
            continue
        title = title_tag.text.strip()
        link = "https://www.mois.go.kr" + title_tag["href"]
        date = item.select("td")[-1].text.strip()
        results.append({"title": title, "date": date, "link": link})
    return results

def get_government_news(query):
    try:
        if "행안부" in query or "행정안전부" in query or "보도자료" in query:
            return crawl_mois_press()
        else:
            return [{"title": "지원되는 검색이 아닙니다", "date": "", "link": ""}]
    except Exception as e:
        return [{"title": "크롤링 중 오류", "date": "", "link": str(e)}]
