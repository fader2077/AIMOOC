# Health Check 測試腳本
# 用法: python test_health.py

import requests
import json

def test_health_check():
    """測試 /health 端點"""
    try:
        response = requests.get('http://localhost:5001/health', timeout=5)
        
        print(f"✅ 狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n📊 Health Check 結果:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 檢查關鍵字段
            assert data['status'] == 'healthy', "服務狀態異常"
            assert 'service' in data, "缺少服務名稱"
            assert 'version' in data, "缺少版本信息"
            
            print("\n✅ Health Check 測試通過！")
            return True
        else:
            print(f"❌ Health Check 失敗: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 連接失敗: {e}")
        return False

if __name__ == "__main__":
    test_health_check()
