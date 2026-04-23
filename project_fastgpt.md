---
name: FastGPT 知识库 RAG 修复完成
description: FastGPT v4.14.10.2 本地部署，知识库搜索空 Cites 问题已修复，需验证对话功能
type: project
---

## FastGPT 当前状态（2026-04-24）

### ⚠️ 下次启动必须做：验证 FastGPT 对话功能
- 打开 http://localhost:4000，用 root/1234 登录
- 进入 "talk" 应用，发送消息测试知识库搜索是否返回引用
- 如果 429 限流，等待几分钟后重试
- **如果搜索结果仍然空 Cites，说明补丁丢失，需要重新执行修复步骤**

### 访问信息
- **地址**: http://localhost:4000
- **用户名/密码**: root / 1234
- **MinIO 控制台**: http://localhost:9001 (minioadmin/minioadmin)
- **AI Proxy 控制台**: http://localhost:4001

### 安装信息
- **版本**: FastGPT v4.14.10.2
- **路径**: D:\FastGPT\
- **端口**: 4000(主服务), 4001(AI Proxy), 9000/9001(MinIO)

---

## 知识库搜索空 Cites 修复过程（2026-04-24）

### 问题描述
用户上传《凉山叹息.docx》到知识库后，聊天时模型回复中 `<Cites>` 始终为空，无法引用知识库内容。跨 3 个会话反复排查。

### 根本原因
FastGPT 的 embedding 调用代码没有把 `dimensions: 1536` 参数传给智谱 embedding-3 API。

**完整链路分析：**
1. `config.json` 中 vectorModel 配置了 `dbConfig: {dimensions: 1536}` 和 `queryConfig: {dimensions: 1536}`
2. 但模型注册代码（`chunks/54038.js`）从 AI Proxy 加载模型时，**只为 LLM 类型合并 defaultConfig**，embedding 模型的 dbConfig/queryConfig 被丢弃
3. embedding 调用代码（`chunks/51445.js`）中 `...a.defaultConfig` 和 `...a.dbConfig` 运行时都是 `undefined`
4. 智谱 embedding-3 API 无 dimensions 参数时返回 2048 维向量
5. FastGPT 将 2048 维截断为 1536 维（砍掉后 512 位），严重破坏向量质量
6. 搜索时余弦相似度极低，所有结果被过滤掉，返回空 Cites

### 修复方案
**1. 源码补丁** — 在 `51445.js` 的 `embeddings.create` 调用中硬编码 `dimensions:1536`
- 文件位置：容器内 `/app/projects/app/.next/server/chunks/51445.js`
- 补丁文件：`D:\FastGPT\patches\51445.js`
- 修改内容：`encoding_format:"float"` → `encoding_format:"float",dimensions:1536`
- 通过 docker-compose.yml volumes 挂载，容器重建也不丢失

**2. 重新向量化** — 使用 `D:\FastGPT\revectorize5.py` 重建全部 520 条向量
- 脚本调用 embedding API 时显式传 `dimensions:1536`
- 每条向量 1536/1536 非零值（之前是 1024 非零 + 512 零填充）
- 插入 PG 后用 RETURNING id 获取自增 ID
- 更新 MongoDB `dataset_datas.indexes[N].dataId` 为新的 PG 行 ID

**3. docker-compose.yml 修改**
```yaml
# fastgpt-app 的 volumes 中添加：
- ./patches/51445.js:/app/projects/app/.next/server/chunks/51445.js
```

### 验证结果
- 520 条向量全部正确（1536 非零，末尾不再全零）
- MongoDB dataId 映射正确（1667-2186）
- API 测试：知识库搜索返回 83 条引用（quoteList 非空）
- 相似度得分正常（最高 0.464）
- GLM-4.7 返回 429 限流，暂未获得完整对话回复（需等限流解除后验证）

### 当前数据状态
- **数据集**: LarteSelf1 (ObjectId: 69e4fe7cd2525a331a5f1285)
- **集合**: 凉山叹息.docx (ObjectId: 69ea369b4fdf1187444d12db)，260 条 dataset_datas，520 个 index
- **PG 向量**: modeldata 表中 520 行（id: 1667-2186）
- **应用**: talk (ObjectId: 69e8f46e1e8ac4447d51255f)

### 如果需要重新修复的步骤
1. 确认补丁文件存在：`D:\FastGPT\patches\51445.js` 包含 `dimensions:1536`
2. 确认 docker-compose.yml 挂载了补丁文件
3. `docker compose up -d` 启动
4. 验证：`docker exec fastgpt-app sh -c "grep -o 'dimensions:1536' /app/projects/app/.next/server/chunks/51445.js"`
5. 如补丁丢失：`docker exec fastgpt-app sh -c "sed -i 's/encoding_format:\"float\"/encoding_format:\"float\",dimensions:1536/g' /app/projects/app/.next/server/chunks/51445.js"`
6. 删除旧向量并重新上传文档，或使用 `revectorize5.py` 手动重建

### 关键 Docker 凭据
- MongoDB: myusername / mypassword，数据库 fastgpt
- PostgreSQL: username / password，数据库 postgres
- AI Proxy PG: postgres / aiproxy，数据库 aiproxy
- AI Proxy Token: fastgpt-aiproxy-admin-2026
- ROOT_KEY: fastgpt-xxx
