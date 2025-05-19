import requests
import json
def get_response(messages):
    url = "http://127.0.0.1:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "qwen3:8b",
        "messages": messages
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=10)
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)
    return response

# 测试调用
messages = [{"role": "user", "content": "Hello"}]
response = get_response(messages)
