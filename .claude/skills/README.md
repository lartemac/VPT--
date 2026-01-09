# Polymath Skills 体系

> 为 FattyTiger 量身定制的跨领域 AI 技能集合

## 📖 什么是 Skills？

**Skills（技能）** 是 Claude Code 的领域知识文档，相当于"专家助手"的"大脑"。每个 Skill 包含特定领域的专业知识、最佳实践和代码模板，让 Claude 能够像专业工程师一样工作。

### 简单理解

| 概念 | 类比 | Skills 的作用 |
|------|------|--------------|
| **Claude Code** | 大脑 | AI 助手本身 |
| **Skills** | 专业知识库 | 装入大脑的专业知识 |
| **Polymath** | 多面手 | 跨领域专家系统 |

---

## 🎯 Polymath 模式说明

**Polymath（博学家）** 模式是 FattyTiger 的专属 AI 助手，根据上下文自动切换三种模式：

### Mode A：教育模式（Teaching Mode）

**触发关键词**：孩子、儿子、教学、学习

**适用场景**：
- 教孩子编程（8岁儿童 Python 启蒙）
- 双语教学（中文 + 英文）
- 简单易懂、生动有趣

**相关 Skill**：
- `python-tutoring` - Python 编程教学助手

---

### Mode B：开发模式（Development Mode）

**触发关键词**：小程序、API、交易、游戏

**适用场景**：
- 微信/支付宝小程序开发
- 量化交易系统开发
- 游戏逻辑开发（7局4胜制）

**相关 Skills**：
- `weapp-development` - 微信小程序全栈开发
- `quantitative-trading` - 量化交易系统开发
- `game-logic` - 游戏逻辑（7局4胜制、流局判定）

---

### Mode C：科研模式（Research Mode）

**触发关键词**：牙髓、VPT、国自然、活髓保存、标书、文献

**适用场景**：
- 医学科研（牙体牙髓病学）
- 国自然标书撰写
- 权威文献检索（PubMed/CNKI）
- 统计分析与科研设计

**相关 Skill**：
- `medical-research` - 医学科研辅助

---

## 📚 Skills 详解

### 1. medical-research（医学科研）

**专业领域**：口腔医学、牙体牙髓病学、VPT（活髓治疗）

**核心功能**：
- 📄 文献检索：PubMed/CNKI 高质量文献检索
- 📝 标书撰写：国自然（NSFC）标书结构模板
- 📊 统计分析：样本量计算、统计方法选择
- 🔬 科研设计：RCT、队列研究、病例对照研究

**关键特性**：
- 优先引用高影响因子期刊（IF > 10）
- 优先近3年文献（2022-2025）
- 提供完整标书模板（4000字示例）

**代码示例**：
```r
# 样本量计算（G*Power）
t检验（两组比较）
- 效应量：d = 0.5（中等效应）
- α = 0.05，Power = 0.80
- 所需样本量：每组64例
```

**触发关键词**：
```
牙髓、VPT、活髓保存、根管治疗
国自然、NSFC、标书、基金
文献、PubMed、CNKI、SCI
统计、SPSS、R语言、数据分析
```

---

### 2. weapp-development（微信小程序开发）

**技术栈**：WXML + WXSS + JavaScript + 云开发

**核心功能**：
- 🎨 前端开发：页面设计、UI/UX 规范
- ☁️ 云开发：云函数、云数据库、云存储
- 👤 用户系统：登录、权限、数据采集
- 📤 数据导出：CSV 导出、报表生成

**关键特性**：
- 完整项目结构规范
- 医学科研数据采集系统示例
- 安全规则配置
- 组件库推荐（WeUI、TDesign）

**代码示例**：
```javascript
// 云函数：保存患者数据
exports.main = async (event, context) => {
  const db = cloud.database()
  const res = await db.collection('patients').add({
    data: {
      ...event,
      createTime: db.serverDate()
    }
  })
  return { success: true, _id: res._id }
}
```

**触发关键词**：
```
小程序、微信、云开发
wxml、wxss、云函数、云数据库
登录、支付、上传图片
数据采集、导出CSV
```

---

### 3. quantitative-trading（量化交易）

