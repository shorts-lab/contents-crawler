import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
from main import crawl_naver_blog

class NaverBlogCrawlerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("네이버 블로그 크롤러")
        self.root.geometry("600x500")
        
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
        self.result_text = scrolledtext.ScrolledText(root, height=15, width=70)
        self.result_text.pack(pady=5, padx=20, fill='both', expand=True)
        
        # 저장 버튼
        self.save_btn = ttk.Button(root, text="JSON 파일로 저장", command=self.save_results, state='disabled')
        self.save_btn.pack(pady=5)
        
        self.results = []
    
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
        
        self.start_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="크롤링 중...")
        self.result_text.delete(1.0, tk.END)
        
        # 별도 스레드에서 크롤링 실행
        thread = threading.Thread(target=self.crawl_worker, args=(keyword, pages))
        thread.daemon = True
        thread.start()
    
    def crawl_worker(self, keyword, pages):
        try:
            self.results = crawl_naver_blog(keyword, pages)
            self.root.after(0, self.crawling_complete)
        except Exception as e:
            self.root.after(0, lambda: self.crawling_error(str(e)))
    
    def crawling_complete(self):
        self.progress.stop()
        self.start_btn.config(state='normal')
        self.save_btn.config(state='normal')
        self.status_label.config(text=f"완료! {len(self.results)}개의 블로그 글을 수집했습니다.")
        
        # 결과 표시
        self.result_text.delete(1.0, tk.END)
        for i, result in enumerate(self.results, 1):
            self.result_text.insert(tk.END, f"{'='*60}\n")
            self.result_text.insert(tk.END, f"[{i}] {result['title']}\n")
            self.result_text.insert(tk.END, f"URL: {result['url']}\n")
            self.result_text.insert(tk.END, f"{'─'*60}\n")
            content_preview = result['content'][:200].replace('\n', ' ') + '...' if len(result['content']) > 200 else result['content']
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
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"naver_blog_{keyword}.json"
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
    app = NaverBlogCrawlerGUI(root)
    root.mainloop()