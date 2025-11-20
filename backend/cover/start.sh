#!/bin/bash
# 图片拼图工具启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
VENV_PYTHON="$VENV_DIR/bin/python"

# 检查 virtualenv 是否安装
VIRTUALENV_CMD=""
if command -v virtualenv > /dev/null 2>&1; then
    VIRTUALENV_CMD="virtualenv"
elif python3 -m virtualenv --help > /dev/null 2>&1; then
    VIRTUALENV_CMD="python3 -m virtualenv"
else
    echo "virtualenv 未安装，正在安装..."
    python3 -m pip install --user virtualenv 2>/dev/null || python3 -m pip install virtualenv
    if command -v virtualenv > /dev/null 2>&1; then
        VIRTUALENV_CMD="virtualenv"
    elif python3 -m virtualenv --help > /dev/null 2>&1; then
        VIRTUALENV_CMD="python3 -m virtualenv"
    fi
fi

if [ -z "$VIRTUALENV_CMD" ]; then
    echo "错误: 无法找到 virtualenv 命令"
    exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "$VENV_DIR" ] || [ ! -f "$VENV_PYTHON" ]; then
    echo "虚拟环境不存在，正在创建..."
    cd "$SCRIPT_DIR"
    make install
    make setup
fi

# 激活虚拟环境并运行脚本
echo "启动拼图工具..."
cd "$SCRIPT_DIR"
"$VENV_PYTHON" puzzle.py "$@"