**核心原则**：安全第一、风险控制优先、数据驱动

**核心功能**：
- 🔐 API 对接：OKX、Binance 等 100+ 交易所
- 📊 策略开发：网格交易、动量策略、定投策略
- 📈 回测系统：历史数据回测、性能评估
- ⚠️ 风险管理：仓位管理、止损止盈、风险控制

**关键特性**：
- **禁止硬编码私钥**：使用环境变量（.env 文件）
- **仓位管理**：单次交易风险不超过 2%
- **止损止盈**：自动计算止损/止盈价格
- **最大回撤**：设置 20% 最大回撤阈值

**代码示例**：
```python
# 环境变量配置（.env 文件，禁止提交到 Git）
OKX_API_KEY=your_api_key_here
OKX_SECRET_KEY=your_secret_key_here
OKX_PASSPHRASE=your_passphrase_here
OKX_SANDBOX=true  # true: 测试环境

# 使用示例
exchange = OKXExchange(
    api_key=os.getenv('OKX_API_KEY'),
    secret_key=os.getenv('OKX_SECRET_KEY'),
    passphrase=os.getenv('OKX_PASSPHRASE'),
    sandbox=True
)
```

**触发关键词**：
```
交易、OKX、Binance、API
量化、策略、回测
K线、技术指标、止损、止盈
```

---

### 4. game-logic（游戏逻辑）

**核心规则**：7局4胜制 + 流局判定

**核心功能**：
- 🎮 比赛管理：7局4胜制流程控制
- ⚖️ 胜负判定：三级优先级系统
- 🔄 流局处理：特殊规则判定
- 📊 状态管理：比赛状态、局状态

**胜负优先级（不可更改）**：
```
1. 正常击杀（最高优先级）
   ↓
2. 流局判定（中等优先级）
   ↓
3. 平局（最低优先级）
```

**关键特性**：
- 严格遵循优先级规则
- 完整的边界情况处理
- 测试用例覆盖

**代码示例**：
```python
# 胜负判定
def judge_round(player_a_score, player_b_score, is_flow_game):
    # 优先级1：正常击杀
    if player_a_score > 0 and player_b_score == 0:
        return RoundResult.NORMAL_KILL

    # 优先级2：流局判定
    if is_flow_game or (player_a_score == 0 and player_b_score == 0):
        return RoundResult.FLOW_GAME

    # 优先级3：平局
    return RoundResult.DRAW
```

**触发关键词**：
```
游戏、比赛、竞技
7局4胜、BO7、Best of 7
流局、麻将、和局、平局
```

---

### 5. python-tutoring（Python 编程教学）

**教学理念**：简单易懂、双语教学、趣味优先

**核心功能**：
- 👶 儿童编程启蒙（8岁起）
- 🌏 双语教学（中文 + 英文）
- 🎮 游戏化学习
- 📝 项目制教学

**教学内容**：
1. 认识 Python（Hello World）
2. 变量（盒子比喻）
3. 数据类型（字符串、整数、小数、布尔）
4. 输入输出（交互式程序）
5. 数学运算（加减乘除）
6. 条件判断（if-else）
7. 循环（for、while）
8. 列表（收集物品）

**关键特性**：
- 使用生活化类比（变量=盒子、循环=重复做事）
- 双语对照（每个概念都有英文翻译）
- 可视化展示（图形、动画）
- 实战项目（猜数字、计算器、石头剪刀布）

**代码示例**：
```python
# 变量教学（使用类比）
name = "Tom"          # 名字盒子
age = 8               # 年龄盒子
height = 130          # 身高盒子

# Variable = A box that holds information
name = "Tom"          # Name box
age = 8               # Age box
height = 130          # Height box
```

**触发关键词**：
```
孩子、儿子、8岁
学编程、Python、教学
编程启蒙、儿童编程
```

---

## 🚀 如何使用 Skills

### 自动激活

当您在对话中提及特定关键词时，相应的 Skill 会自动激活：

```
您："我想开发一个微信小程序来收集患者数据"
Claude：[自动激活 weapp-development Skill]
```

### 手动激活

您也可以显式要求使用某个 Skill：

