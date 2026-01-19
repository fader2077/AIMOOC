"""
視頻生成器 - 將投影片和音頻合成為視頻
使用 moviepy 庫進行視頻合成
"""
import os
from typing import Dict, Any, List
import json


class VideoGenerator:
    """視頻生成器"""
    
    def __init__(self, output_dir: str = None):
        """
        初始化視頻生成器
        
        Args:
            output_dir: 輸出目錄
        """
        if output_dir is None:
            from config import VIDEO_DIR
            output_dir = VIDEO_DIR
        
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 檢查依賴
        self._check_dependencies()
    
    def _check_dependencies(self):
        """檢查並安裝必要的依賴"""
        try:
            # moviepy 2.x 使用新的導入方式
            from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
            self.moviepy_available = True
            print("✅ moviepy 已就緒")
        except ImportError:
            self.moviepy_available = False
            print("⚠️ moviepy 未安裝，視頻生成功能將受限")
            print("提示：運行 'pip install moviepy' 安裝視頻處理功能")
    
    def generate_video(self, course_data: Dict[str, Any], course_id: str, 
                      slide_files: List[str], audio_files: List[str]) -> str:
        """
        生成視頻
        
        Args:
            course_data: 完整的課程數據
            course_id: 課程 ID
            slide_files: 投影片文件列表
            audio_files: 音頻文件列表
            
        Returns:
            生成的視頻文件路徑
        """
        print("\n🎬 開始生成視頻...")
        
        if not self.moviepy_available:
            print("❌ 視頻生成失敗：moviepy 未安裝")
            return ""
        
        if not slide_files:
            print("❌ 沒有投影片文件")
            return ""
        
        try:
            # moviepy 2.x 使用新的導入方式
            from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
            
            # 獲取時間軸信息
            production = course_data.get('results', {}).get('production', {})
            timeline = production.get('timeline', [])
            slides_timeline = production.get('slides_timeline', [])
            
            # 創建投影片字典（slide_id -> file_path）
            slide_dict = {}
            for filepath in slide_files:
                filename = os.path.basename(filepath)
                # 從文件名提取 slide_id
                # 格式: test_1768391845_slide_chapter_1_slide_1.png -> chapter_1_slide_1
                if '_slide_' in filename:
                    # 找到第一個 _slide_ 後的所有內容（去掉 .png）
                    slide_id = filename.split('_slide_', 1)[1].replace('.png', '')
                    slide_dict[slide_id] = filepath
            
            print(f"  檢測到 {len(slide_dict)} 個投影片文件")
            if slide_dict:
                print(f"  示例 slide_id: {list(slide_dict.keys())[:3]}")
            
            # 創建視頻片段列表
            video_clips = []
            
            if timeline and slides_timeline:
                # 方案A：根據時間軸精確控制（推薦）
                print("使用精確時間軸生成視頻...")
                video_clips = self._generate_with_timeline(
                    slide_dict, audio_files, timeline, slides_timeline
                )
            else:
                # 方案B：簡單模式，每張投影片固定時長
                print("使用簡單模式生成視頻...")
                video_clips = self._generate_simple(slide_dict, audio_files)
            
            if not video_clips:
                print("❌ 沒有生成任何視頻片段")
                return ""
            
            # 合併所有片段
            print("正在合併視頻片段...")
            final_video = concatenate_videoclips(video_clips, method="chain")
            
            # 添加音頻（如果有）
            if audio_files:
                try:
                    print("正在添加音頻軌道...")
                    from moviepy import AudioFileClip, concatenate_audioclips
                    audio_clips = [AudioFileClip(f) for f in audio_files if os.path.exists(f)]
                    if audio_clips:
                        combined_audio = concatenate_audioclips(audio_clips)
                        final_video = final_video.with_audio(combined_audio)
                        print(f"✅ 音頻添加成功 ({combined_audio.duration:.1f}秒)")
                except Exception as e:
                    print(f"⚠️ 音頻添加失敗: {str(e)}")
            
            # 輸出文件
            output_filename = f"{course_id}_final.mp4"
            output_path = os.path.join(self.output_dir, output_filename)
            
            print(f"正在渲染視頻：{output_filename}")
            print(f"視頻時長：{final_video.duration:.1f}秒")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                threads=4,
                preset='medium'
            )
            
            # 清理資源
            for clip in video_clips:
                clip.close()
            final_video.close()
            
            print(f"✅ 視頻生成完成：{output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 視頻生成失敗：{str(e)}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _generate_with_timeline(self, slide_dict: Dict[str, str], 
                                audio_files: List[str],
                                timeline: List[Dict],
                                slides_timeline: List[Dict]) -> List:
        """使用時間軸生成視頻（精確控制）"""
        from moviepy import ImageClip, AudioFileClip
        
        clips = []
        
        # 根據 slides_timeline 創建片段
        for slide_info in slides_timeline:
            slide_id = slide_info.get('slide_id')
            duration = slide_info.get('duration', 5)
            
            if slide_id in slide_dict:
                slide_path = slide_dict[slide_id]
                
                # 創建圖像片段
                img_clip = ImageClip(slide_path, duration=duration)
                clips.append(img_clip)
                
                print(f"  ✅ 添加投影片：{slide_id} (時長 {duration}秒)")
        
        return clips
    
    def _generate_simple(self, slide_dict: Dict[str, str], 
                        audio_files: List[str]) -> List:
        """簡單模式: 每張投影片固定時長"""
        from moviepy import ImageClip, AudioFileClip
        
        clips = []
        default_duration = 10  # 每張投影片默認 10 秒
        
        # 按 slide_id 排序
        sorted_slides = sorted(slide_dict.items(), 
                             key=lambda x: int(x[0].replace('slide_', '')))
        
        for slide_id, slide_path in sorted_slides:
            img_clip = ImageClip(slide_path, duration=default_duration)
            clips.append(img_clip)
            print(f"  ✅ 添加投影片：{slide_id} (時長 {default_duration}秒)")
        
        return clips


if __name__ == "__main__":
    # 測試代碼
    print("視頻生成器模組已載入")
