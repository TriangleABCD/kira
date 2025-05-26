# kira
Knowledge Interactive Response Agent, 命令行大模型 Agent 工具

## 使用前配置

- 在 `src/kira.py` 的开头指定 kira 配置文件的位置，例如：

```python
kira_config_path = '/home/wyy/code/kira/config/kira.config.json'
```

- `kira.config.json` 配置示例：
```json
{
  "models": {
    "deepseek": {
        "url": "https://api.deepseek.com",
        "v3": "deepseek-chat",
        "r1": "deepseek-reasoner",
        "key_path": "/path/to/your/key/file",
        "key_key_path": "/path/to/your/key/key/path",
        "encrypt": true
    },
    "siliconflow": {
        "url": "https://api.siliconflow.cn/v1",
        "v3": "deepseek-ai/DeepSeek-V3",
        "r1": "deepseek-ai/DeepSeek-R1",
        "key_path": "/path/to/your/key/file",
        "key_key_path": "",
        "encrypt": false
    }
  },
  "model_choice": "deepseek"
}
```

## run

- 运行 kira
```bash
python src/kira.py
```

- 添加 `-s` 可以流式输出回答

- 添加 `-c` 选项可进入对话模式

- 添加 `-r` 选项可使用推理模式

- 更多参数可执行 `python src/kira.py --help` 查看

## 项目持久化

在一个项目的根目录下执行
```bash
kira --init
```
会在该项目的根目录新建一个 `.kira` 目录，其中将记录之后每次对话的内容，以时间命名。同时每次对话的历史会生成摘要，追加到 `.kira/summary.md` 中，每次的对话，模型都会事先读取其中内容。
