// 云数据库操作工具
const db = wx.cloud.database();

/**
 * 数据库集合名称
 */
const COLLECTIONS = {
  PATIENTS: 'patients',           // 患者基本信息
  PREOPERATIVE: 'preoperative',   // 术前检查数据
  INTRAOPERATIVE: 'intraoperative', // 术中数据
  POSTOPERATIVE: 'postoperative'  // 术后回访数据
};

/**
 * 添加单条数据
 */
function add(collection, data) {
  return db.collection(collection).add({
    data: {
      ...data,
      createTime: db.serverDate(),
      updateTime: db.serverDate()
    }
  });
}

/**
 * 更新数据
 */
function update(collection, id, data) {
  return db.collection(collection).doc(id).update({
    data: {
      ...data,
      updateTime: db.serverDate()
    }
  });
}

/**
 * 删除数据
 */
function remove(collection, id) {
  return db.collection(collection).doc(id).remove();
}

/**
 * 根据 ID 获取数据
 */
function getById(collection, id) {
  return db.collection(collection).doc(id).get();
}

/**
 * 获取列表数据
 */
function getList(collection, where = {}, limit = 20, skip = 0) {
  return db.collection(collection)
    .where(where)
    .orderBy('createTime', 'desc')
    .limit(limit)
    .skip(skip)
    .get();
}

/**
 * 获取所有数据（用于导出）
 */
function getAll(collection) {
  // 注意：云数据库最多一次获取 100 条，需要分页获取
  return new Promise((resolve, reject) => {
    const allData = [];
    const count = 100; // 每次获取数量

    function getData(skip = 0) {
      db.collection(collection)
        .orderBy('createTime', 'desc')
        .limit(count)
        .skip(skip)
        .get()
        .then(res => {
          allData.push(...res.data);

          if (res.data.length === count) {
            // 继续获取下一页
            getData(skip + count);
          } else {
            // 全部获取完成
            resolve(allData);
          }
        })
        .catch(reject);
    }

    getData(0);
  });
}

module.exports = {
  db,
  COLLECTIONS,
  add,
  update,
  remove,
  getById,
  getList,
  getAll
};
