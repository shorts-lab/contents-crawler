import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import logging
from ..crawlers import NaverCrawler, PannCrawler, DCInsideCrawler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CrawlerGUI:
    """GUI interface for the crawler"""
    def __init__(self, root):
        self.root = root
        self.root.title("통합 크롤러 - 네이버 블로그 & PANN NATE & 디시인사이드")
        self.root.geometry("700x600")
        
        # 플랫폼 선택
        platform_frame = ttk.Frame(root)
        platform_frame.pack(pady=10)
        
        ttk.Label(platform_frame, text="플랫폼 선택:").pack(side=tk.LEFT, padx=5)
        self.platform_var = tk.StringVar(value="naver")
        
        ttk.Radiobutton(platform_frame, text="네이버 블로그", 
                       variable=self.platform_var, value="naver").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(platform_frame, text="PANN NATE", 
                       variable=self.platform_var, value="pann").pack(side=tk.LEFT, padx=10)
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
    
    def start_crawling(self):
        """Start the crawling process"""
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
            "naver": "네이버 블로그",
            "pann": "PANN NATE",
            "dcinside": "디시인사이드"
        }
        self.status_label.config(text=f"{platform_names[platform]} 크롤링 중...")
        self.result_text.delete(1.0, tk.END)
        
        # 별도 스레드에서 크롤링 실행
        thread = threading.Thread(target=self.crawl_worker, args=(platform, keyword, pages))
        thread.daemon = True
        thread.start()
    
    def crawl_worker(self, platform, keyword, pages):
        """Worker thread for crawling"""
        try:
            if platform == "naver":
                crawler = NaverCrawler(keyword, pages)
            elif platform == "pann":
                crawler = PannCrawler(keyword, pages)
            else:
                crawler = DCInsideCrawler(keyword, pages)
                
            self.results = crawler.crawl()
            self.root.after(0, self.crawling_complete)
        except Exception as e:
            self.root.after(0, lambda: self.crawling_error(str(e)))
    
    def crawling_complete(self):
        """Handle completion of crawling"""
        self.progress.stop()
        self.start_btn.config(state='normal')
        self.save_btn.config(state='normal')
        
        platform = self.platform_var.get()
        platform_names = {
            "naver": "네이버 블로그",
            "pann": "PANN NATE",
            "dcinside": "디시인사이드"
        }
        self.status_label.config(text=f"완료! {platform_names[platform]}에서 {len(self.results)}개의 글을 수집했습니다.")
        
        # 결과 표시
        self.result_text.delete(1.0, tk.END)
        for i, result in enumerate(self.results, 1):
            self.result_text.insert(tk.END, f"{'='*80}\n")
            self.result_text.insert(tk.END, f"[{i}] {result['title']}\n")
            self.result_text.insert(tk.END, f"플랫폼: {result['platform']}\n")
            self.result_text.insert(tk.END, f"URL: {result['url']}\n")
            self.result_text.insert(tk.END, f"{'─'*80}\n")
            content_preview = result['content'][:300].replace('\n', ' ') + '...' if len(result['content']) > 300 else result['content']
            self.result_text.insert(tk.END, f"{content_preview}\n\n")
    
    def crawling_error(self, error_msg):
        """Handle crawling errors"""
        self.progress.stop()
        self.start_btn.config(state='normal')
        self.status_label.config(text="오류 발생")
        messagebox.showerror("크롤링 오류", f"오류가 발생했습니다: {error_msg}")
    
    def save_results(self):
        """Save results to a JSON file"""
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