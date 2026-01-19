"""
Orchestrator - 協調者
負責協調所有 Agent 的執行順序和數據流
"""
import json
import time
from typing import Dict, Any, List
from agents import (
    CurriculumDesignerAgent,
    ScriptwriterAgent,
    VisualArtistAgent,
    ProducerAgent
)
from generators import SlideGenerator, AudioGenerator, VideoGenerator


class Orchestrator:
    """多 Agent 協調者"""
    
    def __init__(self, generate_media: bool = True):
        self.agents = {
            "curriculum_designer": CurriculumDesignerAgent(),
            "scriptwriter": ScriptwriterAgent(),
            "visual_artist": VisualArtistAgent(),
            "producer": ProducerAgent()
        }
        self.execution_log = []
        self.generate_media = generate_media
        
        # 初始化媒體生成器
        if generate_media:
            self.slide_generator = SlideGenerator()
            self.audio_generator = AudioGenerator(engine="edge")  # 使用 Edge TTS
            self.video_generator = VideoGenerator()
        else:
            self.slide_generator = None
            self.audio_generator = None
            self.video_generator = None
        
    def execute_pipeline(self, topic: str, target_audience: str = "初學者", 
                         duration_minutes: int = 10) -> Dict[str, Any]:
        """
        執行完整的課程生成流程
        
        Args:
            topic: 課程主題
            target_audience: 目標受眾
            duration_minutes: 課程時長
            
        Returns:
            完整的課程數據包
        """
        print("=" * 60)
        print("🚀 AI 磨課師系統啟動")
        print(f"📚 主題：{topic}")
        print(f"👥 受眾：{target_audience}")
        print(f"⏱️  時長：約 {duration_minutes} 分鐘")
        print("=" * 60)
        
        start_time = time.time()
        results = {}
        
        try:
            # Step 1: Curriculum Designer Agent
            print("\n【階段 1/4】教學設計")
            curriculum_result = self.agents["curriculum_designer"].execute(
                topic=topic,
                target_audience=target_audience,
                duration_minutes=duration_minutes
            )
            
            if not curriculum_result["success"]:
                raise Exception("課程大綱生成失敗")
            
            results["curriculum"] = curriculum_result["data"]
            self._log_step("curriculum_design", curriculum_result)
            
            # Step 2: Scriptwriter Agent
            print("\n【階段 2/4】腳本撰寫")
            script_result = self.agents["scriptwriter"].execute(
                curriculum=results["curriculum"]
            )
            
            if not script_result["success"]:
                raise Exception("教學腳本生成失敗")
            
            results["scripts"] = script_result["data"]
            self._log_step("scriptwriting", script_result)
            
            # Step 3: Visual Artist Agent
            print("\n【階段 3/4】視覺設計")
            visual_result = self.agents["visual_artist"].execute(
                scripts=results["scripts"]
            )
            
            if not visual_result["success"]:
                raise Exception("視覺設計生成失敗")
            
            results["visual_design"] = visual_result["data"]
            self._log_step("visual_design", visual_result)
            
            # Step 4: Producer Agent
            print("\n【階段 4/4】製片協調")
            producer_result = self.agents["producer"].execute(
                scripts=results["scripts"],
                slides=results["visual_design"]
            )
            
            if not producer_result["success"]:
                raise Exception("製片方案生成失敗")
            
            results["production"] = producer_result["data"]
            self._log_step("production", producer_result)
            
            # Step 5: 媒體生成（如果啟用）
            media_files = {}
            if self.generate_media:
                print("\n【階段 5/6】媒體生成")
                course_id = f"course_{int(time.time())}"
                
                # 組裝完整數據包
                full_data = {
                    "success": True,
                    "topic": topic,
                    "results": results
                }
                
                # 生成投影片
                try:
                    slide_files = self.slide_generator.generate_slides(full_data, course_id)
                    media_files["slides"] = slide_files
                except Exception as e:
                    print(f"⚠️ 投影片生成失敗：{str(e)}")
                    media_files["slides"] = []
                
                # 生成音頻
                try:
                    audio_files = self.audio_generator.generate_audio(full_data, course_id)
                    media_files["audio"] = audio_files
                except Exception as e:
                    print(f"⚠️ 音頻生成失敗：{str(e)}")
                    media_files["audio"] = []
                
                # 生成視頻
                print("\n【階段 6/6】視頻合成")
                try:
                    video_file = self.video_generator.generate_video(
                        full_data, course_id,
                        media_files.get("slides", []),
                        media_files.get("audio", [])
                    )
                    media_files["video"] = video_file
                except Exception as e:
                    print(f"⚠️ 視頻生成失敗：{str(e)}")
                    media_files["video"] = ""
            
            # 完成
            elapsed_time = time.time() - start_time
            print("\n" + "=" * 60)
            print(f"✅ 所有 Agent 執行完成！耗時：{elapsed_time:.2f} 秒")
            if self.generate_media and media_files:
                print(f"📦 生成的媒體文件：")
                print(f"   - 投影片：{len(media_files.get('slides', []))} 張")
                print(f"   - 音頻：{len(media_files.get('audio', []))} 個")
                print(f"   - 視頻：{'有' if media_files.get('video') else '無'}")
            print("=" * 60)
            
            return {
                "success": True,
                "topic": topic,
                "results": results,
                "media_files": media_files if self.generate_media else {},
                "execution_log": self.execution_log,
                "elapsed_time": elapsed_time,
                "timestamp": time.time()
            }
            
        except Exception as e:
            print(f"\n❌ 流程執行失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "results": results,
                "execution_log": self.execution_log
            }
    
    def _log_step(self, step_name: str, result: Dict[str, Any]):
        """記錄執行步驟"""
        self.execution_log.append({
            "step": step_name,
            "timestamp": time.time(),
            "success": result.get("success", False),
            "agent": result.get("agent", "unknown")
        })
    
    def get_decision_logs(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        獲取所有 Agent 的決策日誌
        
        Returns:
            所有 Agent 的對話歷史
        """
        logs = {}
        for agent_name, agent in self.agents.items():
            logs[agent_name] = agent.get_decision_log()
        return logs
    
    def save_results(self, results: Dict[str, Any], output_path: str):
        """
        保存結果到文件
        
        Args:
            results: 執行結果
            output_path: 輸出路徑
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"💾 結果已保存到：{output_path}")
        except Exception as e:
            print(f"❌ 保存失敗: {str(e)}")
