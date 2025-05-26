import json

class Config:
    def __init__(self, path):
        self.config_path = ''
        self.models = None
        self.model_choice = ''
        self.read_config_from_file(path)

    def read_config_from_file(self, path):
        try:
            with open(path, 'r') as file:
                config_data = json.load(file)
                self.models = config_data.get('models')
                self.model_choice = config_data.get('model_choice')
        except FileNotFoundError:
            print(f"配置文件 {path} 未找到，请检查路径是否正确。")
        except json.JSONDecodeError:
            print(f"配置文件 {path} 格式错误，无法解析为JSON。")
        except Exception as e:
            print(f"读取配置文件时发生错误：{e}")
