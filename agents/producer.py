"""
Producer Agent - 製片代理人
負責音訊生成、時間對齊和最終製片協調
"""
from typing import Dict, Any, List
import base64
import io
from .base_agent import BaseAgent


class ProducerAgent(BaseAgent):
    """製片代理人"""
    
    def __init__(self):
        super().__init__(
            name="Producer",
            role="專業的影片製作協調人，負責音訊和時間軸管理",
            agent_type="producer"  # 使用數據處理優化的模型
        )
    
    def execute(self, scripts: Dict[str, Any], slides: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        生成音訊和時間對齊方案
        
        Args:
            scripts: 教學腳本數據
            slides: 投影片設計數據
            
        Returns:
            製片方案（包含音訊和時間軸）
        """
        print(f"🎬 {self.name} 正在規劃製片方案...")
        
        scripts_data = scripts.get('scripts', [])
        slides_data = slides.get('slides', [])
        
        # 計算每個段落的預估音訊時長（基於文字長度）
        timeline = []
        current_time = 0.0
        
        for chapter in scripts_data:
            for segment in chapter.get('segments', []):
                segment_id = segment['segment_id']
                text = segment['text']
                
                # 估算說話時長：平均每分鐘 150 字（中文）
                estimated_duration = len(text) / 150 * 60
                
                # 找到對應的投影片
                corresponding_slides = [
                    s for s in slides_data 
                    if s.get('segment_id') == segment_id
                ]
                
                timeline_entry = {
                    "segment_id": segment_id,
                    "chapter_number": chapter['chapter_number'],
                    "text": text,
                    "start_time": current_time,
                    "end_time": current_time + estimated_duration,
                    "duration": estimated_duration,
                    "slide_ids": [s['slide_id'] for s in corresponding_slides],
                    "audio_file": f"audio_{segment_id}.mp3"
                }
                
                timeline.append(timeline_entry)
                current_time += estimated_duration
        
        # 生成 TTS 配置
        tts_tasks = []
        for entry in timeline:
            tts_tasks.append({
                "task_id": entry['segment_id'],
                "text": entry['text'],
                "voice": "zh-TW-Standard-A",  # 可配置
                "speed": 1.0,
                "output_file": entry['audio_file']
            })
        
        # 生成投影片時間軸
        slides_timeline = []
        for slide in slides_data:
            segment_id = slide.get('segment_id')
            if segment_id:
                # 找到對應的時間段
                matching_entry = next((e for e in timeline if e['segment_id'] == segment_id), None)
                if matching_entry:
                    slides_timeline.append({
                        "slide_id": slide['slide_id'],
                        "start_time": matching_entry['start_time'],
                        "end_time": matching_entry['end_time'],
                        "duration": matching_entry['duration']
                    })
        
        result = {
            "timeline": timeline,
            "tts_tasks": tts_tasks,
            "slides_timeline": slides_timeline,
            "total_duration": current_time,
            "video_config": {
                "resolution": "1920x1080",
                "fps": 30,
                "format": "mp4"
            }
        }
        
        print(f"✅ 製片方案完成：總時長約 {current_time:.1f} 秒")
        print(f"   - {len(tts_tasks)} 個音訊任務")
        print(f"   - {len(slides_timeline)} 張投影片")
        
        return {
            "success": True,
            "agent": self.name,
            "data": result
        }
    
    def generate_audio_gemini(self, text: str) -> bytes:
        """
        使用 Gemini API 生成語音（佔位符，實際需要 TTS API）
        
        Args:
            text: 要轉換的文字
            
        Returns:
            音訊數據（bytes）
        """
        # 注意：Gemini API 目前可能不直接支持 TTS
        # 這裡是佔位符，實際可能需要使用 Google Cloud TTS 或其他服務
        print(f"⚠️ TTS 功能需要額外的 API 支持")
        return b""  # 返回空數據作為佔位符
