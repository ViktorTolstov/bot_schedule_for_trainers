import sqlite3
import datetime
import time

database = 'database.sqlite'

def init_db():
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("""
    CREATE table fields (
        id integer primary key,
        name text,
        time text,
        date text,
        training text
    );
    """)
    connect.close()

# init_db()

def add_field(name,time,date,training):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM fields")
    try:
        field_id = str(cursor.fetchall()[-1][0] + 1)
    except:
        field_id = 1
    cursor.execute("insert into fields values ("+str(field_id)+",'"+name+"','"+time+"','"+date+"','"+training+"')")
    connect.commit()
    connect.close()

def get_field(day):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM fields where date='"+day+"'")
    res = cursor.fetchall()
    connect.close()
    result = []
    for i in res:
        result.append(list(i))
    return res

# add_field("Иванов И.И.","утро","2020-03-18","Бокс")

# def get_attachment(post_id):
#     connect = sqlite3.connect(database)
#     cursor = connect.cursor()
#     cursor.execute("SELECT * FROM attachment where post_id="+str(post_id))
#     res = cursor.fetchall()
#     connect.close()
#     attachments = []
#     for attachment in res:
#         attachments.append(attachment[1])
#     return attachments

# def update_group(group):
#     if group == "group2":
#         dialog = 2
#     elif group == "group3":
#         dialog = 3
#     elif group == "group4":
#         dialog = 4
#     elif group == "group5":
#         dialog = 5
#     connect = sqlite3.connect(database)
#     cursor = connect.cursor()
#     cursor.execute("SELECT id FROM posts")
#     last_id = cursor.fetchall()[-1][0]
#     cursor.execute("UPDATE posts SET dialog="+str(dialog)+" where id="+str(last_id))
#     connect.commit()
#     connect.close()

# def update_date(day,mounth,year):
#     new_date = str(datetime.date(int(year), int(mounth), int(day)))
#     connect = sqlite3.connect(database)
#     cursor = connect.cursor()
#     cursor.execute("SELECT id FROM posts")
#     last_id = cursor.fetchall()[-1][0]
#     cursor.execute("UPDATE posts SET date='"+new_date+"' where id="+str(last_id))
#     connect.commit()
#     connect.close()

# def update_time(post_time):
#     connect = sqlite3.connect(database)
#     cursor = connect.cursor()
#     cursor.execute("SELECT id FROM posts")
#     last_id = cursor.fetchall()[-1][0]
#     cursor.execute("UPDATE posts SET time='"+post_time+"' where id="+str(last_id))
#     connect.commit()
#     connect.close()

# def get_db(table):
#     connect = sqlite3.connect(database)
#     cursor = connect.cursor()
#     cursor.execute("SELECT * FROM "+table)
#     result = cursor.fetchall()
#     connect.close()
#     print(result)
