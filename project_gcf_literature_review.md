---
name: GCF龈沟液文献综述项目
description: 9篇GCF文献PDF→opendataloader-pdf转换→HTML报告+高清PNG图表导出（2026-05-11完成）
type: project
---

## 项目概况

- 日期：2026-05-11
- 平台：macOS（arm64）
- 工作文件夹：~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/vira9961_bfbe/msg/file/2026-05/

## 完成内容

1. macOS上安装了JDK 17（Temurin 17.0.19）+ opendataloader-pdf
   - JAVA_HOME 已写入 ~/.zshrc
   - 新终端自动加载

2. 9篇GCF龈沟液相关PDF文献转换为MD并深入阅读：
   - PH.pdf, 正畸-免疫.pdf, 图谱.pdf, 龋齿mmp9龈沟液.pdf
   - 氧化应激-International Journal of Dentistry...pdf, 龈沟液综述3区.pdf
   - 三种材料牙髓.pdf, 特定人群龈沟液氧化应激.pdf, 唾液血液龈沟液筛查牙周炎.pdf

3. 生成HTML文献综合总结报告（GCF文献综合总结报告.html，620KB）
   - 围绕三个重点问题：研究目的/GCF指标价值、纳入标准/样本量/采样方法、机制图解释

4. 导出16张高清PNG图表（300dpi，横向版式，适合16:9 PPT）
   - 饼图、柱状图、ROC曲线、机制流程图、折线图等
   - 表格类：表1-5各有合并版（A/B旧版保留）

## 生成脚本（均在工作文件夹中）

- generate_report.py — HTML报告生成
- export_images.py — 16张图表导出
- merge_tables.py — 表3+表5合并版
- merge_tables12.py — 表1+表2合并版

## 图表修改历史

- 表1：行高3.8，列宽[0.11, 0.17, 0.30, 0.20]，每格≤3行
- 表2：行高3.8，列宽[0.11, 0.12, 0.26, 0.26, 0.07]，样本量/排除标准≤3行
- 表3：文献列宽0.13
- 表5：行高3.15，列宽[0.126, 0.08, 0.30, 0.088, 0.12, 0.20]
- 所有表"文献"列统一为"作者+年份+期刊名"格式

## macOS 环境备注

- 系统Python 3.9.6（Windows为3.14）
- 无Homebrew，JDK通过直接下载pkg安装
- matplotlib使用Agg后端，字体Arial Unicode MS
