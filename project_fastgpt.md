---
name: FastGPT 知识库已安装完成
description: FastGPT v4.14.10.2 本地部署完成，Docker 容器全部运行正常，模型已激活4个，端口 4000
type: project
originSessionId: f0a8ddae-f2ed-45f8-9846-ba9bcca95865
---

## FastGPT 安装状态（2026-04-19）：✅ 全部完成

### 访问信息
- **地址**: http://localhost:4000
- **默认用户名**: root
- **默认密码**: 1234
- **MinIO 控制台**: http://localhost:9001 (minioadmin/minioadmin)
- **AI Proxy 控制台**: http://localhost:4001

### 安装详情
- **版本**: FastGPT v4.14.10.2
- **安装路径**: D:\FastGPT\
- **配置文件**: D:\FastGPT\docker-compose.yml + D:\FastGPT\config.json
- **端口映射**: 4000(主服务), 4001(AI Proxy), 9000/9001(MinIO)
- **Docker Desktop**: v4.68.0

### 模型配置（已激活 4 个）
- **glm-4-flash**: 聊天模型（智谱 AI）
- **glm-4-plus**: 聊天模型（智谱 AI）
- **embedding-3**: 向量化模型（智谱 AI）
- AI Proxy 中已配置智谱 API Key 和渠道

### 关键配置修复记录
1. **端口冲突**: Windows Hyper-V 保留 2978-3577 端口，主服务端口从 3000 改为 4000
2. **MinIO 外部端点**: 从 172.18.112.1:9000 改为 host.docker.internal:9000（hosts 文件已有映射）
3. **模型激活**: 通过 FastGPT 网页端 账号→模型提供商 配置，模型从 active:0 变为 active:4

### 容器清单（12个，全部健康）
| 容器 | 用途 |
|---|---|
| fastgpt-app | 主服务 |
| fastgpt-mongo | MongoDB 数据库 |
| fastgpt-pg | PostgreSQL 向量库 |
| fastgpt-redis | Redis 缓存 |
| fastgpt-minio | 对象存储 |
| fastgpt-plugin | 插件服务 |
| fastgpt-code-sandbox | 代码沙盒 |
| fastgpt-aiproxy | AI 代理 |
| fastgpt-aiproxy-pg | AI 代理数据库 |
| fastgpt-opensandbox-server | 开放沙盒 |
| fastgpt-volume-manager | 卷管理 |
| fastgpt-mcp-server | MCP 服务 |

### 下一步
- 创建知识库，上传文档测试
- 创建应用，测试对话功能
