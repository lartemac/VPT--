// pages/preoperative/preoperative.js
const dbUtil = require('../../utils/db.js');

Page({
  data: {
    patientId: '',
    form: {
      hb: '',
      wbc: '',
      plt: '',
      coagulation: '',
      liverKidney: '',
      ecg: '',
      imaging: '',
      other: '',
      checkDate: ''
    }
  },

  onLoad(options) {
    const { patientId } = options;

    if (patientId) {
      this.setData({ patientId });
      this.loadExistingData(patientId);
    }
  },

  // 加载已有数据
  async loadExistingData(patientId) {
    try {
      const res = await dbUtil.getList(dbUtil.COLLECTIONS.PREOPERATIVE, { patientId });

      if (res.data && res.data.length > 0) {
        this.setData({
          form: res.data[0]
        });
      }
    } catch (error) {
      console.error('加载数据失败：', error);
    }
  },

  // 输入变化
  onInputChange(e) {
    const { field } = e.currentTarget.dataset;
    const value = e.detail.value;

    this.setData({
      [`form.${field}`]: value
    });
  },

  // 日期变化
  onDateChange(e) {
    const { field } = e.currentTarget.dataset;
    const value = e.detail.value;

    this.setData({
      [`form.${field}`]: value
    });
  },

  // 保存数据
  async saveData() {
    const form = this.data.form;

    if (!this.data.patientId) {
      wx.showToast({
        title: '患者ID不能为空',
        icon: 'none'
      });
      return;
    }

    wx.showLoading({ title: '保存中...' });

    try {
      // 先查询是否已有数据
      const res = await dbUtil.getList(dbUtil.COLLECTIONS.PREOPERATIVE, { patientId: this.data.patientId });

      if (res.data && res.data.length > 0) {
        // 更新
        await dbUtil.update(dbUtil.COLLECTIONS.PREOPERATIVE, res.data[0]._id, {
          ...form,
          patientId: this.data.patientId
        });
      } else {
        // 新增
        await dbUtil.add(dbUtil.COLLECTIONS.PREOPERATIVE, {
          ...form,
          patientId: this.data.patientId
        });
      }

      wx.showToast({
        title: '保存成功',
        icon: 'success'
      });
    } catch (error) {
      console.error('保存失败：', error);
      wx.showToast({
        title: '保存失败',
        icon: 'none'
      });
    } finally {
      wx.hideLoading();
    }
  },

  // 返回
  goBack() {
    wx.navigateBack();
  }
});
