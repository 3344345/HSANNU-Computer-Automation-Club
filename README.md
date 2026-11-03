# Chatbot

同学们好，这是一个单文件多轮对话 Chatbot，调用智谱 GLM API（OpenAI 兼容接口）。

## 环境要求

- Python 3.8+
- Git
- 一个智谱开放平台的 API Key

## 获取 API Key

1. 访问 https://open.bigmodel.cn
2. 注册并登录
3. 在控制台创建 API Key

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/你的用户名/chatbot.git
cd chatbot
```

### 2. 创建虚拟环境并安装依赖

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install requests
```

**macOS / Linux / Ubuntu**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests
```

或者直接运行一键脚本：

- Windows：双击 `setup.bat`
- macOS / Linux：`bash setup.sh`

### 3. 配置 API Key

复制 `.env.example` 为 `.env`：

**Windows**
```powershell
copy .env.example .env
```

**macOS / Linux**
```bash
cp .env.example .env
```

然后用编辑器打开 `.env`，填入你的 `CHATBOT_API_KEY`。

### 4. 运行

**Windows**
```powershell
py chatbot.py
```

**macOS / Linux**
```bash
python3 chatbot.py
```

输入 `exit` / `quit` / `退出` 结束对话。

## 配置项

所有配置在 `.env` 中修改，代码不需要动：

| 变量 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `CHATBOT_API_KEY` | 智谱 API Key | 无（必填） |
| `CHATBOT_API_URL` | API 端点 | `https://open.bigmodel.cn/api/paas/v4/chat/completions` |
| `CHATBOT_MODEL` | 模型名 | `glm-4-flash`（免费） |
| `CHATBOT_MAX_TOKENS` | 单次回复最大 token | `300` |
| `CHATBOT_TEMPERATURE` | 随机性，0–1 | `0.7` |
| `CHATBOT_TIMEOUT` | 请求超时秒数 | `30` |

想换更强模型，把 `CHATBOT_MODEL` 改成 `glm-4` 即可（付费）。

## 常见错误

| 错误 | 原因 | 解决 |
| :--- | :--- | :--- |
| `401` | Key 无效 | 检查 `.env` 中的 `CHATBOT_API_KEY` |
| `404` | URL 不完整 | 确认 URL 以 `/chat/completions` 结尾 |
| `429` | 请求太频繁 | 等一会儿再试，或换模型 |
| `连不上服务器` | 网络问题 | 检查网络连接 |