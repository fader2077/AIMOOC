"""
Flask API 服務器
提供 RESTful API 接口
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from orchestrator import Orchestrator
import config

app = Flask(__name__)
CORS(app)

# 全局變量
orchestrator = None


@app.route('/health')
def health_check():
    """Health check endpoint for Docker and load balancers"""
    return jsonify({
        "status": "healthy",
        "service": "AI MOOC Generator",
        "version": "1.0.0",
        "ollama_configured": bool(config.OLLAMA_BASE_URL),
        "gemini_configured": bool(config.GEMINI_API_KEY)
    }), 200


@app.route('/')
def index():
    """首頁"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_course():
    """
    生成課程 API
    
    Request Body:
        {
            "topic": "課程主題",
            "target_audience": "目標受眾",
            "duration_minutes": 10
        }
    
    Response:
        {
            "success": true,
            "results": {...},
            "elapsed_time": 45.2,
            "timestamp": 1234567890
        }
    """
    try:
        data = request.get_json()
        
        topic = data.get('topic')
        target_audience = data.get('target_audience', '初學者')
        duration_minutes = data.get('duration_minutes', 10)
        
        if not topic:
            return jsonify({
                "success": False,
                "error": "請提供課程主題"
            }), 400
        
        # 創建新的 Orchestrator
        global orchestrator
        orchestrator = Orchestrator()
        
        # 執行課程生成流程
        result = orchestrator.execute_pipeline(
            topic=topic,
            target_audience=target_audience,
            duration_minutes=duration_minutes
        )
        
        # 保存結果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(config.OUTPUT_DIR, f"course_{timestamp}.json")
        orchestrator.save_results(result, output_file)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ API 錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/decision-logs', methods=['GET'])
def get_decision_logs():
    """
    獲取 Agent 決策日誌
    
    Response:
        {
            "curriculum_designer": [...],
            "scriptwriter": [...],
            "visual_artist": [...],
            "producer": [...]
        }
    """
    try:
        if not orchestrator:
            return jsonify({
                "success": False,
                "error": "尚未執行課程生成"
            }), 400
        
        logs = orchestrator.get_decision_logs()
        return jsonify({
            "success": True,
            "logs": logs
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/outputs/<path:filename>')
def serve_output(filename):
    """提供輸出文件下載"""
    return send_from_directory(config.OUTPUT_DIR, filename)


@app.errorhandler(404)
def not_found(e):
    """404 錯誤處理"""
    return jsonify({
        "success": False,
        "error": "API endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """500 錯誤處理"""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    # 设置控制台编码为UTF-8
    import sys
    if sys.platform == 'win32':
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        except:
            pass
    
    print("=" * 60)
    print("AI 磨課師系統啟動中...")
    print(f"API 地址: http://{config.HOST}:{config.PORT}")
    print(f"Gemini API: {'已配置' if config.GEMINI_API_KEY else '未配置'}")
    print(f"輸出目錄: {config.OUTPUT_DIR}")
    print(f"環境模式: {config.FLASK_ENV}")
    print("=" * 60)
    
    if config.DEBUG:
        print("\n⚠️  WARNING: Running in DEBUG mode. Not for production!")
        print("   For production, use: gunicorn -w 4 -b 0.0.0.0:5001 wsgi:app\n")
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
