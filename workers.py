# workers.py - Worker Manager Process
import socket
import json
from multiprocessing import Pool
from playwright.sync_api import sync_playwright


class WorkerManager:
    def __init__(self, workers=8):
        self.workers = workers
        self.pool = None
        self.sock = None
    def _scrape_worker(self, url):
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch()
                page = browser.new_page()
                page.goto(url, timeout=15000)
                content = page.content()
                browser.close()
                return content
            except Exception as e:
                return f"Scraping failed: {str(e)}"

    def _handle_connection(self, conn):
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                try:
                    task = json.loads(data.decode().strip())
                    result = self.pool.apply(self._scrape_worker, (task['url'],))
                    conn.sendall(json.dumps({
                        "status": 200,
                        "content": result
                    }).encode() + b'\n')
                except Exception as e:
                    conn.sendall(json.dumps({
                        "status": 500,
                        "content": str(e)
                    }).encode() + b'\n')

    def start(self):
        self.pool = Pool(self.workers)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', 9999))
        self.sock.listen()
        print(f"Worker manager ready with {self.workers} processes")

        while True:
            conn, _ = self.sock.accept()
            self._handle_connection(conn)
