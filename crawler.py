import requests
from bs4 import BeautifulSoup

def get_government_news(query):
    if "행안부" in query or "행정안전부" in query:
        return crawl_mois_press()
    elif "지원금" in query or "공모사업" in query or "축제" in query:
        return crawl_korea_government()
    else:
        return [{"title": "지원 가능한 정보를 찾지 못했습니다.", "date": "", "link": ""}]

def crawl_mois_press():
    url = "https://www.mois.go.kr/frt/bbs/type001/commonSelectBoardList.do?bbsId=BBSMSTR_000000000012"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".board_list tbody tr")

    results = []
    for item in items[:5]:
        title = item.select_one("td.title a").text.strip()
        link = "https://www.mois.go.kr" + item.select_one("td.title a")["href"]
        date = item.select("td")[-1].text.strip()
        results.append({"title": title, "date": date, "link": link})
    return results

def crawl_korea_government():
    url = "https://www.korea.kr/news/pressReleaseList.do"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".list01 li")

    results = []
    for item in items[:5]:
        title = item.select_one("a").text.strip()
        link = "https://www.korea.kr" + item.select_one("a")["href"]
        date = item.select_one(".date").text.strip()
        results.append({"title": title, "date": date, "link": link})
    return results

