import pymysql as mysql

conn = mysql.connect(
    user='', 
    passwd='', 
    host='', 
    db='', 
    charset='utf8'
)

cursor = conn.cursor(mysql.cursors.DictCursor)
print("DB연결 완료")
conn.close()
