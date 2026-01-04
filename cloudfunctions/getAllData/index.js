// 云函数入口文件
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();
const _ = db.command;

/**
 * 获取指定集合的所有数据
 */
exports.main = async (event, context) => {
  const { collectionName } = event;

  if (!collectionName) {
    return {
      success: false,
      message: '请指定集合名称'
    };
  }

  try {
    // 获取总数
    const countResult = await db.collection(collectionName).count();
    const total = countResult.total;
    const allData = [];

    // 每次获取 100 条数据
    const limit = 100;
    let skip = 0;

    while (skip < total) {
      const res = await db.collection(collectionName)
        .skip(skip)
        .limit(limit)
        .get();

      allData.push(...res.data);
      skip += limit;
    }

    return {
      success: true,
      data: allData,
      total: total
    };
  } catch (error) {
    console.error('获取数据失败：', error);
    return {
      success: false,
      message: error.message || '获取数据失败'
    };
  }
};
