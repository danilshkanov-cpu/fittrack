#!/usr/bin/env python3
"""
Сервер для трекера. Запусти этот файл на компьютере,
потом отсканируй QR-код телефоном.
"""
import http.server
import socketserver
import socket
import os
import sys
import threading
import webbrowser

PORT = 8080

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def print_qr(url):
    try:
        import qrcode
        qr = qrcode.QRCode(version=2, box_size=10, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        print("\n" + "="*50)
        print("  QR-КОД ДЛЯ ТЕЛЕФОНА:")
        print("="*50)
        qr.print_ascii(invert=True)
        print("="*50)
    except ImportError:
        print("  (установи qrcode: pip install qrcode)")

def main():
    # Найти папку со скриптом
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Проверить что tracker.html рядом
    if not os.path.exists("tracker.html"):
        print("ОШИБКА: файл tracker.html не найден рядом со скриптом!")
        print(f"Папка скрипта: {script_dir}")
        input("Нажми Enter для выхода...")
        sys.exit(1)

    ip = get_local_ip()
    url = f"http://{ip}:{PORT}/tracker.html"

    print("\n" + "="*50)
    print("  МОЙ ТРЕКЕР — ЛОКАЛЬНЫЙ СЕРВЕР")
    print("="*50)
    print(f"\n  Сервер запущен!")
    print(f"  Адрес для телефона: {url}")
    print(f"\n  ВАЖНО: телефон и компьютер")
    print(f"  должны быть в одной Wi-Fi сети!")
    print("\n  Для остановки нажми Ctrl+C")
    
    print_qr(url)
    
    print(f"\n  Ссылка: {url}\n")

    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None  # Убрать логи запросов

    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  Сервер остановлен. До встречи!")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\nОШИБКА: порт {PORT} уже занят.")
            print("Закрой другой сервер или измени PORT в скрипте.")
        else:
            print(f"\nОШИБКА: {e}")
        input("Нажми Enter для выхода...")

if __name__ == "__main__":
    main()
