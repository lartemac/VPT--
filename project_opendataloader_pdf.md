---
name: opendataloader-pdf 安装
description: PDF解析工具已安装（v2.4.1），JDK17装在D盘，需设置JAVA_HOME后使用
type: project
originSessionId: ae47c039-7b09-453e-bdcb-c20fcda83775
---
## opendataloader-pdf 安装信息（2026-05-05）

### 基本信息
- **版本**: 2.4.1
- **用途**: PDF文件解析为Markdown/文本/HTML，Benchmark #1（准确率0.907）
- **GitHub**: https://github.com/opendataloader-project/opendataloader-pdf

### 依赖
- **JDK 17（Eclipse Temurin）**: 安装在 `D:\Java\jdk-17.0.19+10`
- **JAVA_HOME**: 已设置为用户级环境变量指向 D 盘
- **PATH**: 已将 `D:\Java\jdk-17.0.19+10\bin` 添加到用户 PATH 最前面

### 使用方式
```python
import os
os.environ['JAVA_HOME'] = r'D:\Java\jdk-17.0.19+10'
from opendataloader_pdf import convert

# 转换单个PDF
result = convert(input_path="paper.pdf", output_dir="./output", format="markdown")

# 批量转换
result = convert(input_path=["a.pdf", "b.pdf"], output_dir="./output", format="markdown")
```

### 注意事项
- 每次使用前需确保 JAVA_HOME 指向 JDK 17（系统默认是旧版 Java 8）
- 安装路径在 D 盘，不占用 C 盘空间

## Why: 用户需要高质量PDF解析工具用于科研论文处理（NCCL项目等），opendataloader-pdf是开源免费的Benchmark #1方案
## How to apply: 当用户需要解析PDF论文时，使用此工具进行转换
