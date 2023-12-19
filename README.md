# OperaGX Promo Generator

![License](https://img.shields.io/badge/license-MIT-blue)

## Overview

This Python script allows you to generate discord promo links. It utilizes threading for concurrent generation, and you have the option to use proxies to avoid rate limits.

## Features

- Multi-threaded promo code generation
- Proxy support to bypass rate limits
- User-friendly console interface

## How to Use

1. Install Dependencies:

```bash
pip install requests
```

2. Enter proxies in proxies.txt in the following format:
```ruby
username:password@host:port
```

3. Run the Script:
```bash
python gen.py
```
4. Enter the number of threads when prompted.

# Note
This script is intended for educational purposes only. Use it responsibly and respect Discord's & OperaGx's terms of service.
