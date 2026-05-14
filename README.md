# 🔗 URL Shortener

短链接生成器 CLI，支持多个免费 API。

## 使用

```bash
python3 shortener.py "https://github.com/example/repo"
python3 shortener.py "https://example.com" -s tinyurl
python3 shortener.py "https://example.com" -a  # 所有服务
```

## 支持的服务

- is.gd（默认）
- v.gd
- TinyURL

## 特性

- 零依赖
- 多服务对比
- Python 3.6+
