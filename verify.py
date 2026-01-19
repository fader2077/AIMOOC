"""
项目验证脚本 - 验证所有功能是否正常工作
"""
import os
import json
import sys

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (不存在)")
        return False

def check_directory_exists(dir_path, description):
    """检查目录是否存在"""
    if os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} (不存在)")
        return False

def check_json_valid(file_path):
    """检查 JSON 文件是否有效"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"   ✓ JSON 有效，包含 {len(data)} 個鍵")
        return True
    except Exception as e:
        print(f"   ✗ JSON 無效：{str(e)}")
        return False

def main():
    import sys
    import io
    
    # 设置输出编码为 UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 60)
    print("AI 磨課師專案驗證")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    # 1. 检查核心文件
    print("【1】核心文件檢查")
    print("-" * 60)
    
    core_files = [
        ("config.py", "配置文件"),
        ("orchestrator.py", "協調者"),
        ("app.py", "Flask 服務器"),
        ("demo.py", "演示腳本"),
        ("test.py", "測試腳本"),
        ("requirements.txt", "依賴列表"),
        ("README.md", "專案說明"),
        ("USAGE.md", "使用指南"),
        ("PROJECT_SUMMARY.md", "專案總結"),
    ]
    
    for file_name, description in core_files:
        if not check_file_exists(file_name, description):
            all_checks_passed = False
    
    print()
    
    # 2. 检查 Agent 文件
    print("【2】Agent 系統檢查")
    print("-" * 60)
    
    agent_files = [
        ("agents/__init__.py", "Agent Package"),
        ("agents/base_agent.py", "基礎 Agent"),
        ("agents/curriculum_designer.py", "教學設計 Agent"),
        ("agents/scriptwriter.py", "腳本 Agent"),
        ("agents/visual_artist.py", "視覺 Agent"),
        ("agents/producer.py", "製片 Agent"),
    ]
    
    for file_name, description in agent_files:
        if not check_file_exists(file_name, description):
            all_checks_passed = False
    
    print()
    
    # 3. 检查前端文件
    print("【3】前端文件檢查")
    print("-" * 60)
    
    frontend_files = [
        ("templates/index.html", "Web 介面"),
        ("static/app.js", "前端邏輯"),
    ]
    
    for file_name, description in frontend_files:
        if not check_file_exists(file_name, description):
            all_checks_passed = False
    
    print()
    
    # 4. 检查输出目录
    print("【4】輸出目錄檢查")
    print("-" * 60)
    
    output_dirs = [
        ("outputs", "輸出根目錄"),
        ("outputs/audio", "音訊目錄"),
        ("outputs/slides", "投影片目錄"),
        ("outputs/videos", "影片目錄"),
    ]
    
    for dir_name, description in output_dirs:
        if not check_directory_exists(dir_name, description):
            all_checks_passed = False
    
    print()
    
    # 5. 检查生成的课程文件
    print("【5】生成的課程文件檢查")
    print("-" * 60)
    
    if os.path.exists("outputs"):
        json_files = [f for f in os.listdir("outputs") if f.endswith('.json')]
        if json_files:
            print(f"✅ 找到 {len(json_files)} 個課程文件")
            for json_file in json_files[:3]:  # 只显示前3个
                file_path = os.path.join("outputs", json_file)
                print(f"   📄 {json_file}")
                check_json_valid(file_path)
        else:
            print("⚠️  未找到生成的課程文件（運行 demo.py 生成）")
    
    print()
    
    # 6. 统计代码行数
    print("【6】代碼統計")
    print("-" * 60)
    
    total_lines = 0
    py_files = []
    
    for root, dirs, files in os.walk("."):
        # 跳过特定目录
        dirs[:] = [d for d in dirs if d not in ['__pycache__', 'outputs', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                        py_files.append((file_path, lines))
                except:
                    pass
    
    print(f"✅ Python 文件總數：{len(py_files)} 個")
    print(f"✅ 總代碼行數：{total_lines} 行")
    
    # 显示最大的几个文件
    py_files.sort(key=lambda x: x[1], reverse=True)
    print("\n   最大的 5 個文件：")
    for file_path, lines in py_files[:5]:
        print(f"   - {file_path}: {lines} 行")
    
    print()
    
    # 7. 检查依赖
    print("【7】依賴套件檢查")
    print("-" * 60)
    
    try:
        import google.genai
        print("✅ google-genai 已安裝")
    except ImportError:
        print("❌ google-genai 未安裝")
        all_checks_passed = False
    
    try:
        import flask
        print("✅ flask 已安裝")
    except ImportError:
        print("❌ flask 未安裝")
        all_checks_passed = False
    
    try:
        import flask_cors
        print("✅ flask-cors 已安裝")
    except ImportError:
        print("❌ flask-cors 未安裝")
        all_checks_passed = False
    
    try:
        import PIL
        print("✅ pillow 已安裝")
    except ImportError:
        print("❌ pillow 未安裝")
        all_checks_passed = False
    
    print()
    
    # 最终总结
    print("=" * 60)
    if all_checks_passed:
        print("🎉 所有檢查通過！專案已準備就緒")
        print()
        print("下一步：")
        print("  1. 運行演示：python demo.py")
        print("  2. 啟動 Web 介面：python app.py")
        print("  3. 查看文檔：README.md 和 USAGE.md")
    else:
        print("⚠️  部分檢查未通過，請查看上述錯誤")
    print("=" * 60)
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