```
您："请使用 python-tutoring Skill 教我写一个猜数字游戏"
Claude：[激活 python-tutoring Skill]
```

---

## 📂 目录结构

```
.claude/
└── skills/
    ├── README.md                    # 本文件
    ├── medical-research/
    │   └── SKILL.md                 # 医学科研
    ├── weapp-development/
    │   └── SKILL.md                 # 微信小程序开发
    ├── quantitative-trading/
    │   └── SKILL.md                 # 量化交易
    ├── game-logic/
    │   └── SKILL.md                 # 游戏逻辑
    └── python-tutoring/
        └── SKILL.md                 # Python 教学
```

---

## 🔄 Skills 之间的协作

Skills 可以相互配合完成复杂任务：

### 示例 1：开发医学科研小程序
```
1. medical-research Skill：设计科研数据采集方案
2. weapp-development Skill：开发小程序前端和云函数
3. python-tutoring Skill：学习 Python 进行数据分析
```

### 示例 2：开发量化交易系统
```
1. quantitative-trading Skill：开发交易策略
2. weapp-development Skill：开发监控小程序
3. game-logic Skill：处理胜负判定逻辑
```

---

## 🛠️ 技术栈总览

| Skill | 主要技术 | 语言/框架 |
|-------|---------|----------|
| medical-research | 统计分析、文献检索 | R、Python、SPSS |
| weapp-development | 小程序开发 | WXML、WXSS、JS、云开发 |
| quantitative-trading | 交易系统开发 | Python、ccxt、pandas |
| game-logic | 游戏逻辑 | Python、状态机 |
| python-tutoring | 编程教学 | Python（基础） |

---

## 📝 Skill 开发规范

### Skill.md 文件格式

每个 Skill 必须包含：

```markdown
---
name: skill-name
description: 简短描述（含触发关键词）
allowed-tools: 工具列表
model: 模型选择（sonnet/opus/haiku）
---

# Skill 标题

## 何时激活此 Skill
触发关键词列表

## 核心功能
功能列表

## 代码示例
具体代码

## 常见问题
Q & A
```

### 命名规范

- **文件名**：小写字母 + 连字符（如 `medical-research`）
- **目录名**：与文件名一致
- **SKILL.md**：必须大写，固定文件名

---

## 🎓 学习路径

### 新手入门
1. **第一步**：使用 `python-tutoring` 学习 Python 基础
2. **第二步**：使用 `weapp-development` 开发第一个小程序
3. **第三步**：根据需求选择其他 Skills

### 进阶学习
1. **医学科研方向**：`medical-research` → `weapp-development`（数据采集系统）
2. **金融量化方向**：`quantitative-trading` → `game-logic`（策略逻辑）
3. **教育培训方向**：`python-tutoring`（教学方法）

---

## 📊 Skills 统计

| Skill | 行数 | 代码示例 | 主要应用 |
|-------|------|---------|---------|
| medical-research | ~600 | R、Python | 医学科研、国自然 |
| weapp-development | ~800 | JS、WXML | 小程序开发 |
| quantitative-trading | ~700 | Python、ccxt | 量化交易 |
| game-logic | ~500 | Python | 游戏开发 |
| python-tutoring | ~900 | Python（基础） | 编程教育 |

**总计**：约 3500 行专业内容，200+ 代码示例

---

## 🔄 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-01-10 | 创建完整 Polymath Skills 体系（5个 Skills） |

---

## 💡 使用建议

### ✅ 推荐做法
- 充分利用 Skills 的专业知识
- 多个 Skills 配合使用
- 参考 Skills 中的代码示例
- 遵循 Skills 中的最佳实践

### ❌ 避免做法
- 不要同时激活太多 Skills（会混乱）
- 不要忽略 Skills 中的安全警告
- 不要在 Skills 范围外强行使用

---

## 📮 反馈与改进

如果您在使用 Skills 时有任何建议或发现问题，欢迎提出改进意见！

**改进方向**：
- 添加新的 Skills
- 优化现有 Skills 内容
- 增加更多代码示例
- 完善跨 Skill 协作

---

**最后更新**：2026-01-10
**维护者**：FattyTiger
**版本**：v1.0.0
**许可**：MIT License
