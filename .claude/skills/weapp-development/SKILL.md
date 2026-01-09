---
name: weapp-development
description: 微信小程序全栈开发，包含前端设计、云开发、数据库设计、用户认证、支付功能。专长于医学科研数据采集系统。触发关键词：小程序、微信、云开发、云函数、数据库、wxml、wxss。
allowed-tools: Read, Write, Edit, Bash, Glob
model: sonnet
---

# 微信小程序开发 Skill

## 技术栈

### 前端
- **WXML**：微信标记语言（类似HTML）
- **WXSS**：微信样式表（类似CSS）
- **JavaScript/TypeScript**：业务逻辑
- **微信开发者工具**：v2.01.2510260

### 后端（云开发）
- **云数据库**：MongoDB 数据库
- **云函数**：Node.js 12+ 运行时
- **云存储**：文件存储（图片、PDF、视频）
- **云调用**：调用微信开放接口（支付、模板消息等）

## 何时激活此 Skill

当用户提及以下关键词时，自动激活此 Skill：
- **平台**：小程序、微信、微信开发者工具
- **技术**：wxml、wxss、云开发、云函数、云数据库
- **功能**：登录、支付、上传图片、数据采集、导出CSV

## 项目结构规范

```
my-miniprogram/
├── app.js                 # 小程序逻辑
├── app.json              # 小程序配置
├── app.wxss              # 全局样式
├── project.config.json   # 项目配置
├── sitemap.json          # 搜索配置
│
├── pages/                # 页面目录
│   ├── index/           # 首页
│   │   ├── index.wxml
│   │   ├── index.wxss
│   │   ├── index.js
│   │   └── index.json
│   ├── data-collection/ # 数据采集页
│   └── profile/         # 个人中心
│
├── components/           # 自定义组件
│   ├── data-form/       # 数据表单组件
│   └── chart-view/      # 图表组件
│
├── utils/               # 工具函数
│   ├── util.js          # 通用工具
│   └── request.js       # 网络请求封装
│
└── cloudfunctions/      # 云函数
    ├── login/           # 用户登录
    ├── export-csv/      # 导出CSV
    └── payment/         # 支付功能
```

## 核心功能实现

### 1. 用户登录与权限

#### 前端登录（获取 openid）
```javascript
// app.js
App({
  onLaunch() {
    this.login()
  },

  login() {
    wx.cloud.init({
      env: 'your-env-id' // 云开发环境ID
    })

    wx.cloud.callFunction({
      name: 'login'
    }).then(res => {
      this.globalData.openid = res.result.openid
      console.log('登录成功', res.result.openid)
    }).catch(err => {
      console.error('登录失败', err)
    })
  },

  globalData: {
    openid: null
  }
})
```

#### 云函数（login）
```javascript
// cloudfunctions/login/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()

  // 1. 获取用户信息
  const openid = wxContext.OPENID

  // 2. 查询数据库，判断是否新用户
  const db = cloud.database()
  const _ = db.command

  const userRes = await db.collection('users').where({
    openid: openid
  }).get()

  // 3. 新用户：创建用户记录
  if (userRes.data.length === 0) {
    await db.collection('users').add({
      data: {
        openid: openid,
        createTime: db.serverDate(),
        updateTime: db.serverDate(),
        role: 'user', // 默认角色
        // 可添加更多用户字段
        nickname: event.nickname || '',
        avatar: event.avatar || ''
      }
    })
  }

  // 4. 返回 openid
  return {
    openid: openid,
    isNewUser: userRes.data.length === 0
  }
}
```

### 2. 数据采集与存储

#### 前端表单（data-collection.wxml）
```xml
<form bindsubmit="onSubmit">
  <!-- 基本信息 -->
  <view class="form-group">
    <text>患者姓名</text>
    <input name="name" placeholder="请输入" />
  </view>

  <view class="form-group">
    <text>年龄</text>
    <input name="age" type="number" placeholder="请输入" />
  </view>

  <view class="form-group">
    <text>性别</text>
    <radio-group name="gender">
      <label><radio value="male" checked />男</label>
      <label><radio value="female" />女</label>
    </radio-group>
  </view>

  <!-- 单选按钮 -->
  <view class="form-group">
    <text>牙髓炎类型</text>
    <radio-group name="pulpitis_type">
      <label><radio value="reversible" />可复性牙髓炎</label>
      <label><radio value="irreversible" />不可复性牙髓炎</label>
      <label><radio value="necrosis" />牙髓坏死</label>
    </radio-group>
  </view>

  <!-- 多选按钮 -->
  <view class="form-group">
    <text>症状（可多选）</text>
    <checkbox-group name="symptoms">
      <label><checkbox value="pain" />自发痛</label>
      <label><checkbox value="cold" />冷刺激痛</label>
      <label><checkbox value="heat" />热刺激痛</label>
    </checkbox-group>
  </view>

  <!-- 图片上传 -->
  <view class="form-group">
    <text>上传X光片</text>
    <button type="default" bindtap="chooseImage">选择图片</button>
    <image wx:if="{{imageUrl}}" src="{{imageUrl}}" mode="aspectFill" />
  </view>

  <!-- 提交按钮 -->
  <button formType="submit" type="primary">提交数据</button>
</form>
```

