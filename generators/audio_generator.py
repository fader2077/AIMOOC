"""
音頻生成器 - 使用 TTS 將文字轉換為語音
支持多種 TTS 引擎：Edge TTS (免費), gTTS (免費), Azure TTS (付費)
"""
import os
import asyncio
from typing import Dict, Any, List
import json


class AudioGenerator:
    """音頻生成器"""
    
    def __init__(self, output_dir: str = None, engine: str = "edge"):
        """
        初始化音頻生成器
        
        Args:
            output_dir: 輸出目錄
            engine: TTS 引擎 ("edge", "gtts", "azure")
        """
        if output_dir is None:
            from config import AUDIO_DIR
            output_dir = AUDIO_DIR
        
        self.output_dir = output_dir
        self.engine = engine
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 檢查依賴
        self._check_dependencies()
    
    def _check_dependencies(self):
        """檢查並安裝必要的依賴"""
        try:
            if self.engine == "edge":
                import edge_tts
                self.tts_available = True
            elif self.engine == "gtts":
                from gtts import gTTS
                self.tts_available = True
            else:
                self.tts_available = False
                print(f"⚠️ TTS 引擎 '{self.engine}' 未安裝，將生成靜音音頻")
        except ImportError:
            self.tts_available = False
            print(f"⚠️ TTS 依賴未安裝，將生成靜音音頻")
            print("提示：運行 'pip install edge-tts gtts' 安裝 TTS 功能")
    
    def generate_audio(self, course_data: Dict[str, Any], course_id: str) -> List[str]:
        """
        生成所有音頻文件
        
        Args:
            course_data: 完整的課程數據（包含 production.tts_tasks）
            course_id: 課程 ID（用於命名文件）
            
        Returns:
            生成的音頻文件路徑列表
        """
        print("\n🎵 開始生成音頻...")
        
        production = course_data.get('results', {}).get('production', {})
        tts_tasks = production.get('tts_tasks', [])
        
        if not tts_tasks:
            print("⚠️ 沒有找到 TTS 任務")
            return []
        
        generated_files = []
        
        if self.engine == "edge" and self.tts_available:
            # 使用 Edge TTS（異步）
            generated_files = asyncio.run(self._generate_with_edge(tts_tasks, course_id))
        elif self.engine == "gtts" and self.tts_available:
            # 使用 gTTS（同步）
            generated_files = self._generate_with_gtts(tts_tasks, course_id)
        else:
            # 生成靜音音頻（備用）
            generated_files = self._generate_silent_audio(tts_tasks, course_id)
        
        print(f"\n✅ 音頻生成完成！共 {len(generated_files)} 個文件")
        return generated_files
    
    async def _generate_with_edge(self, tts_tasks: List[Dict], course_id: str) -> List[str]:
        """使用 Edge TTS 生成音頻（推薦，質量好且免費）"""
        import edge_tts
        
        generated_files = []
        voice = "zh-CN-XiaoxiaoNeural"  # 中文女聲
        
        for i, task in enumerate(tts_tasks, 1):
            try:
                text = task.get('text', '')
                task_id = task.get('task_id', f'seg_{i}')
                filename = f"{course_id}_{task_id}.mp3"
                filepath = os.path.join(self.output_dir, filename)
                
                # 生成音頻
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(filepath)
                
                generated_files.append(filepath)
                print(f"  ✅ 已生成：{filename} ({len(text)} 字)")
                
            except Exception as e:
                print(f"  ❌ 生成音頻失敗 {task.get('task_id', i)}: {str(e)}")
        
        return generated_files
    
    def _generate_with_gtts(self, tts_tasks: List[Dict], course_id: str) -> List[str]:
        """使用 gTTS 生成音頻（備選，免費但質量一般）"""
        from gtts import gTTS
        
        generated_files = []
        
        for i, task in enumerate(tts_tasks, 1):
            try:
                text = task.get('text', '')
                task_id = task.get('task_id', f'seg_{i}')
                filename = f"{course_id}_{task_id}.mp3"
                filepath = os.path.join(self.output_dir, filename)
                
                # 生成音頻
                tts = gTTS(text=text, lang='zh-TW', slow=False)
                tts.save(filepath)
                
                generated_files.append(filepath)
                print(f"  ✅ 已生成：{filename} ({len(text)} 字)")
                
            except Exception as e:
                print(f"  ❌ 生成音頻失敗 {task.get('task_id', i)}: {str(e)}")
        
        return generated_files
    
    def _generate_silent_audio(self, tts_tasks: List[Dict], course_id: str) -> List[str]:
        """生成靜音音頻（當 TTS 不可用時的後備方案）"""
        try:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            generated_files = []
            
            for i, task in enumerate(tts_tasks, 1):
                try:
                    duration_ms = int(task.get('duration', 10) * 1000)  # 秒轉毫秒
                    task_id = task.get('task_id', f'seg_{i}')
                    filename = f"{course_id}_{task_id}.mp3"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    # 生成靜音
                    silent = AudioSegment.silent(duration=duration_ms)
                    silent.export(filepath, format="mp3")
                    
                    generated_files.append(filepath)
                    print(f"  ⚪ 已生成靜音：{filename} ({duration_ms/1000:.1f}秒)")
                    
                except Exception as e:
                    print(f"  ❌ 生成靜音音頻失敗 {task.get('task_id', i)}: {str(e)}")
            
            return generated_files
            
        except ImportError:
            print("⚠️ pydub 未安裝，跳過音頻生成")
            print("提示：運行 'pip install pydub' 安裝音頻處理功能")
            return []


if __name__ == "__main__":
    # 測試代碼
    print("音頻生成器模組已載入")
    print("支持的 TTS 引擎：edge (推薦), gtts, azure")
