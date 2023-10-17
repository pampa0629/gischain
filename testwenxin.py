
import requests
import json

API_KEY = "Gev6k0qO9OPatIHCu41iCKAS"
SECRET_KEY = "M6GqjYAVygDm7Fqee1ENZQ9KEpk4a8Qh"

def main():
        
    token = get_access_token()
    print(token)
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + token
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "hello"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
