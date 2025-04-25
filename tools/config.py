import os
import configparser

def load_config(config_file):
    # 这里修改为 config.ini 并把该ini文件中的key值改为自己的key
    os.environ["config_file"] = config_file
    config = configparser.ConfigParser()
    config.read(config_file)

    os.environ['glm_key'] = config.get("zhipu", "key")
    os.environ['qwen_key'] = config.get("qwen", "key")
    os.environ['wenxin_ak']  = config.get("wenxin", "ak")
    os.environ['wenxin_sk']  = config.get("wenxin", "sk")
    os.environ['text2sql_key']  = config.get("text2sql", "key")
    os.environ['gpt_key']  = config.get("gpt", "key")
    os.environ['deepseek_key']  = config.get("deepseek", "key")
