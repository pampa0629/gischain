import os
import configparser

# 各大模型key的环境变量名 -> (配置段, 选项名) 的映射
KEY_MAPPINGS = {
    "glm_key": ("zhipu", "key"),
    "qwen_key": ("qwen", "key"),
    "wenxin_ak": ("wenxin", "ak"),
    "wenxin_sk": ("wenxin", "sk"),
    "text2sql_key": ("text2sql", "key"),
    "gpt_key": ("gpt", "key"),
    "deepseek_key": ("deepseek", "key"),
}

def load_config(config_file):
    # 这里修改为 config.ini 并把该ini文件中的key值改为自己的key
    os.environ["config_file"] = config_file
    config = configparser.ConfigParser()
    config.read(config_file)

    # 配置文件或配置段缺失时不崩溃，key置为空字符串；
    # 只有实际调用对应大模型时才会暴露key无效的问题
    for env_name, (section, option) in KEY_MAPPINGS.items():
        os.environ[env_name] = config.get(section, option, fallback="")
