"""
Visual Artist Agent - 視覺代理人
負責設計投影片佈局和生成圖像描述
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class VisualArtistAgent(BaseAgent):
    """視覺代理人"""
    
    def __init__(self):
        super().__init__(
            name="Visual Artist",
            role="專業的視覺設計師，擅長教育類投影片設計",
            agent_type="visual"  # 使用結構化輸出優化的模型
        )
    
    def execute(self, scripts: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        設計投影片佈局和視覺元素
        
        Args:
            scripts: 教學腳本數據
            
        Returns:
            投影片設計結構
        """
        print(f"🎨 {self.name} 正在設計投影片...")
        
        system_instruction = """你是一位專業的教育類投影片視覺設計師。

設計原則：
1. 每個章節開始時要有封面頁（包含章節標題和編號）
2. 內容頁要簡潔明瞭，避免文字過多
3. 適當使用圖表、圖示等視覺元素
4. 保持視覺風格統一（色彩、字體、佈局）
5. 每個腳本段落對應 1-2 張投影片
6. 為需要圖像的投影片提供詳細的圖像生成提示詞

⚠️ 重要：請返回純淨的JSON格式，不要包含任何註釋（//或/**/）！

請以 JSON 格式回應，結構如下：
{
  "style": {
    "theme": "主題風格（如：現代簡約、專業商務等）",
    "primary_color": "主色調",
    "secondary_color": "輔色",
    "font_style": "字體風格"
  },
  "slides": [
    {
      "slide_id": "slide_1",
      "slide_type": "title|content|image|chart",
      "chapter_number": 章節編號,
      "segment_id": "對應的腳本段落ID",
      "title": "投影片標題",
      "content": {
        "text": "主要文字內容（簡潔版）",
        "bullet_points": ["要點1", "要點2"],
        "image_prompt": "如果需要圖像，提供詳細的生成提示詞",
        "layout": "佈局描述"
      }
    }
  ]
}"""
        
        scripts_data = scripts.get('scripts', [])
        
        prompt = f"""請為以下教學腳本設計投影片佈局：

教學腳本：
"""
        for chapter in scripts_data:
            prompt += f"""
第 {chapter['chapter_number']} 章：{chapter['chapter_title']}
"""
            for seg in chapter.get('segments', []):
                prompt += f"  - [{seg['segment_id']}] {seg['text'][:100]}...\n"
        
        prompt += """
請設計完整的投影片佈局，確保視覺吸引力和教學效果。
對於需要圖像的投影片，請提供詳細的圖像生成提示詞（適合 AI 圖像生成）。"""
        
        response_text = self._call_ai(
            prompt=prompt,
            system_instruction=system_instruction,
            temperature=0.7
        )
        
        try:
            visual_design = self._extract_json(response_text)
            
            slides_count = len(visual_design.get('slides', []))
            print(f"✅ 投影片設計完成：共 {slides_count} 張投影片")
            
            return {
                "success": True,
                "agent": self.name,
                "data": visual_design,
                "raw_response": response_text
            }
            
        except Exception as e:
            print(f"❌ 視覺設計解析失敗: {str(e)}")
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "raw_response": response_text
            }
