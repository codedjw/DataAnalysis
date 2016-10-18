/***************************************
	MERGE VISIT TABLE AND PAGEVISIT TABLE (FIND 10774 RECORDS) 
***************************************/
/*
SELECT *
FROM
  (SELECT *
   FROM qyw_7th_visit
   ORDER BY USER_ID,
            VISIT_TIME) AS t1
INNER JOIN
  (SELECT *
   FROM qyw_7th_pagevisit
   ORDER BY USER_ID,
            OPERATE_TIME) AS t2 ON t1.USER_ID = t2.USER_ID
AND t1.VISIT_TIME = t2.OPERATE_TIME;
*/

/***************************************
	MERGE VISIT TABLE AND OP DICT TABLE
***************************************/

-- UPDATE VISIT_OP (REMOVE PREFIX)
/*
UPDATE qyw_7th_visit SET VISIT_OP = REPLACE(VISIT_OP, 'http://app.quyiyuan.com:8888', '');
UPDATE qyw_7th_visit SET VISIT_OP = REPLACE(VISIT_OP, 'http://100.98.41.195:8888', '');
UPDATE qyw_7th_visit SET VISIT_OP = REPLACE(VISIT_OP, 'http://app.quyiyuan.com:8888', '');
UPDATE qyw_7th_visit SET VISIT_OP = REPLACE(VISIT_OP, 'http://luoyang.quyiyuan.com:8888', '');
*/

/*
INSERT INTO qyw_7th_visit_mean 
SELECT t1.USER_ID,
       t1.HOSPITAL_ID,
       t1.IP,
       t1.VISIT_TIME,
       t1.VERSION,
       t2.*
FROM
  (SELECT *
   FROM qyw_7th_visit
   ORDER BY VISIT_OP) AS t1
INNER JOIN
  (SELECT VISIT_OP,
          CATEGORY,
          MEAN AS VISIT_MEAN,
          TRIGGER_TYPE
   FROM sys_business_dict_20151207_07
   WHERE DICT_ID != 112
   ORDER BY VISIT_OP) AS t2 ON t1.VISIT_OP = t2.VISIT_OP
ORDER BY t1.USER_ID,
         t1.VISIT_TIME;
*/

/***************************************
	筛选出老用户和新用户的数据
***************************************/
/*
-- 新用户 (61637)
INSERT INTO qyw_7th_event_new_user
SELECT CASE_ID,
       t1.USER_ID,
       VISIT_TIME,
       VISIT_MEAN,
       CATEGORY,
	   TRIGGER_TYPE
FROM
  (SELECT *
   FROM qyw_7th_event
   ORDER BY USER_ID) AS t1
INNER JOIN
  (SELECT *
   FROM qyw_7th_user
   ORDER BY USER_ID) AS t2 ON t1.USER_ID = t2.USER_ID
WHERE DATE(VISIT_TIME) = DATE(REGISTER_DATE);

-- 老用户 (230228)
INSERT INTO qyw_7th_event_old_user
SELECT CASE_ID,
       t1.USER_ID,
       VISIT_TIME,
       VISIT_MEAN,
       CATEGORY,
	   TRIGGER_TYPE
FROM
  (SELECT *
   FROM qyw_7th_event
   ORDER BY USER_ID) AS t1
INNER JOIN
  (SELECT *
   FROM qyw_7th_user
   ORDER BY USER_ID) AS t2 ON t1.USER_ID = t2.USER_ID
WHERE DATE(VISIT_TIME) != DATE(REGISTER_DATE);
*/

