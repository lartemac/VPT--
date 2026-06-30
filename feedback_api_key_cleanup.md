---
name: feedback-api-key-cleanup
description: Git仓库API密钥安全清理规则（2026-06-30）
type: feedback
---

## API密钥安全清理（2026-06-30）

### 已修复的文件
| 文件 | 密钥类型 | 处理方式 |
|------|------|------|
| api_config.json | GLM/Google/Tushare | 占位符替代 |
| zhihu_mcp/search.py | 知乎Access Secret | 占位符替代 |
| zhihu_mcp/server.py | 知乎Access Secret | 占位符替代 |
| reference_zhipu_api_billing.md | 智谱双Key | 占位符替代 |
| project_zhihu_mcp.md | 知乎Secret | 占位符替代 |
| lessons.md | Tushare Token引用 | 占位符替代 |

### 关键教训
- api_config.json 虽在 .gitignore 中但因曾 git add 而被跟踪，.gitignore 对已跟踪文件无效
- DeepSeek和小米密钥未暴露（使用`<你的Key>`占位符），安全性好

### How to apply:
- 新项目首次提交前先用 `grep -r "sk-\|AIza\|token\|secret"` 检查
- API密钥统一通过环境变量或本地 .env 文件管理（不入Git）
- 模板文件使用 `YOUR_XXX` 占位符，真实Key另行保存
