"""
演示脚本 - 使用模拟数据展示完整流程
当 API 配额用完时，使用此脚本演示系统功能
"""
import json
import time
from datetime import datetime
import os


class MockOrchestrator:
    """模拟的 Orchestrator，用于演示"""
    
    def __init__(self):
        self.execution_log = []
    
    def execute_pipeline(self, topic, target_audience="初學者", duration_minutes=10):
        """执行模拟的课程生成流程"""
        print("=" * 60)
        print("🚀 AI 磨課師系統啟動（演示模式）")
        print(f"📚 主題：{topic}")
        print(f"👥 受眾：{target_audience}")
        print(f"⏱️  時長：約 {duration_minutes} 分鐘")
        print("=" * 60)
        
        start_time = time.time()
        
        # Step 1: Curriculum Designer
        print("\n【階段 1/4】教學設計")
        print("🎓 Curriculum Designer 正在設計課程大綱...")
        time.sleep(1)
        
        curriculum = {
            "course_title": f"{topic} - 完整教學",
            "target_audience": target_audience,
            "total_duration": duration_minutes,
            "learning_objectives": [
                f"理解{topic}的基本概念",
                f"掌握{topic}的核心原理",
                f"能夠應用{topic}解決實際問題"
            ],
            "chapters": [
                {
                    "chapter_number": 1,
                    "title": "導論與基礎概念",
                    "duration": 3,
                    "learning_goal": f"了解{topic}的定義和重要性",
                    "key_points": ["定義", "歷史發展", "應用領域"]
                },
                {
                    "chapter_number": 2,
                    "title": "核心原理解析",
                    "duration": 4,
                    "learning_goal": f"深入理解{topic}的運作機制",
                    "key_points": ["基本原理", "關鍵技術", "實現方法"]
                },
                {
                    "chapter_number": 3,
                    "title": "實際應用案例",
                    "duration": 3,
                    "learning_goal": f"學會應用{topic}解決問題",
                    "key_points": ["案例分析", "實踐步驟", "注意事項"]
                }
            ]
        }
        print(f"✅ 課程大綱生成完成：{curriculum['course_title']}")
        print(f"   - 共 {len(curriculum['chapters'])} 個章節")
        
        # Step 2: Scriptwriter
        print("\n【階段 2/4】腳本撰寫")
        print("📝 Scriptwriter 正在撰寫教學腳本...")
        time.sleep(1)
        
        scripts = {
            "scripts": [
                {
                    "chapter_number": ch["chapter_number"],
                    "chapter_title": ch["title"],
                    "segments": [
                        {
                            "segment_id": f"seg_{ch['chapter_number']}_{i+1}",
                            "text": f"大家好，歡迎來到{topic}的第{ch['chapter_number']}章。{kp}是我們要學習的重點...",
                            "visual_cue": f"顯示{kp}的示意圖",
                            "estimated_duration": 30
                        }
                        for i, kp in enumerate(ch["key_points"])
                    ]
                }
                for ch in curriculum["chapters"]
            ]
        }
        
        total_segments = sum(len(ch["segments"]) for ch in scripts["scripts"])
        print(f"✅ 教學腳本生成完成：共 {total_segments} 個段落")
        
        # Step 3: Visual Artist
        print("\n【階段 3/4】視覺設計")
        print("🎨 Visual Artist 正在設計投影片...")
        time.sleep(1)
        
        slides = []
        slide_id = 1
        
        # 封面
        slides.append({
            "slide_id": f"slide_{slide_id}",
            "slide_type": "title",
            "chapter_number": 0,
            "segment_id": None,
            "title": curriculum["course_title"],
            "content": {
                "text": f"目標受眾：{target_audience}",
                "layout": "center"
            }
        })
        slide_id += 1
        
        # 每個章節的投影片
        for chapter in scripts["scripts"]:
            # 章節封面
            slides.append({
                "slide_id": f"slide_{slide_id}",
                "slide_type": "title",
                "chapter_number": chapter["chapter_number"],
                "segment_id": None,
                "title": f"第 {chapter['chapter_number']} 章",
                "content": {
                    "text": chapter["chapter_title"],
                    "layout": "center"
                }
            })
            slide_id += 1
            
            # 內容投影片
            for segment in chapter["segments"]:
                slides.append({
                    "slide_id": f"slide_{slide_id}",
                    "slide_type": "content",
                    "chapter_number": chapter["chapter_number"],
                    "segment_id": segment["segment_id"],
                    "title": chapter["chapter_title"],
                    "content": {
                        "text": segment["text"][:50] + "...",
                        "bullet_points": ["要點 1", "要點 2", "要點 3"],
                        "layout": "two-column"
                    }
                })
                slide_id += 1
        
        visual_design = {
            "style": {
                "theme": "現代簡約",
                "primary_color": "#667eea",
                "secondary_color": "#764ba2",
                "font_style": "Sans-serif"
            },
            "slides": slides
        }
        
        print(f"✅ 投影片設計完成：共 {len(slides)} 張投影片")
        
        # Step 4: Producer
        print("\n【階段 4/4】製片協調")
        print("🎬 Producer 正在規劃製片方案...")
        time.sleep(1)
        
        timeline = []
        current_time = 0.0
        
        for chapter in scripts["scripts"]:
            for segment in chapter["segments"]:
                timeline.append({
                    "segment_id": segment["segment_id"],
                    "chapter_number": chapter["chapter_number"],
                    "text": segment["text"],
                    "start_time": current_time,
                    "end_time": current_time + segment["estimated_duration"],
                    "duration": segment["estimated_duration"],
                    "audio_file": f"audio_{segment['segment_id']}.mp3"
                })
                current_time += segment["estimated_duration"]
        
        production = {
            "timeline": timeline,
            "tts_tasks": [
                {
                    "task_id": entry["segment_id"],
                    "text": entry["text"],
                    "voice": "zh-TW-Standard-A",
                    "speed": 1.0,
                    "output_file": entry["audio_file"]
                }
                for entry in timeline
            ],
            "slides_timeline": [
                {
                    "slide_id": slide["slide_id"],
                    "start_time": 0,  # 簡化版本
                    "end_time": 5,
                    "duration": 5
                }
                for slide in slides if slide.get("segment_id")
            ],
            "total_duration": current_time,
            "video_config": {
                "resolution": "1920x1080",
                "fps": 30,
                "format": "mp4"
            }
        }
        
        print(f"✅ 製片方案完成：總時長約 {production['total_duration']:.1f} 秒")
        print(f"   - {len(production['tts_tasks'])} 個音訊任務")
        print(f"   - {len(production['slides_timeline'])} 張投影片")
        
        # 完成
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 60)
        print(f"✅ 所有 Agent 執行完成！耗時：{elapsed_time:.2f} 秒")
        print("=" * 60)
        
        return {
            "success": True,
            "topic": topic,
            "results": {
                "curriculum": curriculum,
                "scripts": scripts,
                "visual_design": visual_design,
                "production": production
            },
            "execution_log": self.execution_log,
            "elapsed_time": elapsed_time,
            "timestamp": time.time()
        }
    
    def save_results(self, results, output_path):
        """保存结果"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"💾 結果已保存到：{output_path}")


def main():
    """主函数"""
    print("🎓 AI 磨課師系統 - 完整演示")
    print("\n注意：此演示使用模擬數據，不需要 API 配額")
    print("=" * 60)
    
    # 创建输出目录
    os.makedirs("outputs", exist_ok=True)
    
    # 测试不同主题
    topics = [
        "Python 程式設計入門",
        "機器學習基礎",
        "深度學習與神經網路"
    ]
    
    for i, topic in enumerate(topics, 1):
        print(f"\n\n{'='*60}")
        print(f"示例 {i}/{len(topics)}")
        print(f"{'='*60}")
        
        orchestrator = MockOrchestrator()
        result = orchestrator.execute_pipeline(
            topic=topic,
            target_audience="初學者" if i == 1 else "中級學習者",
            duration_minutes=10
        )
        
        # 保存结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"outputs/demo_course_{i}_{timestamp}.json"
        orchestrator.save_results(result, output_file)
        
        # 显示摘要
        print("\n📊 課程摘要：")
        curriculum = result["results"]["curriculum"]
        print(f"   📌 標題：{curriculum['course_title']}")
        print(f"   📚 章節：{len(curriculum['chapters'])} 個")
        
        scripts = result["results"]["scripts"]
        total_segments = sum(len(ch["segments"]) for ch in scripts["scripts"])
        print(f"   📝 腳本段落：{total_segments} 個")
        
        slides = result["results"]["visual_design"]["slides"]
        print(f"   🎨 投影片：{len(slides)} 張")
        
        production = result["results"]["production"]
        print(f"   ⏱️  總時長：{production['total_duration']:.1f} 秒")
        print(f"   🎵 音訊任務：{len(production['tts_tasks'])} 個")
        
        if i < len(topics):
            print("\n按 Enter 繼續下一個示例...")
            input()
    
    print("\n\n" + "=" * 60)
    print("🎉 演示完成！")
    print("=" * 60)
    print("\n生成的文件位於 outputs/ 目錄")
    print("你可以查看 JSON 文件以了解完整的數據結構")
    print("\n要啟動 Web 介面，請運行：python app.py")


if __name__ == "__main__":
    main()