/***************************************
	筛选出新用户成功预约挂号的CASE
***************************************/
-- 新用户预约成功
/*
SELECT DISTINCT t3.CASE_ID,
                t3.VISIT_TIME,
                t3.USER_ID,
                t3.VISIT_MEAN
FROM
  (SELECT *
   FROM qyw_7th_event_new_user
   WHERE CASE_ID IN
       (SELECT DISTINCT t5.CASE_ID
        FROM
          (SELECT DISTINCT t1.CASE_ID
           FROM
             (SELECT DISTINCT CASE_ID
              FROM qyw_7th_event_new_user
              WHERE VISIT_MEAN IN ('C端主页的预约挂号入口',
                                   '获取医生列表')) AS t1
           INNER JOIN
             (SELECT DISTINCT CASE_ID
              FROM qyw_7th_event_new_user
              WHERE VISIT_MEAN IN ('获取预约挂号结果页面',
                                   '获取预约挂号详情')) AS t2 ON t1.CASE_ID = t2.CASE_ID) AS t5
        INNER JOIN
          (SELECT DISTINCT CASE_ID
           FROM qyw_7th_event_new_user
           WHERE VISIT_MEAN LIKE '%成功%') AS t6 ON t5.CASE_ID = t6.CASE_ID)
   ORDER BY VISIT_MEAN) AS t3
WHERE t3.TRIGGER_TYPE = '用户点击'
ORDER BY t3.USER_ID,
         t3.VISIT_TIME;
*/
-- 老用户预约成功
/*
SELECT DISTINCT t3.CASE_ID,
                t3.VISIT_TIME,
                t3.USER_ID,
                t3.VISIT_MEAN
FROM
  (SELECT *
   FROM qyw_7th_event_old_user
   WHERE CASE_ID IN
       (SELECT DISTINCT t5.CASE_ID
        FROM
          (SELECT DISTINCT t1.CASE_ID
           FROM
             (SELECT DISTINCT CASE_ID
              FROM qyw_7th_event_old_user
              WHERE VISIT_MEAN IN ('C端主页的预约挂号入口',
                                   '获取医生列表')) AS t1
           INNER JOIN
             (SELECT DISTINCT CASE_ID
              FROM qyw_7th_event_old_user
              WHERE VISIT_MEAN IN ('获取预约挂号结果页面',
                                   '获取预约挂号详情')) AS t2 ON t1.CASE_ID = t2.CASE_ID) AS t5
        INNER JOIN
          (SELECT DISTINCT CASE_ID
           FROM qyw_7th_event_old_user
           WHERE VISIT_MEAN LIKE '%成功%') AS t6 ON t5.CASE_ID = t6.CASE_ID)
   ORDER BY VISIT_MEAN) AS t3
WHERE t3.TRIGGER_TYPE = '用户点击'
ORDER BY t3.USER_ID,
         t3.VISIT_TIME;
*/
-- 新用户所有预约
/*
SELECT DISTINCT t3.CASE_ID,
                t3.VISIT_TIME,
                t3.USER_ID,
                t3.VISIT_MEAN
FROM
  (SELECT *
   FROM qyw_7th_event_new_user
   WHERE CASE_ID IN
       (SELECT DISTINCT CASE_ID
        FROM qyw_7th_event_new_user
        WHERE VISIT_MEAN IN ('C端主页的预约挂号入口',
                             '获取医生列表'))
   ORDER BY VISIT_MEAN) AS t3
WHERE t3.TRIGGER_TYPE = '用户点击'
ORDER BY t3.USER_ID,
         t3.VISIT_TIME;
*/
-- 老用户所有预约
/*
SELECT DISTINCT t3.CASE_ID,
                t3.VISIT_TIME,
                t3.USER_ID,
                t3.VISIT_MEAN
FROM
  (SELECT *
   FROM qyw_7th_event_old_user
   WHERE CASE_ID IN
       (SELECT DISTINCT CASE_ID
        FROM qyw_7th_event_old_user
        WHERE VISIT_MEAN IN ('C端主页的预约挂号入口',
                             '获取医生列表'))
   ORDER BY VISIT_MEAN) AS t3
WHERE t3.TRIGGER_TYPE = '用户点击'
ORDER BY t3.USER_ID,
         t3.VISIT_TIME;
*/
-- 新用户预约失败
/*
SELECT DISTINCT t3.CASE_ID,
                t3.VISIT_TIME,
                t3.USER_ID,
                t3.VISIT_MEAN
FROM
  (SELECT *
   FROM qyw_7th_event_new_user
   WHERE CASE_ID IN
       (SELECT DISTINCT t7.CASE_ID
        FROM
          (SELECT DISTINCT CASE_ID
           FROM qyw_7th_event_new_user
           WHERE VISIT_MEAN IN ('C端主页的预约挂号入口',
                                '获取医生列表')) AS t7
        LEFT JOIN
          (SELECT DISTINCT t5.CASE_ID
           FROM
             (SELECT DISTINCT t1.CASE_ID
              FROM
                (SELECT DISTINCT CASE_ID
                 FROM qyw_7th_event_new_user
                 WHERE VISIT_MEAN IN ('C端主页的预约挂号入口',
                                      '获取医生列表')) AS t1
              INNER JOIN
                (SELECT DISTINCT CASE_ID
                 FROM qyw_7th_event_new_user
                 WHERE VISIT_MEAN IN ('获取预约挂号结果页面',
                                      '获取预约挂号详情')) AS t2 ON t1.CASE_ID = t2.CASE_ID) AS t5
           INNER JOIN
             (SELECT DISTINCT CASE_ID
              FROM qyw_7th_event_new_user
              WHERE VISIT_MEAN LIKE '%成功%') AS t6 ON t5.CASE_ID = t6.CASE_ID) AS t8 ON t7.CASE_ID = t8.CASE_ID
        WHERE t8.CASE_ID IS NULL)
   ORDER BY VISIT_MEAN) AS t3
WHERE t3.TRIGGER_TYPE = '用户点击'
ORDER BY t3.USER_ID,
         t3.VISIT_TIME;
*/
-- 老用户预约失败
/*
SELECT DISTINCT t3.CASE_ID,
                t3.VISIT_TIME,
                t3.USER_ID,
                t3.VISIT_MEAN
FROM
  (SELECT *
   FROM qyw_7th_event_old_user
   WHERE CASE_ID IN
       (SELECT DISTINCT t7.CASE_ID
        FROM
          (SELECT DISTINCT CASE_ID
           FROM qyw_7th_event_old_user
           WHERE VISIT_MEAN IN ('C端主页的预约挂号入口',
                                '获取医生列表')) AS t7
        LEFT JOIN
          (SELECT DISTINCT t5.CASE_ID
           FROM
             (SELECT DISTINCT t1.CASE_ID
              FROM
                (SELECT DISTINCT CASE_ID
                 FROM qyw_7th_event_old_user
                 WHERE VISIT_MEAN IN ('C端主页的预约挂号入口',
                                      '获取医生列表')) AS t1
              INNER JOIN
                (SELECT DISTINCT CASE_ID
                 FROM qyw_7th_event_old_user
                 WHERE VISIT_MEAN IN ('获取预约挂号结果页面',
                                      '获取预约挂号详情')) AS t2 ON t1.CASE_ID = t2.CASE_ID) AS t5
           INNER JOIN
             (SELECT DISTINCT CASE_ID
              FROM qyw_7th_event_old_user
              WHERE VISIT_MEAN LIKE '%成功%') AS t6 ON t5.CASE_ID = t6.CASE_ID) AS t8 ON t7.CASE_ID = t8.CASE_ID
        WHERE t8.CASE_ID IS NULL)
   ORDER BY VISIT_MEAN) AS t3
WHERE t3.TRIGGER_TYPE = '用户点击'
ORDER BY t3.USER_ID,
         t3.VISIT_TIME;
*/

