// pages/patient/patient.js
const dbUtil = require('../../utils/db.js');
const app = getApp();

Page({
  data: {
    mode: 'list', // list, add, edit
    patientId: null,
    form: {
      name: '',
      gender: '男',
      age: '',
      phone: '',
      medicalRecordNo: '',
      firstVisitDate: '',
      chiefComplaint: '',
      presentIllness: '',
      pastHistory: '',
      remarks: ''
    },
    patientList: [],
    searchKeyword: ''
  },

  onLoad(options) {
    const { mode, id } = options;

    if (mode) {
      this.setData({ mode });

      if (mode === 'edit' && id) {
        this.setData({ patientId: id });
        this.loadPatientDetail(id);
      } else if (mode === 'add') {
        this.setTodayDate();
      }
    }

    if (mode === 'list') {
      this.loadPatientList();
    }
  },

  onShow() {
    if (this.data.mode === 'list') {
      this.loadPatientList();
    }
  },

  // 设置今天的日期
  setTodayDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');

    this.setData({
      'form.firstVisitDate': `${year}-${month}-${day}`
    });
  },

  // 加载患者列表
  async loadPatientList() {
    wx.showLoading({ title: '加载中...' });

    try {
      const res = await dbUtil.getList(dbUtil.COLLECTIONS.PATIENTS, {}, 100);

      this.setData({
        patientList: res.data
      });
    } catch (error) {
      console.error('加载患者列表失败：', error);
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    } finally {
      wx.hideLoading();
    }
  },

  // 加载患者详情
  async loadPatientDetail(id) {
    wx.showLoading({ title: '加载中...' });

    try {
      const res = await dbUtil.getById(dbUtil.COLLECTIONS.PATIENTS, id);

      this.setData({
        form: res.data
      });
    } catch (error) {
      console.error('加载患者详情失败：', error);
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    } finally {
      wx.hideLoading();
    }
  },

  // 输入框变化
  onInputChange(e) {
    const { field } = e.currentTarget.dataset;
    const value = e.detail.value;

    this.setData({
      [`form.${field}`]: value
    });
  },

  // 日期选择
  onDateChange(e) {
    const { field } = e.currentTarget.dataset;
    const value = e.detail.value;

    this.setData({
      [`form.${field}`]: value
    });
  },

  // 搜索输入
  onSearchInput(e) {
    this.setData({
      searchKeyword: e.detail.value
    });
  },

  // 保存患者信息
  async savePatient() {
    const form = this.data.form;

    // 验证必填项
    if (!form.name) {
      wx.showToast({
        title: '请输入患者姓名',
        icon: 'none'
      });
      return;
    }

    if (!form.age) {
      wx.showToast({
        title: '请输入年龄',
        icon: 'none'
      });
      return;
    }

    wx.showLoading({ title: '保存中...' });

    try {
      if (this.data.mode === 'add') {
        // 新增
        await dbUtil.add(dbUtil.COLLECTIONS.PATIENTS, form);
        wx.showToast({
          title: '保存成功',
          icon: 'success'
        });
      } else if (this.data.mode === 'edit') {
        // 更新
        await dbUtil.update(dbUtil.COLLECTIONS.PATIENTS, this.data.patientId, form);
        wx.showToast({
          title: '更新成功',
          icon: 'success'
        });
      }

      // 保存成功后返回
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
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

  // 查看患者详情
  viewPatient(e) {
    const { id } = e.currentTarget.dataset;

    wx.showActionSheet({
      itemList: ['查看详情', '编辑信息', '术前数据', '术中数据', '术后回访'],
      success: (res) => {
        switch (res.tapIndex) {
          case 0: // 查看详情
            wx.navigateTo({
              url: `/pages/patient/patient?mode=view&id=${id}`
            });
            break;
          case 1: // 编辑信息
            wx.navigateTo({
              url: `/pages/patient/patient?mode=edit&id=${id}`
            });
            break;
          case 2: // 术前数据
            wx.navigateTo({
              url: `/pages/preoperative/preoperative?patientId=${id}`
            });
            break;
          case 3: // 术中数据
            wx.navigateTo({
              url: `/pages/intraoperative/intraoperative?patientId=${id}`
            });
            break;
          case 4: // 术后回访
            wx.navigateTo({
              url: `/pages/postoperative/postoperative?patientId=${id}`
            });
            break;
        }
      }
    });
  },

  // 返回
  goBack() {
    wx.navigateBack();
  }
});
