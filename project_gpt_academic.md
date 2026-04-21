---
name: GPT Academic 本地部署
description: GPT Academic (gpt_academic) Docker部署，智谱GLM API，端口12345，已上传20篇NCCL论文
type: project
originSessionId: ba60bf23-fe51-4ee2-8253-1c55887a0e86
---
## GPT Academic 部署状态（2026-04-22）：✅ 已部署运行

### 访问信息
- **地址**: http://localhost:12345
- **部署方式**: Docker Desktop + docker-compose
- **安装路径**: D:\gpt_academic\
- **镜像**: ghcr.io/binary-husky/gpt_academic_with_latex:master

### 当前配置
- **模型**: glm-4-flash（免费，原生API通道）
- **API Key**: ZHIPUAI_API_KEY（原生API通道Key）
- **端口映射**: 12345:12345
- **主题**: Default
- **并发数**: 5

### 待办：账户充值后升级模型
- 充值后改 `LLM_MODEL` 为 `glm-5.1`
- 改 `AVAIL_LLM_MODELS` 加入更多模型
- 重启容器：`docker compose down && docker compose up -d`

### NCCL研究进展
- 已上传20篇NCCL相关PDF论文（C:\Users\Administrator\Desktop\NCCL\）
- 批量总结PDF文档已完成
- 待提交7个研究问题：
  1. NCCL的定义及发病率
  2. NCCL的病损形态与病因的关联
  3. NCCL的临床分型
  4. NCCL的牙体预备量如何把控
  5. NCCL修复材料、酸蚀、粘接剂如何选择
  6. NCCL的修复策略
  7. 其他方面

### 界面操作备忘
- 输入区在页面**右上方**
- 函数插件在**左侧**
- 提交按钮下拉选项：常规对话/查互联网后回答/多模型对话/智能召回RAG/多媒体查询
- 常规对话模式即可用于研究问题

### Why: 评估了ARS/Claude Scientific Writer等工具后，只有GPT Academic支持智谱原生API直连
### How to apply: 用户充值智谱账户后，帮改配置升级到GLM-5.1