/***************************************
	评估预约操作
***************************************/
-- SELECT t2.*, CASE_CNT FROM (SELECT USER_ID, COUNT(*) AS CASE_CNT FROM qyw_7th_yy_succ_new GROUP BY USER_ID ORDER BY USER_ID) AS t1 INNER JOIN (SELECT * FROM qyw_7th_user ORDER BY USER_ID) AS t2 ON t1.USER_ID = t2.USER_ID ORDER BY CASE_CNT DESC;
-- SELECT t2.*, CASE_CNT FROM (SELECT USER_ID, COUNT(*) AS CASE_CNT FROM qyw_7th_yy_succ_old GROUP BY USER_ID ORDER BY USER_ID) AS t1 INNER JOIN (SELECT * FROM qyw_7th_user ORDER BY USER_ID) AS t2 ON t1.USER_ID = t2.USER_ID ORDER BY CASE_CNT DESC;

-- SELECT * FROM qyw_7th_event_new_user WHERE USER_ID = 11069676 AND TRIGGER_TYPE = '用户点击';

-- SELECT t2.*, CASE_CNT FROM (SELECT USER_ID, COUNT(*) AS CASE_CNT FROM qyw_7th_yy_all_new GROUP BY USER_ID ORDER BY USER_ID) AS t1 INNER JOIN (SELECT * FROM qyw_7th_user ORDER BY USER_ID) AS t2 ON t1.USER_ID = t2.USER_ID ORDER BY CASE_CNT DESC;
-- SELECT t2.*, CASE_CNT FROM (SELECT USER_ID, COUNT(*) AS CASE_CNT FROM qyw_7th_yy_all_old GROUP BY USER_ID ORDER BY USER_ID) AS t1 INNER JOIN (SELECT * FROM qyw_7th_user ORDER BY USER_ID) AS t2 ON t1.USER_ID = t2.USER_ID ORDER BY CASE_CNT DESC;

