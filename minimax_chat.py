#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


ENV_FILES = (Path(".env"), Path("api_minimax.env"))


def load_env() -> None:
    for path in ENV_FILES:
        if not path.exists():
            continue

        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} belum diisi di .env atau api_minimax.env.")
    return value


def chat(prompt: str) -> str:
    api_key = require_env("MINIMAX_API_KEY")
    base_url = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.io/v1").rstrip("/")
    model = os.environ.get("MINIMAX_MODEL", "MiniMax-M2.7")
    max_tokens = int(os.environ.get("MINIMAX_MAX_TOKENS", "1200"))

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }

    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"MiniMax API error {error.code}: {body}") from error

    return data["choices"][0]["message"]["content"]


def strip_thinking(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Kirim prompt ke MiniMax Chat Completions API.")
    parser.add_argument(
        "--show-thinking",
        action="store_true",
        help="Tampilkan output mentah termasuk blok <think> jika ada.",
    )
    parser.add_argument("prompt", nargs="+", help="Prompt yang ingin dikirim.")
    args = parser.parse_args()

    load_env()
    prompt = " ".join(args.prompt)

    try:
        answer = chat(prompt)
        print(answer if args.show_thinking else strip_thinking(answer))
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
