---
name: FastGPT 已清理
description: FastGPT 已于2026-05-05完全删除（容器+镜像+卷+本地文件D:\FastGPT），不再使用
type: project
originSessionId: ae47c039-7b09-453e-bdcb-c20fcda83775
---
## FastGPT 清理记录（2026-05-05）

### 已删除内容
- 12个 FastGPT 相关 Docker 容器（全部停止并删除）
- 10个 FastGPT 镜像（约 5.5GB 虚拟大小）
- 5个 FastGPT 卷（mongo/pg/redis/minio/aiproxy_pg）
- 本地文件 D:\FastGPT\ 整个目录
- Docker vhdx 从 31.66GB 压缩到 25.35GB，C盘回收约 6GB

### 保留
- Docker Desktop 仅用于运行 GPT Academic

## Why: 用户确认 FastGPT 没有存在必要，要求完全清理以释放 C 盘空间
## How to apply: 不再提及 FastGPT 相关操作，Docker 仅服务于 GPT Academic