#### 前端逻辑（data-collection.js）
```javascript
Page({
  data: {
    imageUrl: ''
  },

  // 选择图片并上传到云存储
  chooseImage() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: res => {
        const tempFilePath = res.tempFilePaths[0]

        // 上传到云存储
        const cloudPath = `xray/${Date.now()}-${Math.floor(Math.random() * 1000)}.jpg`

        wx.cloud.uploadFile({
          cloudPath: cloudPath,
          filePath: tempFilePath,
          success: res => {
            this.setData({
              imageUrl: res.fileID // 云文件ID
            })
            wx.showToast({ title: '上传成功', icon: 'success' })
          }
        })
      }
    })
  },

  // 提交表单
  onSubmit(event) {
    const formData = event.detail.value
    const app = getApp()

    // 添加 openid 和图片URL
    formData.openid = app.globalData.openid
    formData.imageUrl = this.data.imageUrl
    formData.createTime = new Date()

    // 保存到云数据库
    wx.cloud.callFunction({
      name: 'save-data',
      data: formData
    }).then(res => {
      wx.showToast({ title: '提交成功', icon: 'success' })
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    }).catch(err => {
      wx.showToast({ title: '提交失败', icon: 'none' })
      console.error(err)
    })
  }
})
```

#### 云函数（save-data）
```javascript
// cloudfunctions/save-data/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const db = cloud.database()
  const _ = db.command

  try {
    // 保存数据到集合
    const res = await db.collection('patients').add({
      data: {
        ...event,
        createTime: db.serverDate()
      }
    })

    return {
      success: true,
      _id: res._id
    }
  } catch (err) {
    console.error(err)
    return {
      success: false,
      error: err.message
    }
  }
}
```

### 3. 数据导出（CSV）

#### 云函数（export-csv）
```javascript
// cloudfunctions/export-csv/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const db = cloud.database()

  try {
    // 1. 查询所有数据（限制1000条）
    const res = await db.collection('patients')
      .limit(1000)
      .orderBy('createTime', 'desc')
      .get()

    // 2. 转换为CSV格式
    const data = res.data

    if (data.length === 0) {
      return { success: false, message: '暂无数据' }
    }

    // CSV表头
    const headers = Object.keys(data[0]).join(',')

    // CSV数据行
    const rows = data.map(item => {
      return Object.values(item).map(val => {
        // 处理包含逗号的字段
        if (typeof val === 'string' && val.includes(',')) {
          return `"${val}"`
        }
        return val
      }).join(',')
    })

    const csvContent = [headers, ...rows].join('\n')

    // 3. 上传到云存储
    const fileName = `export/patients-${Date.now()}.csv`
    const uploadRes = await cloud.uploadFile({
      cloudPath: fileName,
      fileContent: csvContent
    })

    // 4. 返回下载链接（有效期1小时）
    const fileRes = await cloud.getTempFileURL({
      fileList: [uploadRes.fileID]
    })

    return {
      success: true,
      downloadUrl: fileRes.fileList[0].tempFileURL,
      count: data.length
    }
  } catch (err) {
    console.error(err)
    return {
      success: false,
      error: err.message
    }
  }
}
```

#### 前端调用导出
```javascript
// 导出CSV
exportCSV() {
  wx.showLoading({ title: '导出中...' })

  wx.cloud.callFunction({
    name: 'export-csv'
  }).then(res => {
    wx.hideLoading()

    if (res.result.success) {
      // 下载文件
      wx.downloadFile({
        url: res.result.downloadUrl,
        success: res => {
          // 打开文件
          wx.openDocument({
            filePath: res.tempFilePath,
            fileType: 'csv',
            showMenu: true
          })
        }
      })

      wx.showToast({
        title: `导出${res.result.count}条数据`,
        icon: 'success'
      })
    } else {
      wx.showToast({ title: res.result.message, icon: 'none' })
    }
  }).catch(err => {
    wx.hideLoading()
    wx.showToast({ title: '导出失败', icon: 'none' })
  })
}
```

### 4. 数据库设计规范

#### 集合（表）命名
```
users        # 用户表
patients     # 患者数据表
records      # 诊疗记录表
followups    # 随访记录表
```

#### 字段命名规范
```
// 通用字段
_id          # 主键（自动生成）
_openid      # 用户openid（索引字段）
createTime   # 创建时间（db.serverDate()）
updateTime   # 更新时间

// 患者字段
name         # 姓名（必填）
age          # 年龄
gender       # 性别：male/female
phone        # 联系电话
diagnosis    # 诊断
treatment    # 治疗方案
```

#### 安全规则（database.rules.json）
```json
{
  "rules": {
    "users": {
      "read": "auth.openid == doc.openid",
      "write": "auth.openid == doc.openid"
    },
    "patients": {
      "read": "auth.openid != null", // 需要登录
      "write": "auth.openid != null"
    }
  }
}
```

