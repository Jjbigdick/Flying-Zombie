# server.py - Async HTTP Server
import asyncio
import json
from urllib.parse import unquote, urlparse
from multiprocessing import Process
import socket


class AsyncHTTPServer:
    def __init__(self, host='0.0.0.0', port=8080, worker_host='127.0.0.1', worker_port=9999):
        self.host = host
        self.port = port
        self.worker_host = worker_host
        self.worker_port = worker_port
        self.server = None
        self.worker_sock = None

    async def connect_to_workers(self):
        self.worker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.worker_sock.connect((self.worker_host, self.worker_port))
        self.worker_sock.setblocking(False)
        print("Connected to worker manager")

    async def _validate_request(self, path):
        parsed = urlparse(path)
        if parsed.path != "/scrape":
            return (400, "Invalid endpoint")

        query = parse_qs(parsed.query)
        if 'url' not in query or not query['url'][0].startswith(('http://', 'https://')):
            return (400, "Missing/invalid URL parameter")

        return (200, unquote(query['url'][0]))

    async def _send_to_worker(self, url):
        loop = asyncio.get_event_loop()
        await loop.sock_sendall(self.worker_sock,
                                json.dumps({"url": url}).encode() + b'\n')

        response = b''
        while True:
            chunk = await loop.sock_recv(self.worker_sock, 1024)
            response += chunk
            if b'\n' in chunk:
                break

        return json.loads(response.decode().strip())

    async def handle_client(self, reader, writer):
        try:
            data = await reader.read(4096)
            path = data.decode().split()[1]

            status, url = await self._validate_request(path)
            if status != 200:
                writer.write(f"HTTP/1.1 {status}\r\n\r\n".encode())
                return

            scraped_data = await self._send_to_worker(url)

            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/html\r\n"
                f"Content-Length: {len(scraped_data)}\r\n\r\n"
                f"{scraped_data}"
            )
            writer.write(response.encode())

        except Exception as e:
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
            print(f"Error: {str(e)[:200]}")
        finally:
            await writer.drain()
            writer.close()

    async def start(self):
        await self.connect_to_workers()
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port)

        async with self.server:
            await self.server.serve_forever()

    def stop(self):
        if self.worker_sock:
            self.worker_sock.close()


if __name__ == "__main__":
    # Start worker manager in separate process
    from workers import WorkerManager

    worker_process = Process(target=WorkerManager(8).start)
    worker_process.start()

    server = AsyncHTTPServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        server.stop()
        worker_process.terminate()
