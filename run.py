import sys
import webbrowser
import threading
import time
import uvicorn

def open_browser():
    time.sleep(1.5)
    url = "http://127.0.0.1:8000"
    print(f"\n[GramSetu] Opening browser at {url} ...\n")
    webbrowser.open(url)

if __name__ == "__main__":
    print("=" * 60)
    print("  🚀 Starting GramSetu Rural Problem Redressal Network")
    print("  🌐 Website URL: http://127.0.0.1:8000")
    print("=" * 60)
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
