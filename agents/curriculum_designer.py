"""
Curriculum Designer Agent - 教學設計代理人
負責根據主題生成具備教學法的課程大綱
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class CurriculumDesignerAgent(BaseAgent):
    """教學設計代理人"""
    
    def __init__(self):
        super().__init__(
            name="Curriculum Designer",
            role="教學設計專家，精通 ADDIE 模型和教學法",
            agent_type="curriculum"  # 使用專門的教學設計模型
        )
    
    def execute(self, topic: str, target_audience: str = "初學者", 
                duration_minutes: int = 10, **kwargs) -> Dict[str, Any]:
        """
        生成課程大綱
        
        Args:
            topic: 課程主題
            target_audience: 目標受眾
            duration_minutes: 課程時長（分鐘）
            
        Returns:
            課程大綱結構
        """
        print(f"🎓 {self.name} 正在設計課程大綱...")
        
        system_instruction = f"""你是一位專業的教學設計師，精通 ADDIE 教學模型（分析、設計、開發、實施、評估）。
你的任務是為「{topic}」主題設計一個約 {duration_minutes} 分鐘的微課程大綱。

設計原則：
1. 知識拆解要循序漸進，確保難度梯度合理
2. 每個章節都要有明確的學習目標
3. 適合{target_audience}的理解程度
4. 每個章節時長約 2-3 分鐘
5. 總共 3-5 個章節

⚠️ 重要：請返回純淨的JSON格式，不要包含任何註釋（//或/**/）！

請以 JSON 格式回應，結構如下：
{{
  "course_title": "課程標題",
  "target_audience": "目標受眾",
  "total_duration": 預估總時長（分鐘）,
  "learning_objectives": ["學習目標1", "學習目標2", ...],
  "chapters": [
    {{
      "chapter_number": 1,
      "title": "章節標題",
      "duration": 預估時長（分鐘）,
      "learning_goal": "本章節學習目標",
      "key_points": ["要點1", "要點2", ...]
    }},
    ...
  ]
}}"""
        
        prompt = f"""請為以下主題設計課程大綱：

主題：{topic}
目標受眾：{target_audience}
課程時長：約 {duration_minutes} 分鐘

請確保課程結構清晰、邏輯連貫，適合線上教學。"""
        
        response_text = self._call_ai(
            prompt=prompt,
            system_instruction=system_instruction,
            temperature=0.7
        )
        
        try:
            curriculum = self._extract_json(response_text)
            
            print(f"✅ 課程大綱生成完成：{curriculum.get('course_title', '未命名課程')}")
            print(f"   - 共 {len(curriculum.get('chapters', []))} 個章節")
            
            return {
                "success": True,
                "agent": self.name,
                "data": curriculum,
                "raw_response": response_text
            }
            
        except Exception as e:
            print(f"❌ 課程大綱解析失敗: {str(e)}")
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "raw_response": response_text
            }
