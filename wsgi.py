"""
WSGI Entry Point for Production Deployment
使用 Gunicorn 或 Waitress 啟動應用

Usage:
  gunicorn -w 4 -b 0.0.0.0:5001 wsgi:app
  waitress-serve --host=0.0.0.0 --port=5001 wsgi:app
"""
from app import app

if __name__ == "__main__":
    app.run()
