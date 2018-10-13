import mysql.connector

conn = mysql.connector.connect(user='root', password='123456', database='test')

cursor = conn.cursor()
id = 2
name = 'b'
# cursor.execute('insert into test values (%s, %s)', [id, name])
# conn.commit()
cursor.execute('select * from test')
result = cursor.fetchall()
cursor.close()
conn.close()
print(result)
