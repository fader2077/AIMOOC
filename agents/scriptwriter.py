"""
Scriptwriter Agent - 腳本代理人
負責將課程大綱轉化為口語化的教學腳本
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class ScriptwriterAgent(BaseAgent):
    """腳本代理人"""
    
    def __init__(self):
        super().__init__(
            name="Scriptwriter",
            role="專業的教學腳本作者，擅長將知識轉化為易懂的口語表達",
            agent_type="scriptwriter"  # 使用創意寫作優化的模型
        )
    
    def execute(self, curriculum: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        生成教學腳本
        
        Args:
            curriculum: 課程大綱數據
            
        Returns:
            教學腳本結構
        """
        print(f"📝 {self.name} 正在撰寫教學腳本...")
        
        course_title = curriculum.get("course_title", "未命名課程")
        chapters = curriculum.get("chapters", [])
        
        system_instruction = """你是一位專業的教學腳本作者，擅長將專業知識轉化為口語化、易懂的教學內容。

撰寫原則：
1. 使用口語化表達，避免過於正式或學術化
2. 適當加入「轉場提示」（如：「接下來我們來看...」「請注意這張圖...」）
3. 每個段落約 30-60 秒的說話長度
4. 使用第一人稱「我」或「我們」
5. 加入互動元素（如：「你可能會想...」「讓我們一起...」）
6. 在需要展示視覺元素的地方標註 [視覺提示: 描述]

⚠️ 重要：請返回純淨的JSON格式，不要包含任何註釋（//或/**/）！

請以 JSON 格式回應，結構如下：
{
  "scripts": [
    {
      "chapter_number": 章節編號,
      "chapter_title": "章節標題",
      "segments": [
        {
          "segment_id": "seg_1_1",
          "text": "口語化腳本內容...",
          "visual_cue": "視覺提示（可選）",
          "estimated_duration": 預估秒數
        }
      ]
    }
  ]
}"""
        
        prompt = f"""請為以下課程撰寫教學腳本：

課程標題：{course_title}

章節內容：
"""
        for chapter in chapters:
            prompt += f"""
第 {chapter['chapter_number']} 章：{chapter['title']}
- 學習目標：{chapter['learning_goal']}
- 重點：{', '.join(chapter['key_points'])}
"""
        
        prompt += """
請為每個章節撰寫詳細的口語化教學腳本，確保自然流暢。"""
        
        response_text = self._call_ai(
            prompt=prompt,
            system_instruction=system_instruction,
            temperature=0.8
        )
        
        try:
            scripts = self._extract_json(response_text)
            
            total_segments = sum(len(ch.get('segments', [])) for ch in scripts.get('scripts', []))
            print(f"✅ 教學腳本生成完成：共 {total_segments} 個段落")
            
            return {
                "success": True,
                "agent": self.name,
                "data": scripts,
                "raw_response": response_text
            }
            
        except Exception as e:
            print(f"❌ 腳本解析失敗: {str(e)}")
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "raw_response": response_text
            }
