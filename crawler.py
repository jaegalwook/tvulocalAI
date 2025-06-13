# crawler.py
import requests
from bs4 import BeautifulSoup

def crawl_mois_press():
    url = "https://www.mois.go.kr/frt/bbs/type001/commonSelectBoardList.do?bbsId=BBSMSTR_000000000014"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    result = []
    for item in soup.select(".bbs_default tbody tr")[:5]:  # 최신 5건
        title = item.select_one("td.subject a").text.strip()
        link = "https://www.mois.go.kr" + item.select_one("td.subject a")["href"]
        date = item.select("td")[-1].text.strip()
        result.append({
            "title": title,
            "link": link,
            "date": date
        })

    return result
