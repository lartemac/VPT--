// pages/index/index.js
const dbUtil = require('../../utils/db.js');

Page({
  data: {
    stats: {
      totalPatients: 0,
      todayPatients: 0,
      completed: 0
    }
  },

  onLoad() {
    this.loadStats();
  },

  onShow() {
    this.loadStats();
  },

  // 加载统计数据
  async loadStats() {
    try {
      // 获取患者总数
      const res = await dbUtil.getList(dbUtil.COLLECTIONS.PATIENTS);

      // 计算今日新增
      const today = new Date();
      today.setHours(0, 0, 0, 0);

      const todayCount = res.data.filter(item => {
        const createTime = new Date(item.createTime);
        return createTime >= today;
      }).length;

      this.setData({
        'stats.totalPatients': res.data.length,
        'stats.todayPatients': todayCount,
        'stats.completed': res.data.length // 可根据实际情况修改
      });
    } catch (error) {
      console.error('加载统计数据失败：', error);
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  // 跳转到新增患者页面
  goToPatient() {
    wx.navigateTo({
      url: '/pages/patient/patient?mode=add'
    });
  },

  // 跳转到患者列表页面
  goToList() {
    wx.navigateTo({
      url: '/pages/patient/patient?mode=list'
    });
  },

  // 跳转到数据导出页面
  goToExport() {
    wx.switchTab({
      url: '/pages/export/export'
    });
  }
});
