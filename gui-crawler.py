import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.parse
import requests
import time
import random

class UnifiedCrawlerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("통합 크롤러 - 네이버 블로그 & PANN NATE & 디시인사이드")
        self.root.geometry("700x600")
        
        # 플랫폼 선택
        platform_frame = ttk.Frame(root)
        platform_frame.pack(pady=10)
        
        ttk.Label(platform_frame, text="플랫폼 선택:").pack(side=tk.LEFT, padx=5)
        self.platform_var = tk.StringVar(value="naver_blog")
        
        ttk.Radiobutton(platform_frame, text="네이버 블로그", 
                       variable=self.platform_var, value="naver_blog").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(platform_frame, text="PANN NATE", 
                       variable=self.platform_var, value="pann_nate").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(platform_frame, text="디시인사이드", 
                       variable=self.platform_var, value="dcinside").pack(side=tk.LEFT, padx=10)
        
        # 키워드 입력
        ttk.Label(root, text="검색 키워드:").pack(pady=5)
        self.keyword_entry = ttk.Entry(root, width=40)
        self.keyword_entry.pack(pady=5)
        
        # 페이지 수 입력
        ttk.Label(root, text="크롤링할 페이지 수:").pack(pady=5)
        self.pages_entry = ttk.Entry(root, width=10)
        self.pages_entry.insert(0, "3")
        self.pages_entry.pack(pady=5)
        
        # 시작 버튼
        self.start_btn = ttk.Button(root, text="크롤링 시작", command=self.start_crawling)
        self.start_btn.pack(pady=10)
        
        # 진행률 표시
        self.progress = ttk.Progressbar(root, mode='indeterminate')
        self.progress.pack(pady=5, fill='x', padx=20)
        
        # 상태 표시
        self.status_label = ttk.Label(root, text="대기 중...")
        self.status_label.pack(pady=5)
        
        # 결과 표시
        ttk.Label(root, text="크롤링 결과:").pack(pady=(20,5))
        self.result_text = scrolledtext.ScrolledText(root, height=20, width=80)
        self.result_text.pack(pady=5, padx=20, fill='both', expand=True)
        
        # 저장 버튼
        self.save_btn = ttk.Button(root, text="JSON 파일로 저장", command=self.save_results, state='disabled')
        self.save_btn.pack(pady=5)
        
        self.results = []
    
    def crawl_naver_blog(self, keyword, max_pages=1):
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
                
                driver.get(url)
                time.sleep(3)

                soup = BeautifulSoup(driver.page_source, "html.parser")
                blog_cards = soup.select("div.list_search_post > div")
                print(f"Found {len(blog_cards)} blog cards on page {page}")

                for card in blog_cards:
                    link_tag = card.select_one("a.desc_inner")
                    if link_tag:
                        link = link_tag["href"]
                        title = link_tag.text.strip()
                        
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

    def crawl_pann_nate(self, keyword, max_pages=1):
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
                
                driver.get(url)
                time.sleep(3)
                
                soup = BeautifulSoup(driver.page_source, "html.parser")
                post_links = soup.select("a.subject")
                print(f"Found {len(post_links)} posts on page {page}")
                
                for link in post_links:
                    title = link.text.strip()
                    post_url = "https://pann.nate.com" + link["href"]
                    
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

    def crawl_dcinside(self, keyword, max_pages=1):
        results = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for page in range(1, max_pages + 1):
            params = {
                'id': 'loveconsultation',
                'exception_mode': 'recommend',
                'page': page,
            }
            
            try:
                response = requests.get("https://gall.dcinside.com/board/lists/", params=params, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                posts = soup.select('tr.ub-content') or soup.select('.gall_list tbody tr')
                print(f"Found {len(posts)} posts on page {page}")
                
                for post in posts:
                    title_elem = post.select_one('.gall_tit a') or post.select_one('td a')
                    if title_elem and title_elem.get_text(strip=True):
                        title = title_elem.get_text(strip=True)
                        href = title_elem.get('href', '')
                        if href:
                            link = "https://gall.dcinside.com" + href if href.startswith('/') else href
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
    
    def start_crawling(self):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showerror("오류", "키워드를 입력해주세요.")
            return
        
        try:
            pages = int(self.pages_entry.get())
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("오류", "올바른 페이지 수를 입력해주세요.")
            return
        
        platform = self.platform_var.get()
        
        self.start_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.progress.start()
        
        platform_names = {
            "naver_blog": "네이버 블로그",
            "pann_nate": "PANN NATE",
            "dcinside": "디시인사이드"
        }
        self.status_label.config(text=f"{platform_names[platform]} 크롤링 중...")
        self.result_text.delete(1.0, tk.END)
        
        # 별도 스레드에서 크롤링 실행
        thread = threading.Thread(target=self.crawl_worker, args=(platform, keyword, pages))
        thread.daemon = True
        thread.start()
    
    def crawl_worker(self, platform, keyword, pages):
        try:
            if platform == "naver_blog":
                self.results = self.crawl_naver_blog(keyword, pages)
            elif platform == "pann_nate":
                self.results = self.crawl_pann_nate(keyword, pages)
            else:
                self.results = self.crawl_dcinside(keyword, pages)
            
            self.root.after(0, self.crawling_complete)
        except Exception as e:
            self.root.after(0, lambda: self.crawling_error(str(e)))
    
    def crawling_complete(self):
        self.progress.stop()
        self.start_btn.config(state='normal')
        self.save_btn.config(state='normal')
        
        platform = self.platform_var.get()
        platform_names = {
            "naver_blog": "네이버 블로그",
            "pann_nate": "PANN NATE",
            "dcinside": "디시인사이드"
        }
        self.status_label.config(text=f"완료! {platform_names[platform]}에서 {len(self.results)}개의 글을 수집했습니다.")
        
        # 결과 표시
        self.result_text.delete(1.0, tk.END)
        for i, result in enumerate(self.results, 1):
            self.result_text.insert(tk.END, f"{'='*80}\n")
            self.result_text.insert(tk.END, f"[{i}] {result['title']}\n")
            self.result_text.insert(tk.END, f"플랫폼: {result['source']}\n")
            self.result_text.insert(tk.END, f"URL: {result['url']}\n")
            self.result_text.insert(tk.END, f"{'─'*80}\n")
            content_preview = result['content'][:300].replace('\n', ' ') + '...' if len(result['content']) > 300 else result['content']
            self.result_text.insert(tk.END, f"{content_preview}\n\n")
    
    def crawling_error(self, error_msg):
        self.progress.stop()
        self.start_btn.config(state='normal')
        self.status_label.config(text="오류 발생")
        messagebox.showerror("크롤링 오류", f"오류가 발생했습니다: {error_msg}")
    
    def save_results(self):
        if not self.results:
            messagebox.showwarning("경고", "저장할 데이터가 없습니다.")
            return
        
        keyword = self.keyword_entry.get().strip()
        platform = self.platform_var.get()
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"{platform}_{keyword}.json"
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(self.results, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("저장 완료", f"파일이 저장되었습니다: {filename}")
            except Exception as e:
                messagebox.showerror("저장 오류", f"파일 저장 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedCrawlerGUI(root)
    root.mainloop()