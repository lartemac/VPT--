// pages/export/export.js
const dbUtil = require('../../utils/db.js');

Page({
  data: {
    exporting: {
      patients: false,
      preoperative: false,
      intraoperative: false,
      postoperative: false,
      all: false
    },
    exportHistory: []
  },

  onLoad() {
    this.loadExportHistory();
  },

  // 导出单个数据集
  async exportData(e) {
    const { type } = e.currentTarget.dataset;
    const collectionMap = {
      patients: { collection: dbUtil.COLLECTIONS.PATIENTS, name: '患者基本信息' },
      preoperative: { collection: dbUtil.COLLECTIONS.PREOPERATIVE, name: '术前检查数据' },
      intraoperative: { collection: dbUtil.COLLECTIONS.INTRAOPERATIVE, name: '术中数据' },
      postoperative: { collection: dbUtil.COLLECTIONS.POSTOPERATIVE, name: '术后回访数据' }
    };

    const config = collectionMap[type];
    if (!config) return;

    this.setData({
      [`exporting.${type}`]: true
    });

    try {
      wx.showLoading({ title: '获取数据中...' });

      // 调用云函数获取所有数据
      const res = await wx.cloud.callFunction({
        name: 'getAllData',
        data: {
          collectionName: config.collection
        }
      });

      wx.hideLoading();

      if (!res.result.success) {
        throw new Error(res.result.message || '获取数据失败');
      }

      const data = res.result.data;

      if (data.length === 0) {
        wx.showToast({
          title: '暂无数据',
          icon: 'none'
        });
        return;
      }

      // 转换为 CSV 格式
      const csv = this.convertToCSV(data);

      // 生成文件名
      const fileName = `${config.name}_${this.getTimestamp()}.csv`;

      // 复制到剪贴板
      await wx.setClipboardData({
        data: csv
      });

      wx.showModal({
        title: '导出成功',
        content: `CSV 数据已复制到剪贴板，共 ${data.length} 条记录。请粘贴到文本编辑器中保存为 .csv 文件。`,
        showCancel: false,
        success: () => {
          // 记录导出历史
          this.addExportHistory(config.name, data.length);
        }
      });

    } catch (error) {
      console.error('导出失败：', error);
      wx.showToast({
        title: error.message || '导出失败',
        icon: 'none'
      });
    } finally {
      this.setData({
        [`exporting.${type}`]: false
      });
    }
  },

  // 导出全部数据
  async exportAllData() {
    this.setData({
      'exporting.all': true
    });

    try {
      wx.showLoading({ title: '获取数据中...' });

      // 并行获取所有数据
      const promises = [
        wx.cloud.callFunction({
          name: 'getAllData',
          data: { collectionName: dbUtil.COLLECTIONS.PATIENTS }
        }),
        wx.cloud.callFunction({
          name: 'getAllData',
          data: { collectionName: dbUtil.COLLECTIONS.PREOPERATIVE }
        }),
        wx.cloud.callFunction({
          name: 'getAllData',
          data: { collectionName: dbUtil.COLLECTIONS.INTRAOPERATIVE }
        }),
        wx.cloud.callFunction({
          name: 'getAllData',
          data: { collectionName: dbUtil.COLLECTIONS.POSTOPERATIVE }
        })
      ];

      const results = await Promise.all(promises);

      wx.hideLoading();

      const allData = {
        patients: results[0].result.data,
        preoperative: results[1].result.data,
        intraoperative: results[2].result.data,
        postoperative: results[3].result.data
      };

      const totalCount = allData.patients.length + allData.preoperative.length +
                        allData.intraoperative.length + allData.postoperative.length;

      if (totalCount === 0) {
        wx.showToast({
          title: '暂无数据',
          icon: 'none'
        });
        return;
      }

      // 生成合并的 CSV
      const csv = this.convertAllToCSV(allData);

      // 复制到剪贴板
      await wx.setClipboardData({
        data: csv
      });

      wx.showModal({
        title: '导出成功',
        content: `所有数据已复制到剪贴板，共 ${totalCount} 条记录。请粘贴到文本编辑器中保存为 .csv 文件。`,
        showCancel: false,
        success: () => {
          this.addExportHistory('全部数据', totalCount);
        }
      });

    } catch (error) {
      console.error('导出失败：', error);
      wx.hideLoading();
      wx.showToast({
        title: error.message || '导出失败',
        icon: 'none'
      });
    } finally {
      this.setData({
        'exporting.all': false
      });
    }
  },

  // 将数据转换为 CSV 格式
  convertToCSV(data) {
    if (!data || data.length === 0) return '';

    // 获取所有字段（从第一条数据）
    const firstItem = data[0];
    const fields = Object.keys(firstItem).filter(key => key !== '_id');

    // 构建 CSV 表头
    let csv = fields.join(',') + '\n';

    // 构建数据行
    data.forEach(item => {
      const row = fields.map(field => {
        let value = item[field];

        // 处理日期对象
        if (value && typeof value === 'object') {
          if (value.$date) {
            value = new Date(value.$date).toLocaleString('zh-CN');
          } else {
            value = JSON.stringify(value);
          }
        }

        // 处理 undefined 和 null
        if (value === undefined || value === null) {
          value = '';
        }

        // 转换为字符串并处理逗号
        value = String(value);
        if (value.includes(',') || value.includes('\n') || value.includes('"')) {
          value = `"${value.replace(/"/g, '""')}"`;
        }

        return value;
      });

      csv += row.join(',') + '\n';
    });

    return csv;
  },

  // 将全部数据转换为 CSV（分多个工作表）
  convertAllToCSV(allData) {
    let csv = '';

    // 患者基本信息
    csv += '=== 患者基本信息 ===\n';
    csv += this.convertToCSV(allData.patients);
    csv += '\n\n';

    // 术前数据
    csv += '=== 术前检查数据 ===\n';
    csv += this.convertToCSV(allData.preoperative);
    csv += '\n\n';

    // 术中数据
    csv += '=== 术中数据 ===\n';
    csv += this.convertToCSV(allData.intraoperative);
    csv += '\n\n';

    // 术后数据
    csv += '=== 术后回访数据 ===\n';
    csv += this.convertToCSV(allData.postoperative);

    return csv;
  },

  // 获取时间戳
  getTimestamp() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()).padStart(2, '0');
    const minute = String(now.getMinutes()).padStart(2, '0');

    return `${year}${month}${day}_${hour}${minute}`;
  },

  // 添加导出历史
  addExportHistory(type, count) {
    const history = this.data.exportHistory;
    history.unshift({
      id: Date.now(),
      time: new Date().toLocaleString('zh-CN'),
      type: type,
      count: count
    });

    // 只保留最近 10 条
    if (history.length > 10) {
      history.pop();
    }

    this.setData({
      exportHistory: history
    });

    // 保存到本地存储
    wx.setStorageSync('exportHistory', history);
  },

  // 加载导出历史
  loadExportHistory() {
    const history = wx.getStorageSync('exportHistory') || [];
    this.setData({
      exportHistory: history
    });
  }
});
