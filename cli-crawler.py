from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.parse
import requests
import json
import time
import random

def crawl_naver_blog(keyword, max_pages=1):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    results = []

    try:
        for page in range(1, max_pages + 1):
            base_url = "https://section.blog.naver.com/Search/Post.naver"
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"{base_url}?pageNo={page}&rangeType=ALL&orderBy=recentdate&keyword={encoded_keyword}"
            
            print(f"🔎 Crawling Naver Blog page {page} ...")
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
                    
                    try:
                        driver.get(link)
                        time.sleep(2)
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        
                        frame = driver.find_elements(By.CSS_SELECTOR, "iframe#mainFrame")
                        if frame:
                            driver.switch_to.frame(frame[0])
                            time.sleep(2)
                            soup = BeautifulSoup(driver.page_source, "html.parser")

                        content_div = soup.select_one("div.se-main-container") or \
                                      soup.select_one("div#postViewArea") or \
                                      soup.select_one("div#contentArea")

                        content = content_div.get_text(separator="\n").strip() if content_div else "(본문을 찾을 수 없습니다)"
                    except Exception as e:
                        content = f"(오류 발생: {e})"
                    
                    results.append({
                        "title": title,
                        "url": link,
                        "content": content,
                        "source": "naver_blog"
                    })
    finally:
        driver.quit()
    return results

def crawl_pann_nate(keyword, max_pages=1):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    results = []
    
    try:
        for page in range(1, max_pages + 1):
            base_url = "https://pann.nate.com/search/talk"
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"{base_url}?searchType=A&q={encoded_keyword}&page={page}"
            
            print(f"🔎 Crawling PANN NATE page {page} ...")
            driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            post_links = soup.select("a.subject")
            
            for link in post_links:
                title = link.text.strip()
                post_url = "https://pann.nate.com" + link["href"]
                print(f"  → 게시글 수집 중: {title}")
                
                try:
                    driver.get(post_url)
                    time.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    
                    content_div = soup.select_one("div.usertxt") or soup.select_one("div.content")
                    content = content_div.get_text(separator="\n").strip() if content_div else "(본문을 찾을 수 없습니다)"
                except Exception as e:
                    content = f"(오류 발생: {e})"
                
                results.append({
                    "title": title,
                    "url": post_url,
                    "content": content,
                    "source": "pann_nate"
                })
    finally:
        driver.quit()
    return results

def crawl_dcinside(keyword, max_pages=1):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for page in range(1, max_pages + 1):
        params = {
            'id': 'loveconsultation',
            'page': page,
            's_type': 'search_subject_memo',
            's_keyword': keyword
        }
        
        try:
            print(f"🔎 Crawling DCInside page {page} ...")
            response = requests.get("https://gall.dcinside.com/board/lists/", params=params, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            posts = soup.select('tr.ub-content') or soup.select('.gall_list tbody tr')
            
            for post in posts:
                title_elem = post.select_one('.gall_tit a') or post.select_one('td a')
                if title_elem and title_elem.get_text(strip=True):
                    title = title_elem.get_text(strip=True)
                    href = title_elem.get('href', '')
                    if href:
                        link = "https://gall.dcinside.com" + href if href.startswith('/') else href
                        print(f"  → 게시글 수집 중: {title}")
                        
                        results.append({
                            'title': title,
                            'url': link,
                            'content': title,
                            'source': 'dcinside'
                        })
            
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"페이지 {page} 크롤링 중 오류: {e}")
            continue
    
    return results

def main():
    print("=== 통합 크롤러 ===")
    print("1. 네이버 블로그")
    print("2. PANN NATE")
    print("3. 디시인사이드")
    
    choice = input("플랫폼을 선택하세요 (1, 2, 또는 3): ").strip()
    keyword = input("검색할 키워드를 입력하세요: ").strip()
    pages = int(input("크롤링할 페이지 수를 입력하세요: "))
    
    if choice == "1":
        data = crawl_naver_blog(keyword, pages)
        platform = "naver_blog"
    elif choice == "2":
        data = crawl_pann_nate(keyword, pages)
        platform = "pann_nate"
    else:
        data = crawl_dcinside(keyword, pages)
        platform = "dcinside"
    
    filename = f"{platform}_{keyword}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {len(data)}개의 글이 '{filename}' 파일로 저장되었습니다.")

if __name__ == "__main__":
    main()