# backend/crawler.py
import requests
from bs4 import BeautifulSoup

def crawl_government_data(user_message):
    """
    user_message에서 키워드를 추출하여 관련 정부 사이트에서 크롤링 수행
    현재는 korea.kr 보도자료 목록에서 관련 키워드를 검색
    """
    base_url = "https://www.korea.kr/news/pressReleaseList.do"
    search_url = f"https://www.korea.kr/news/pressReleaseList.do?searchWord={user_message}"

    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("크롤링 요청 오류:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    # 보도자료 목록 가져오기
    ul = soup.find("ul", class_="list type01")
    if not ul:
        return []

    for li in ul.find_all("li")[:5]:  # 최대 5개 항목
        try:
            title_tag = li.find("a")
            title = title_tag.get_text(strip=True)
            link = "https://www.korea.kr" + title_tag["href"]
            desc = li.find("p").get_text(strip=True)
            date = li.find("span", class_="date").get_text(strip=True)

            items.append({
                "title": title,
                "desc": desc,
                "date": date,
                "link": link
            })
        except Exception as e:
            print("항목 파싱 실패:", e)
            continue

    return items
