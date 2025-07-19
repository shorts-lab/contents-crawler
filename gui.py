#!/usr/bin/env python
import tkinter as tk
from src.interfaces.gui import CrawlerGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = CrawlerGUI(root)
    root.mainloop()