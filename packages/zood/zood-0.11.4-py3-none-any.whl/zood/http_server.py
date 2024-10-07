import http.server
import socketserver
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import socket


# 文件系统事件处理器
class ReloadEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"File modified: {event.src_path}")

    def on_created(self, event):
        print(f"File created: {event.src_path}")

    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")


# 启动 HTTP 服务器
def start_http_server():

    # 对于 vscode 的 live server 的优化
    # vscode_settings = os.path.join(".vscode", "settings.json")

    # if os.path.exists(vscode_settings):
    #     with open(vscode_settings, "r", encoding="utf-8") as f:
    #         settings = json5.load(f)
    #         if "liveServer.settings.port" in settings:
    #             print(
    #                 f'\nVscode live server: http://127.0.0.1:{settings["liveServer.settings.port"]}/docs/index.html\n'
    #             )
    # else:
    #     print(f"\nVscode live server: http://127.0.0.1:5500/docs/index.html\n")

    port = find_available_port()
    # handler = functools.partial(CustomHTTPRequestHandler, directory=html_dir_name)
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        try:
            print(f"\nServing HTTP: http://127.0.0.1:{port}/docs/index.html")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


def find_available_port(start_port=8000):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port  # 如果端口可用,返回端口号
            except OSError:
                port += 1  # 如果端口不可用,尝试下一个端口

def start_server(config):

    start_http_server()
    # 启动文件变化监听
    # start_watchdog(config["markdown_folder"], stop_event)
