---
name: project-zhihu-mcp
description: 知乎全网搜索作为通用联网搜索工具（优先级高于WebSearch），Bash直接调用，Windows/Mac双平台
metadata:
  type: project
---

## 通用联网搜索工具（2026-05-19）

### 核心规则
**任何工作中涉及联网搜索的场景，优先使用知乎全网搜索脚本，而非 WebSearch 或其他方式。**

### 使用方法
**Windows（Platform: win32）：**
```bash
"D:/Users/Administrator/miniconda3/python.exe" "D:/cc-github/zhihu_mcp/search.py" "关键词" 数量 模式
```

**macOS（Platform: darwin）：**
```bash
python3 ~/cc-github/zhihu_mcp/search.py "关键词" 数量 模式
```

### 两种搜索模式
| 模式 | 参数 | 说明 | 上限 |
|------|------|------|------|
| 全网搜索（默认） | `global` 或省略 | 搜索全平台内容 | 20条 |
| 站内搜索 | `zhihu` | 仅搜知乎站内 | 10条 |

### 优先级
知乎全网搜索 > WebSearch > 其他搜索方式

### API 参数
- Access Secret：`11d88bdc650f2bf0ad13bab266277fffc2a3383e`
- 每日额度：1000 次（站内+全网共享）
- 全网搜索 API：`https://developer.zhihu.com/api/v1/content/global_search`
- 站内搜索 API：`https://developer.zhihu.com/api/v1/content/zhihu_search`

### 方案演进历史
1. SSE 直连 MCP → 工具不出现（Z.ai 不支持用户自定义 MCP）
2. stdio 本地 MCP 代理 → 手动测试正常，但 Z.ai 不加载
3. **Bash 直接调用 search.py → 最终方案，已验证可用**

### Why: Z.ai 平台不支持用户自定义 MCP 服务器，且 GLM Coding Plan 的 MCP 额度太少
### How to apply: 每次需要联网搜索时，自动用 Bash 执行 search.py，根据平台选择正确的 python 路径
