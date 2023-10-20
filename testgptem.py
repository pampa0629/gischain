import openai

openai.api_base = 'https://api.closeai-asia.com/v1' # 固定不变
gpt_key = 'sk-ohe7INluTagKkdGRXP2QGs14n0rhL7sKs5BMEJT41e0Ezwzm'
openai.api_key = gpt_key 


import numpy as np

# np array
def list2array(input):
    input = input["data"][0]["embedding"] 
    input = [float(x) for x in input]
    input = np.array(input)
    return input
    # print(result)

def text2em(text):
    result= openai.Embedding.create(
    model="text-embedding-ada-002",
    input=text
    )
    return list2array(result)

# ============

import requests
import json

API_KEY = "Gev6k0qO9OPatIHCu41iCKAS"
SECRET_KEY = "M6GqjYAVygDm7Fqee1ENZQ9KEpk4a8Qh"

def baidu_em(text):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token=" + get_access_token()
    payload = json.dumps({
        "input": [
            text
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(response.text)
    return list2array(response)
    
    # print(response.text)
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
