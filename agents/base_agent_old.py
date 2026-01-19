"""
Base Agent 類別
所有 Agent 的基礎類別
"""
import json
import time
from typing import Dict, Any, List
from google import genai
import config


class BaseAgent:
    """Agent 基礎類別"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.conversation_history = []
        
    def _call_gemini(self, prompt: str, system_instruction: str = None, 
                     temperature: float = 0.7, max_retries: int = 3) -> str:
        """
        調用 Gemini API
        
        Args:
            prompt: 用戶提示
            system_instruction: 系統指令
            temperature: 溫度參數
            max_retries: 最大重試次數
            
        Returns:
            AI 回應文本
        """
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=config.GEMINI_MODEL,
                    contents=prompt,
                    config={
                        "temperature": temperature,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 8192,
                        "system_instruction": system_instruction if system_instruction else ""
                    }
                )
                
                result = response.text
                
                # 記錄對話
                self.conversation_history.append({
                    "role": "user",
                    "content": prompt,
                    "timestamp": time.time()
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": result,
                    "timestamp": time.time()
                })
                
                return result
                
            except Exception as e:
                print(f"⚠️ {self.name} API 調用失敗 (嘗試 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指數退避
                else:
                    raise Exception(f"{self.name} API 調用失敗: {str(e)}")
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        從文本中提取 JSON
        
        Args:
            text: 包含 JSON 的文本
            
        Returns:
            解析後的 JSON 對象
        """
        # 嘗試直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # 嘗試提取 JSON 代碼塊
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # 嘗試提取任何 JSON 結構
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        raise ValueError(f"無法從回應中提取有效的 JSON: {text[:200]}...")
    
    def get_decision_log(self) -> List[Dict[str, Any]]:
        """獲取決策日誌"""
        return self.conversation_history
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        執行 Agent 任務（子類需實現）
        
        Returns:
            執行結果
        """
        raise NotImplementedError("子類必須實現 execute 方法")
