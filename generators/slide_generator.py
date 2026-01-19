"""
投影片生成器 - 將 JSON 配置轉換為實際的圖片檔案
"""
import os
from typing import Dict, Any, List
from PIL import Image, ImageDraw, ImageFont
import json


class SlideGenerator:
    """投影片生成器"""
    
    def __init__(self, output_dir: str = None):
        """
        初始化投影片生成器
        
        Args:
            output_dir: 輸出目錄
        """
        if output_dir is None:
            from config import SLIDES_DIR
            output_dir = SLIDES_DIR
        
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 投影片配置
        self.width = 1920
        self.height = 1080
        self.default_bg_color = (102, 126, 234)  # #667eea
        self.text_color = (255, 255, 255)
        
        # 載入字體（跨平台支持）
        self.title_font = self._load_font(80)
        self.subtitle_font = self._load_font(50)
        self.text_font = self._load_font(36)
        self.small_font = self._load_font(28)
    
    def _load_font(self, size: int):
        """載入字體（跨平台支持）"""
        import platform
        import sys
        
        font_paths = []
        system = platform.system()
        
        if system == "Windows":
            font_paths = [
                "C:/Windows/Fonts/msyh.ttc",
                "C:/Windows/Fonts/simhei.ttf",
                "C:/Windows/Fonts/simsun.ttc"
            ]
        elif system == "Darwin":  # macOS
            font_paths = [
                "/System/Library/Fonts/PingFang.ttc",
                "/Library/Fonts/Arial Unicode.ttf"
            ]
        else:  # Linux
            font_paths = [
                "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            ]
        
        # 嘗試從 assets 目錄載入（優先）
        assets_font = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'NotoSansTC-Bold.otf')
        if os.path.exists(assets_font):
            try:
                return ImageFont.truetype(assets_font, size)
            except:
                pass
        
        # 嘗試系統字體
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        
        # 如果都失敗，使用預設字體
        print(f"⚠️ 無法載入中文字體，使用預設字體 (size={size})")
        return ImageFont.load_default()
    
    def generate_slides(self, course_data: Dict[str, Any], course_id: str) -> List[str]:
        """
        生成所有投影片
        
        Args:
            course_data: 完整的課程數據（包含 visual_design）
            course_id: 課程 ID（用於命名文件）
            
        Returns:
            生成的投影片文件路徑列表
        """
        print("\n🎨 開始生成投影片...")
        
        visual_design = course_data.get('results', {}).get('visual_design', {})
        slides_data = visual_design.get('slides', [])
        style = visual_design.get('style', {})
        
        # 更新背景色（如果有）
        if 'primary_color' in style:
            try:
                color_hex = style['primary_color'].lstrip('#')
                self.default_bg_color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
            except:
                pass
        
        generated_files = []
        
        for i, slide in enumerate(slides_data, 1):
            try:
                filename = f"{course_id}_slide_{slide.get('slide_id', i)}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                # 根據投影片類型生成
                slide_type = slide.get('slide_type', 'content')
                if slide_type == 'title':
                    self._generate_title_slide(slide, filepath)
                elif slide_type == 'chapter':
                    self._generate_chapter_slide(slide, filepath)
                else:
                    self._generate_content_slide(slide, filepath)
                
                generated_files.append(filepath)
                print(f"  ✅ 已生成：{filename}")
                
            except Exception as e:
                print(f"  ❌ 生成投影片失敗 {slide.get('slide_id', i)}: {str(e)}")
        
        print(f"\n✅ 投影片生成完成！共 {len(generated_files)} 張")
        return generated_files
    
    def _generate_title_slide(self, slide: Dict[str, Any], filepath: str):
        """生成標題投影片"""
        img = Image.new('RGB', (self.width, self.height), self.default_bg_color)
        draw = ImageDraw.Draw(img)
        
        # 繪製漸層效果（簡化版）
        for i in range(self.height):
            alpha = int(255 * (1 - i / self.height * 0.3))
            color = tuple(min(255, c + alpha // 10) for c in self.default_bg_color)
            draw.rectangle([(0, i), (self.width, i+1)], fill=color)
        
        # 標題
        title = slide.get('title', '課程標題')
        bbox = draw.textbbox((0, 0), title, font=self.title_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2 - 100
        draw.text((x, y), title, fill=self.text_color, font=self.title_font)
        
        # 副標題
        content = slide.get('content', {})
        subtitle = content.get('subtitle', '')
        if subtitle:
            bbox = draw.textbbox((0, 0), subtitle, font=self.subtitle_font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2 + 50
            draw.text((x, y), subtitle, fill=self.text_color, font=self.subtitle_font)
        
        img.save(filepath, 'PNG')
    
    def _generate_chapter_slide(self, slide: Dict[str, Any], filepath: str):
        """生成章節投影片"""
        img = Image.new('RGB', (self.width, self.height), self.default_bg_color)
        draw = ImageDraw.Draw(img)
        
        # 章節編號
        chapter_num = slide.get('chapter_number', 1)
        chapter_text = f"第 {chapter_num} 章"
        bbox = draw.textbbox((0, 0), chapter_text, font=self.subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 300), chapter_text, fill=self.text_color, font=self.subtitle_font)
        
        # 章節標題
        title = slide.get('title', '')
        bbox = draw.textbbox((0, 0), title, font=self.title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 450), title, fill=self.text_color, font=self.title_font)
        
        img.save(filepath, 'PNG')
    
    def _generate_content_slide(self, slide: Dict[str, Any], filepath: str):
        """生成內容投影片"""
        img = Image.new('RGB', (self.width, self.height), self.default_bg_color)
        draw = ImageDraw.Draw(img)
        
        # 標題區域
        title = slide.get('title', '')
        draw.rectangle([(0, 0), (self.width, 150)], fill=(0, 0, 0, 50))
        draw.text((60, 50), title, fill=self.text_color, font=self.subtitle_font)
        
        # 內容區域
        content = slide.get('content', {})
        y_offset = 220
        
        # 主要文字
        text = content.get('text', '')
        if text:
            # 文字換行處理
            max_width = self.width - 120
            lines = self._wrap_text(text, self.text_font, max_width)
            for line in lines[:8]:  # 最多8行
                draw.text((60, y_offset), line, fill=self.text_color, font=self.text_font)
                y_offset += 50
        
        # 要點列表
        bullet_points = content.get('bullet_points', [])
        if bullet_points:
            y_offset += 30
            for point in bullet_points[:5]:  # 最多5個要點
                draw.ellipse([(60, y_offset + 15), (75, y_offset + 30)], fill=self.text_color)
                point_lines = self._wrap_text(point, self.small_font, max_width - 40)
                for line in point_lines[:2]:  # 每個要點最多2行
                    draw.text((100, y_offset), line, fill=self.text_color, font=self.small_font)
                    y_offset += 40
        
        img.save(filepath, 'PNG')
    
    def _wrap_text(self, text: str, font, max_width: int) -> List[str]:
        """文字換行處理"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines


if __name__ == "__main__":
    # 測試代碼
    print("投影片生成器模組已載入")
