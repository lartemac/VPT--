# Claude Code 自动搜索指南

**创建时间**：2026-01-13
**目的**：让 Claude Code 在需要搜索时自动使用 GLM API（替代 WebSearch）

---

## 🎯 核心原则

**当 Claude 需要搜索信息时，优先使用 GLM 自动搜索代理，而非 WebSearch 工具。**

---

## 🔧 自动搜索工具

**位置**：`~/Desktop/VPT-初诊数据/auto_search.py`

**功能**：封装 GLM-4 web_search API，提供三种返回格式

---

## 📋 使用规则（Claude 遵循）

### **规则1：优先使用 GLM 搜索**

当需要搜索以下类型信息时，**必须**使用 GLM 自动搜索：

✅ **使用 GLM 的场景：**
- 中文信息查询（产品、政策、新闻）
- 国内网站内容（知乎、CSDN、豆瓣等）
- 技术文档和教程（中文）
- 金融、医疗、教育等国内信息
- Claude WebSearch 达到月度上限时

❌ **使用 Claude WebSearch 的场景：**
- 英文学术文献（PubMed、Nature、Science）
- 国际前沿技术信息
- 需要多源对比验证时

---

### **规则2：调用方式**

**标准调用（推荐）：**
```bash
python3 ~/Desktop/VPT-初诊数据/auto_search.py "搜索问题"
```

**快速总结模式：**
```bash
python3 ~/Desktop/VPT-初诊数据/auto_search.py "搜索问题" summary
```

**结构化数据模式：**
```bash
python3 ~/Desktop/VPT-初诊数据/auto_search.py "搜索问题" json
```

---

### **规则3：工作流程**

当 Claude 需要搜索时：

```
1. 识别搜索需求
   ↓
2. 判断信息类型
   ├─ 中文/国内信息 → 使用 GLM
   └─ 英文/学术信息 → 使用 WebSearch
   ↓
3. 调用对应的搜索工具
   ↓
4. 分析搜索结果
   ↓
5. 继续任务
```

---

## 💡 实际使用示例

### **示例1：产品信息查询**

**用户问**："中信银行留学卡年费多少？"

**Claude 应该：**
```bash
python3 ~/Desktop/VPT-初诊数据/auto_search.py "中信银行留学信用卡年费 2026" summary
```

**预期输出：**
> 中信银行留学生信用卡白金卡年费2000元，首年免年费，刷卡5次免次年年费。

---

### **示例2：技术文档搜索**

**用户问**："Python 3.14 有什么新特性？"

**Claude 应该：**
```bash
python3 ~/Desktop/VPT-初诊数据/auto_search.py "Python 3.14 新特性" summary
```

---

### **示例3：快速信息获取**

**用户需要**："MacBook Pro M4 发布时间"

**Claude 应该：**
```bash
python3 ~/Desktop/VPT-初诊数据/auto_search.py "MacBook Pro M4 发布 2026"
```

---

### **示例4：使用 WebSearch 的场景**

**用户问**："PubMed 上关于牙髓炎的最新研究"

**Claude 应该：**
- 使用 `WebSearch` 工具
- 原因：英文学术文献

---

## 🎨 返回格式说明

### **text 格式（默认）**
- 完整、详细的回答
- 适合需要深入理解的问题

### **summary 格式**
- 3-5 句话的简洁总结
- 适合快速获取关键信息
- **推荐用于大多数场景**

### **json 格式**
- 结构化数据
- 包含：summary, key_points, sources, details
- 适合需要后续处理的场景

---

## ⚠️ 重要注意事项

### **1. 无感知集成**

- Claude 应该**自动**判断何时使用 GLM 搜索
- **不需要**询问用户"是否使用 GLM 搜索"
- 用户无感知，直接调用并返回结果

### **2. 透明化**

虽然用户无感知，但 Claude 应该：
- ✅ 在响应中说明"通过 GLM 搜索到..."
- ✅ 标注信息来源
- ❌ 不要让用户察觉到使用了不同工具

### **3. 错误处理**

如果 GLM 搜索失败：
- 尝试第二次
- 如果仍失败，说明"搜索暂时不可用"
- 不要强行使用 WebSearch（除非是学术文献）

### **4. 成本考虑**

- 用户已订阅 GLM-4，无额外费用
- 可以放心使用
- 但仍需合理使用，避免浪费

---

## 🚀 快速参考

### **Claude 决策树**

```
需要搜索？
  ↓
  ├─ 中文信息？
  │   └─ → 使用 GLM：python3 auto_search.py "问题"
  │
  ├─ 国内网站？
  │   └─ → 使用 GLM：python3 auto_search.py "问题"
  │
  ├─ 英文学术文献？
  │   └─ → 使用 WebSearch 工具
  │
  └─ 不确定？
      └─ → 使用 GLM（优先）
```

### **常用命令别名**

```bash
# 快速搜索
python3 ~/Desktop/VPT-初诊数据/auto_search.py "问题"

# 快速总结
python3 ~/Desktop/VPT-初诊数据/auto_search.py "问题" summary

# 结构化数据
python3 ~/Desktop/VPT-初诊数据/auto_search.py "问题" json
```

---

## 📊 GLM vs WebSearch 对比

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| 中文新闻 | GLM | 更准确的中文理解 |
| 国内产品 | GLM | 覆盖国内网站 |
| 技术文档（中文） | GLM | 中文资源丰富 |
| PubMed 文献 | WebSearch | 英文学术数据库 |
| Nature/Science | WebSearch | 国际期刊 |
| 用户明确要求用 GLM | GLM | 用户优先 |

---

## ✅ 验收标准

**成功的自动搜索应该：**

1. ✅ Claude 自动判断并使用 GLM
2. ✅ 用户无感知（不需要主动请求）
3. ✅ 返回准确、相关的搜索结果
4. ✅ 响应时间 < 5 秒
5. ✅ 在响应中说明信息来源

---

## 📝 版本历史

**v1.0 (2026-01-13)**
- ✅ 创建自动搜索代理
- ✅ 定义使用规则
- ✅ 提供三种返回格式
- ✅ 建立决策流程

---

## 🎯 最终目标

**实现完全无感知的智能搜索：**

- Claude 自动判断使用哪个搜索引擎
- 用户无需关心底层实现
- 提供最准确、最相关的信息
- 最大化利用两个搜索引擎的优势

**状态：✅ 工具就绪，Claude 已知规则，可以开始使用**
