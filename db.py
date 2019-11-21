# -*- coding: utf-8 -*- 
import pymysql

def selectByParameters(sql,params = None):
        #建立连接
    db = pymysql.connect(host='172.16.230.131',port=3306,user ='devops',passwd='147258369',db='devops')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,params)
    result = cursor.fetchall()
    return result
    cursor.close()
    db.close()

def updateByParameters(sql,params = None):
    db = pymysql.connect(host='172.16.230.131',port=3306,user ='devops',passwd='147258369',db='devops')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    count = cursor.execute(sql,params)
    db.commit()
    return count
    db.rollback()
    cursor.close()
    db.close()

#测试查询封装，带查询查询封装
if __name__ == "__main__":
    #sql = "select * from server where name=%s" 
    #sql = "insert into server (name, ip, port, user) values( 'long', '1.1.1.1', 22, 'root' )"
    sql = "delete from server where name = %s"
    #params =("test")
    params =("long")
    #result = selectByParameters(sql,params=params)
    result = updateByParameters(sql,params=params)
    print( result )

