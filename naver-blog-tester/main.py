from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.parse
import json
import time

def get_search_url(keyword, page):
    base_url = "https://section.blog.naver.com/Search/Post.naver"
    encoded_keyword = urllib.parse.quote(keyword)
    return f"{base_url}?pageNo={page}&rangeType=ALL&orderBy=recentdate&keyword={encoded_keyword}"

def extract_blog_content(driver, url):
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # 블로그 iframe 안에 실제 본문이 있는 경우 대응
        frame = driver.find_elements(By.CSS_SELECTOR, "iframe#mainFrame")
        if frame:
            driver.switch_to.frame(frame[0])
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, "html.parser")

        # 본문 추출: Naver 블로그 구조에 따라 다양한 케이스 대응
        content_div = soup.select_one("div.se-main-container") or \
                      soup.select_one("div#postViewArea") or \
                      soup.select_one("div#contentArea")

        if content_div:
            return content_div.get_text(separator="\n").strip()
        else:
            return "(본문을 찾을 수 없습니다)"
    except Exception as e:
        return f"(오류 발생: {e})"

def crawl_naver_blog(keyword, max_pages=1):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    results = []

    try:
        for page in range(1, max_pages + 1):
            url = get_search_url(keyword, page)
            print(f"🔎 Crawling page {page} ...")
            driver.get(url)
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            blog_cards = soup.select("div.list_search_post > div")

            for card in blog_cards:
                link_tag = card.select_one("a.desc_inner")
                if link_tag:
                    link = link_tag["href"]
                    title = link_tag.text.strip()
                    print(f"  → 블로그 수집 중: {title}")
                    content = extract_blog_content(driver, link)
                    results.append({
                        "title": title,
                        "url": link,
                        "content": content
                    })
    finally:
        driver.quit()

    return results

if __name__ == "__main__":
    keyword = input("검색할 키워드를 입력하세요 (예: 연애): ").strip()
    pages = int(input("크롤링할 페이지 수를 입력하세요 (예: 3): "))
    data = crawl_naver_blog(keyword, pages)

    filename = f"naver_blog_{keyword}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {len(data)}개의 블로그 글이 '{filename}' 파일로 저장되었습니다.")