## UI/UX 设计规范

### 1. 色彩系统
```css
/* 主题色 */
--primary-color: #07C160; /* 微信绿 */
--secondary-color: #10AEFF; /* 微信蓝 */

/* 中性色 */
--text-primary: #333333;
--text-secondary: #666666;
--border-color: #E5E5E5;
--bg-color: #F7F7F7;

/* 语义色 */
--success: #07C160;
--warning: #FFB800;
--error: #FA5151;
```

### 2. 间距规范
```css
/* 页面边距 */
.page-padding { padding: 32rpx; }

/* 元素间距 */
.spacing-sm { margin: 16rpx 0; }
.spacing-md { margin: 24rpx 0; }
.spacing-lg { margin: 32rpx 0; }
```

### 3. 字体规范
```css
/* 标题 */
.title-h1 { font-size: 48rpx; font-weight: bold; }
.title-h2 { font-size: 40rpx; font-weight: bold; }
.title-h3 { font-size: 32rpx; font-weight: 500; }

/* 正文 */
.text-body { font-size: 28rpx; line-height: 1.6; }
.text-caption { font-size: 24rpx; color: var(--text-secondary); }
```

### 4. 组件示例（卡片）
```xml
<!-- data-card.wxml -->
<view class="card">
  <view class="card-header">
    <text class="card-title">{{title}}</text>
    <text class="card-time">{{time}}</text>
  </view>
  <view class="card-body">
    <slot></slot>
  </view>
  <view class="card-footer" wx:if="{{showFooter}}">
    <button size="mini" bindtap="onEdit">编辑</button>
    <button size="mini" type="warn" bindtap="onDelete">删除</button>
  </view>
</view>
```

```css
/* data-card.wxss */
.card {
  background: #FFFFFF;
  border-radius: 16rpx;
  padding: 32rpx;
  margin: 24rpx 0;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24rpx;
}

.card-title {
  font-size: 32rpx;
  font-weight: bold;
}

.card-time {
  font-size: 24rpx;
  color: #999;
}
```

## 常见问题与解决方案

### Q1: 如何调试云函数？
**A**:
1. 右键云函数目录 → "上传并部署：云端安装依赖"
2. 在云函数控制台查看日志
3. 本地调试：微信开发者工具 → 云开发 → 云函数 → 本地调试

### Q2: 数据库查询速度慢？
**A**: 优化方法
1. **添加索引**：在常用查询字段上建立索引
2. **限制查询数量**：使用 `.limit(20)`
3. **使用分页**：`.skip(page * 20).limit(20)`
4. **避免查询大字段**：图片URL等大字段单独存储

```javascript
// 添加索引（在云开发控制台）
db.collection('patients').createIndex({
  openid: 1,
  createTime: -1
})
```

### Q3: 如何实现数据权限控制？
**A**: 三层防护
1. **前端限制**：根据用户角色显示不同功能
2. **云函数验证**：检查 openid 是否有权限
3. **数据库安全规则**：配置 database.rules.json

```javascript
// 云函数权限验证
const wxContext = cloud.getWXContext()
const openid = wxContext.OPENID

// 查询用户角色
const user = await db.collection('users').where({
  openid: openid
}).get()

if (user.data[0].role !== 'admin') {
  return { success: false, message: '无权限' }
}
```

### Q4: 如何优化小程序体积？
**A**:
1. **分包加载**：app.json 配置 subpackages
2. **图片压缩**：使用 tinypng 压缩
3. **按需引入**：组件按需引入，不引入未使用的库
4. **云存储**：大文件上传到云存储

```json
// app.json 分包配置
{
  "pages": ["pages/index/index"],
  "subpackages": [
    {
      "root": "package-data",
      "pages": ["pages/data-collection/data-collection"]
    },
    {
      "root": "package-admin",
      "pages": ["pages/admin/admin"]
    }
  ]
}
```

## 开发流程

### 1. 初始化项目
```bash
# 1. 微信开发者工具 → 创建项目
# 2. 填写 AppID（测试号或正式号）
# 3. 选择"云开发"模板
# 4. 创建云开发环境
```

### 2. 开发流程
```
1. 设计数据库结构（云开发控制台）
2. 开发前端页面（wxml + wxss + js）
3. 开发云函数（Node.js）
4. 调试（本地调试 → 云端调试）
5. 发布体验版（测试）
6. 提交审核（正式发布）
```

### 3. 版本管理
```
开发版本 → 体验版本 → 审核版本 → 线上版本
```

## 组件库推荐

### 官方组件库
- **WeUI**：https://weui.io/
- **TDesign**：https://tdesign.tencent.com/

### 第三方组件
- **Vant Weapp**：https://vant-contrib.gitee.io/vant-weapp/
- **ColorUI**：https://github.com/weilanwl/ColorUI

---

**最后更新**：2026-01-10
**适用项目**：VPT初诊数据收集系统、医学科研数据采集
**开发者**：FattyTiger
