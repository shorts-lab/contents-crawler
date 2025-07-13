from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.parse
import json
import time

def get_search_url(keyword, page=1):
    base_url = "https://pann.nate.com/search/talk"
    encoded_keyword = urllib.parse.quote(keyword)
    return f"{base_url}?searchType=A&q={encoded_keyword}&page={page}"

def extract_post_content(driver, url):
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        content_div = soup.select_one("div.usertxt") or soup.select_one("div.content")
        if content_div:
            return content_div.get_text(separator="\n").strip()
        return "(본문을 찾을 수 없습니다)"
    except Exception as e:
        return f"(오류 발생: {e})"

def crawl_pann_nate(keyword, max_pages=1):
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
            post_links = soup.select("a.subject")
            
            for link in post_links:
                title = link.text.strip()
                post_url = "https://pann.nate.com" + link["href"]
                print(f"  → 게시글 수집 중: {title}")
                content = extract_post_content(driver, post_url)
                results.append({
                    "title": title,
                    "url": post_url,
                    "content": content
                })
    finally:
        driver.quit()
    
    return results

if __name__ == "__main__":
    keyword = input("검색할 키워드를 입력하세요 (예: 연애): ").strip()
    pages = int(input("크롤링할 페이지 수를 입력하세요 (예: 3): "))
    data = crawl_pann_nate(keyword, pages)
    
    filename = f"pann_nate_{keyword}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {len(data)}개의 게시글이 '{filename}' 파일로 저장되었습니다.")