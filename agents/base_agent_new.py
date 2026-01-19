"""
Base Agent 類別 - Ollama 本地化版本
支持 Ollama 本地模型和 Gemini 雲端模型
"""
import json
import time
from typing import Dict, Any, List
import config


class BaseAgent:
    """Agent 基礎類別 - 支持 Ollama 和 Gemini"""
    
    def __init__(self, name: str, role: str, agent_type: str = "default"):
        self.name = name
        self.role = role
        self.agent_type = agent_type
        self.conversation_history = []
        
        # 初始化 AI 提供商
        if config.AI_PROVIDER == "ollama":
            self._init_ollama()
        else:
            self._init_gemini()
    
    def _init_ollama(self):
        """初始化 Ollama 客戶端"""
        import ollama
        self.client_type = "ollama"
        self.ollama_client = ollama
        
        # 根據 Agent 類型選擇模型
        self.model = config.OLLAMA_MODELS.get(
            self.agent_type, 
            config.OLLAMA_MODELS["default"]
        )
        
        if config.VERBOSE:
            print(f"🤖 {self.name} 使用 Ollama 本地模型: {self.model}")
    
    def _init_gemini(self):
        """初始化 Gemini 客戶端"""
        from google import genai
        self.client_type = "gemini"
        self.gemini_client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model = config.GEMINI_MODEL
        
        if config.VERBOSE:
            print(f"☁️ {self.name} 使用 Gemini 雲端模型: {self.model}")
    
    def _call_ai(self, prompt: str, system_instruction: str = None, 
                 temperature: float = None, max_retries: int = None) -> str:
        """
        調用 AI 模型（支持 Ollama 和 Gemini）
        
        Args:
            prompt: 用戶提示
            system_instruction: 系統指令
            temperature: 溫度參數
            max_retries: 最大重試次數
            
        Returns:
            AI 回應文本
        """
        if temperature is None:
            temperature = config.OLLAMA_TEMPERATURE if self.client_type == "ollama" else 0.7
        if max_retries is None:
            max_retries = config.MAX_RETRIES
        
        for attempt in range(max_retries):
            try:
                if self.client_type == "ollama":
                    result = self._call_ollama(prompt, system_instruction, temperature)
                else:
                    result = self._call_gemini(prompt, system_instruction, temperature)
                
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
                provider_name = "Ollama" if self.client_type == "ollama" else "Gemini"
                print(f"⚠️ {self.name} {provider_name} 調用失敗 (嘗試 {attempt + 1}/{max_retries}): {str(e)}")
                
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"   等待 {wait_time} 秒後重試...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"{self.name} {provider_name} 調用失敗: {str(e)}")
    
    def _call_ollama(self, prompt: str, system_instruction: str = None, 
                     temperature: float = 0.7) -> str:
        """調用 Ollama 本地模型"""
        messages = []
        
        # 添加系統指令
        if system_instruction:
            messages.append({
                "role": "system",
                "content": system_instruction
            })
        
        # 添加用戶提示
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        # 調用 Ollama
        response = self.ollama_client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature,
                "num_ctx": config.OLLAMA_NUM_CTX,
                "num_predict": config.OLLAMA_NUM_PREDICT,
                "top_p": 0.9,
                "top_k": 40
            },
            stream=False  # 暫不使用流式輸出以簡化處理
        )
        
        return response['message']['content']
    
    def _call_gemini(self, prompt: str, system_instruction: str = None, 
                     temperature: float = 0.7) -> str:
        """調用 Gemini API"""
        response = self.gemini_client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "system_instruction": system_instruction if system_instruction else ""
            }
        )
        
        return response.text
    
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
