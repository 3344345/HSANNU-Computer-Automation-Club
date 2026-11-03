import os
import sys
import requests

ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


def load_env(path):
    """极简 .env 解析，零额外依赖。已存在的环境变量优先，不被覆盖。"""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


load_env(ENV_FILE)

API_KEY     = os.getenv("CHATBOT_API_KEY", "").strip()
API_URL     = os.getenv("CHATBOT_API_URL", "https://api.openai.com/v1/chat/completions").strip()
MODEL       = os.getenv("CHATBOT_MODEL", "gpt-4o-mini").strip()
MAX_TOKENS  = int(os.getenv("CHATBOT_MAX_TOKENS", "300"))
TEMPERATURE = float(os.getenv("CHATBOT_TEMPERATURE", "0.7"))
TIMEOUT     = int(os.getenv("CHATBOT_TIMEOUT", "30"))

EXIT_WORDS = {"exit", "quit", "退出"}


def chat(messages):
    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
        },
        timeout=TIMEOUT,
    )

    if resp.status_code != 200:
        hints = {
            401: "API Key 无效或未设置。",
            403: "没有权限访问该模型。",
            404: "API 地址或模型名不对。",
            429: "请求太频繁或额度用尽。",
        }
        hint = hints.get(resp.status_code, "服务器返回了错误。")
        raise RuntimeError(f"HTTP {resp.status_code} — {hint}")

    data = resp.json()
    if not data.get("choices"):
        raise RuntimeError("返回格式异常，没有 choices 字段。")

    return data["choices"][0]["message"]["content"]


def main():
    if not API_KEY:
        print("未设置 CHATBOT_API_KEY，请在 .env 中填写后重试。")
        sys.exit(1)

    messages = []

    while True:
        try:
            user = input("你：").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user.lower() in EXIT_WORDS:
            break
        if not user:
            continue

        messages.append({"role": "user", "content": user})

        try:
            reply = chat(messages)
        except requests.exceptions.Timeout:
            print("Bot：请求超时。")
            messages.pop()
            continue
        except requests.exceptions.ConnectionError:
            print("Bot：连不上服务器。")
            messages.pop()
            continue
        except Exception as e:
            print(f"Bot：{e}")
            messages.pop()
            continue

        print(f"Bot：{reply}")
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()