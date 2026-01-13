#!/bin/bash
# GLM 搜索快捷启动脚本

cd ~/Desktop/VPT-初诊数据

if [ -z "$1" ]; then
    echo "用法："
    echo "  ./glm_search.sh \"搜索问题\""
    echo ""
    echo "示例："
    echo "  ./glm_search.sh \"中信银行信用卡年费\""
    echo "  ./glm_search.sh \"Python 最新版本\""
    exit 1
fi

python3 glm_search.py "$@"
