---
name: VPT微信小程序云开发项目
description: 微信小程序VPT/RCT临床数据采集与统计分析项目，四页面+四云函数+三数据库集合
type: project
---

# VPT 微信小程序云开发项目

**项目位置**：`~/WeChatProjects/82671230weapp`（微信开发者工具项目，AppID: wx45677f091c824d9e）
**GitHub 仓库**：`lartemac/82671230weapp`（独立于 VPT-- 仓库）
**技术栈**：微信云开发 CloudBase（原生），非第三方框架

## v2.0 迭代（2026-09-02）：统计分析模块
- 数据模型从"每用户一条记录"升级为"一个患者一条记录、可录入多例"
- 临床字段：治疗组别(VPT/RCT)、年龄、性别、牙位类型、盖髓材料、术后VAS评分、随访月数、最终结局(成功/失败/失访)
- 新增 `pages/stats` 统计分析页 + `statsEngine` 云函数

## 页面
- `pages/login` — 微信一键登录（getPhoneNumber 绑定手机号）
- `pages/index` — 患者列表 + 临床数据表单（新增/编辑），保存到 clinical_records
- `pages/stats` — 统计分析（3 卡片：KM 生存分析 / 卡方·Fisher / Mann-Whitney U）
- `pages/logs` — 操作日志（管理员看所有用户修改日志）

## 云函数
- `login` — 获取 openid + 解析手机号，写入 user_profiles
- `submitForm` — 多例患者记录新增/更新；修改时写 audit_logs 审计日志
- `statsEngine` — 统计引擎（KM+Log-rank、卡方/Fisher精确、Mann-Whitney U，纯 JS 算法已用标准值验证）
- `getLogs` — 校验 ADMIN_OPENIDS 后返回 audit_logs

## 数据库集合
- `user_profiles`（用户资料：openid/phone/role）
- `clinical_records`（临床记录，含 v2.0 临床字段）
- `audit_logs`（审计日志：修改前/后数据）

## 临床字段（clinical_records）
- name 姓名、recordId 诊疗编号、treatmentGroup(VPT/RCT)、age 年龄、gender(male/female)
- toothType(观察位点编号，如16/21/36)、material(MTA/iRoot/other)
- vasScore(0-10)、followUpMonth 随访月、outcome(success/failure/lost)、note 备注

## 部署状态
- v1.0：环境 `cloud1-d6g2e0yep481068ea`、三集合、三云函数、管理员 openid 均已配置完成
- v2.0：已开发完成，UI 已脱敏；submitForm/statsEngine 云函数需上传部署
- 已建立独立 Git 仓库 `lartemac/82671230weapp` 并推送（2026-09-02）

## 踩坑记录
- openid 手填时把大写 `I` 误填成小写 `l`（或反之）导致"无权限"——getLogs 已加 currentOpenid 对比排查功能
- 云函数 `db.collection().add()` 不会自动写 `_openid`，前端直接查库在"仅创建者可读写"下读不到 → 列表改走 submitForm 云函数 `action=list` 解决

## 注意事项
- 数据库权限保持默认"仅创建者可读写"
- cloud.openapi.phonenumber.getPhoneNumber 为云调用（config.json 已声明权限）
- statsEngine 单次最多读 1000 条，数据量更大需分页
- 旧 v1.0 数据缺新字段，需重新编辑补充后才能纳入统计
- pages/example 与 quickstartFunctions 为模板遗留，保留不影响

## UI 脱敏准则（强制执行，2026-09-02 起）
项目主体为个体工商户（类目：工具-办公），微信审核严格，所有 UI 层文字必须中性脱敏：
- 患者/患者姓名→记录对象/ID；诊疗/治疗/病例→观察/处置/课题记录
- VPT组 vs RCT组→Group V vs Group R；牙位→观察位点（填编号如16、21、36）
- VAS疼痛评分→舒适度评分；牙髓坏死/失败→终点事件发生；牙髓存活率→观察终点存活率
- 材料名（MTA、iRoot BP Plus）可保留；代码层变量名/字段名保持专业命名不变
- 已脱敏：login/index/stats 页面、app.json 标题、submitForm 校验提示
