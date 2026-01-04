// pages/intraoperative/intraoperative.js
const dbUtil = require('../../utils/db.js');

Page({
  data: {
    patientId: '',
    form: {
      surgeryDate: '',
      surgeryMethod: '',
      anesthesia: '',
      duration: '',
      bloodLoss: '',
      complications: '',
      specialNotes: '',
      images: []
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
      const res = await dbUtil.getList(dbUtil.COLLECTIONS.INTRAOPERATIVE, { patientId });

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

  // 上传图片
  uploadImage() {
    wx.chooseImage({
      count: 9,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePaths = res.tempFilePaths;

        wx.showLoading({ title: '上传中...' });

        // 上传所有图片
        const uploadPromises = tempFilePaths.map(filePath => {
          return wx.cloud.uploadFile({
            cloudPath: `intraoperative/${Date.now()}_${Math.random().toString(36).substr(2)}.jpg`,
            filePath: filePath
          });
        });

        Promise.all(uploadPromises).then(uploadRes => {
          const fileIDs = uploadRes.map(item => item.fileID);

          // 添加到现有图片列表
          const images = this.data.form.images || [];
          images.push(...fileIDs);

          this.setData({
            'form.images': images
          });

          wx.hideLoading();
          wx.showToast({
            title: '上传成功',
            icon: 'success'
          });
        }).catch(error => {
          console.error('上传失败：', error);
          wx.hideLoading();
          wx.showToast({
            title: '上传失败',
            icon: 'none'
          });
        });
      }
    });
  },

  // 预览图片
  previewImage(e) {
    const { url } = e.currentTarget.dataset;

    wx.previewImage({
      current: url,
      urls: this.data.form.images
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
      const res = await dbUtil.getList(dbUtil.COLLECTIONS.INTRAOPERATIVE, { patientId: this.data.patientId });

      if (res.data && res.data.length > 0) {
        // 更新
        await dbUtil.update(dbUtil.COLLECTIONS.INTRAOPERATIVE, res.data[0]._id, {
          ...form,
          patientId: this.data.patientId
        });
      } else {
        // 新增
        await dbUtil.add(dbUtil.COLLECTIONS.INTRAOPERATIVE, {
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