-- SELECT t4.*, t3.ALL_CASE_CNT, T3.SUCC_CNT FROM (SELECT t1.USER_ID, t1.CASE_CNT AS ALL_CASE_CNT, IF(t2.CASE_CNT IS NULL, 0, t2.CASE_CNT) AS SUCC_CNT FROM (SELECT USER_ID, COUNT(*) AS CASE_CNT FROM qyw_7th_yy_all_new GROUP BY USER_ID ORDER BY USER_ID) AS t1 LEFT JOIN (SELECT USER_ID, COUNT(*) AS CASE_CNT FROM qyw_7th_yy_succ_new GROUP BY USER_ID ORDER BY USER_ID) AS t2 ON t1.USER_ID = t2.USER_ID ORDER BY USER_ID) AS t3 INNER JOIN (SELECT * FROM qyw_7th_user ORDER BY USER_ID) AS t4 ON t3.USER_ID = t4.USER_ID;
-- SELECT t4.*, t3.ALL_CASE_CNT, T3.SUCC_CNT FROM (SELECT t1.USER_ID, t1.CASE_CNT AS ALL_CASE_CNT, IF(t2.CASE_CNT IS NULL, 0, t2.CASE_CNT) AS SUCC_CNT FROM (SELECT USER_ID, COUNT(*) AS CASE_CNT FROM qyw_7th_yy_all_old GROUP BY USER_ID ORDER BY USER_ID) AS t1 LEFT JOIN (SELECT USER_ID, COUNT(*) AS CASE_CNT FROM qyw_7th_yy_succ_old GROUP BY USER_ID ORDER BY USER_ID) AS t2 ON t1.USER_ID = t2.USER_ID ORDER BY USER_ID) AS t3 INNER JOIN (SELECT * FROM qyw_7th_user ORDER BY USER_ID) AS t4 ON t3.USER_ID = t4.USER_ID ORDER BY ALL_CASE_CNT DESC;

-- SELECT * FROM qyw_7th_event WHERE CASE_ID = '11137203@2016-05-16_0' ORDER BY VISIT_TIME;

SELECT * FROM qyw_7th_yy_all_old WHERE USER_ID = 10897793 ORDER BY START_TIME;
