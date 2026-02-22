# Early Reach

Help indie developers find early users and collect feedback safely.

## Problem

Indie developers build products but struggle to find willing early users. Fear of public criticism leads to building in isolation, wasting time on unwanted features.

## Solution

Early Reach helps you:
- Generate platform-specific launch content (Product Hunt, Reddit, Twitter, etc.)
- Track your launches across different channels
- Collect and analyze user feedback systematically

## Installation


## Quick Start

1. Initialize your product:

2. Generate launch content:

3. Record a launch:

4. Add user feedback:

5. View feedback and generate reports:

## Commands

- `init` - Initialize product profile
- `generate` - Generate platform-specific launch content
- `launch` - Record a product launch
- `launches` - List all launches
- `add-feedback` - Add user feedback
- `feedbacks` - List all feedback
- `report` - Generate feedback analysis report

## Supported Platforms

- Product Hunt
- Reddit
- Twitter
- Hacker News
- Indie Hackers

## Data Storage

All data is stored locally in `.early-reach/` directory as JSON files.

## Tips

- Customize generated content before posting
- Be genuine and transparent in your launches
- Respond to all feedback promptly
- Use the report to identify patterns and prioritize features
# 安装依赖
pip install -r requirements.txt

# 初始化产品
python main.py init -n "MyApp" -d "Solve X problem"

# 生成发布文案
python main.py generate ProductHunt

# 记录发布
python main.py launch Reddit --url "https://..."

# 添加反馈
python main.py add-feedback -s "user@email.com" -c "Great tool!" -r 5

# 查看报告
python main.py report