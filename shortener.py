#!/usr/bin/env python3
"""短链接生成器 CLI - 使用多个免费 API"""
import argparse
import json
import sys
import urllib.request
import urllib.parse

SERVICES = {
    "isgd": {
        "name": "is.gd",
        "url": "https://is.gd/create.php?format=json&url={url}",
        "extract": lambda d: d.get("shorturl", "")
    },
    "vgd": {
        "name": "v.gd", 
        "url": "https://v.gd/create.php?format=json&url={url}",
        "extract": lambda d: d.get("shorturl", "")
    },
    "tinyurl": {
        "name": "TinyURL",
        "url": "https://tinyurl.com/api-create.php?url={url}",
        "extract": lambda d: d if isinstance(d, str) else ""
    },
}

def shorten(url, service="isgd"):
    svc = SERVICES.get(service)
    if not svc:
        return f"❌ 未知服务: {service}"
    api_url = svc["url"].format(url=urllib.parse.quote(url, safe=''))
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode()
            try:
                result = json.loads(data)
            except json.JSONDecodeError:
                result = data
            short = svc["extract"](result)
            return short if short else f"❌ {svc['name']} 返回异常: {data[:100]}"
    except Exception as e:
        return f"❌ {svc['name']} 请求失败: {e}"

def main():
    parser = argparse.ArgumentParser(description="短链接生成器")
    parser.add_argument("url", help="要缩短的 URL")
    parser.add_argument("-s", "--service", default="isgd", choices=SERVICES.keys(), help="API 服务 (默认: isgd)")
    parser.add_argument("-a", "--all", action="store_true", help="查询所有服务")
    args = parser.parse_args()
    
    if args.all:
        for name, svc in SERVICES.items():
            result = shorten(args.url, name)
            print(f"  {svc['name']}: {result}")
    else:
        result = shorten(args.url, args.service)
        print(result)

if __name__ == "__main__":
    main()
