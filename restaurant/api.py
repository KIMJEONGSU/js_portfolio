# 도커로 서울의 음식점에 대한 DB적재
import psycopg2
import os
import csv

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="1234",
    port="5432"
)

DB_FILEPATH_seoul = os.path.join(os.getcwd(), 'seoul_food_store.csv')
DB_FILEPATH_seoul_review = os.path.join(os.getcwd(), 'seoul_review.csv')
DB_FILEPATH_seoul_last = os.path.join(os.getcwd(), 'last_data.csv')

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS seoul_food_store;")
cur.execute("DROP TABLE IF EXISTS seoul_store_review;")
cur.execute("DROP TABLE IF EXISTS last_data;")

cur.execute("""CREATE TABLE seoul_food_store(
            id INTEGER PRIMARY KEY,
            Business_name VARCHAR(128),
            address VARCHAR(128),
            middle_category VARCHAR(128),
            small_category VARCHAR(128),
            industry_classification VARCHAR(128),
            Dongmyeong VARCHAR(128),
            Latitude FLOAT,
            Hardness FLOAT);""")

cur.execute("""CREATE TABLE seoul_store_review(
        id INTEGER PRIMARY KEY,
        name VARCHAR(128),
        address VARCHAR(128),
        middle_category VARCHAR(128),
        small_category VARCHAR(128),
        industry_classification VARCHAR(128),
        Dongmyeong VARCHAR(128),
        URL VARCHAR(128),
        kakao_star_point FLOAT,
        kakao_star_point_qty INTEGER,
        kakao_blog_review_txt TEXT,
        kakao_blog_review_qty INTEGER);""")    

cur.execute("""CREATE TABLE last_data(
        name VARCHAR(128),
        address VARCHAR(128),
        middle_category VARCHAR(128),
        small_category VARCHAR(128),
        industry_classification VARCHAR(128),
        Dongmyeong VARCHAR(128),
        kakao_star_point FLOAT,
        kakao_star_point_qty INTEGER,
        kakao_blog_review_txt TEXT,
        kakao_blog_review_qty INTEGER,
        mix_cate VARCHAR(128));""") 
  
with open(DB_FILEPATH_seoul,'r',encoding='utf-8') as file_seoul:
    f_seoul=csv.reader(file_seoul)
    next(f_seoul)
    list_f_seoul = list(f_seoul)
    for i,row in enumerate(list_f_seoul):
        cur.execute(f"INSERT INTO seoul_food_store VALUES ({i+1},%s,%s,%s,%s,%s,%s,%s,%s)",
                    (row[0],row[1],row[3],row[4],row[5],row[6],row[7],row[8]))

with open(DB_FILEPATH_seoul_review,'r',encoding='utf-8') as file:
    f=csv.reader(file)
    next(f)
    list_f = list(f)
    for i,row in enumerate(list_f):
        cur.execute(f"INSERT INTO seoul_store_review VALUES ({i+1},%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[8],row[9],row[10],row[11]))
        
with open(DB_FILEPATH_seoul_last,'r',encoding='utf-8') as file:
    f=csv.reader(file)
    next(f)
    list_f = list(f)
    for i,row in enumerate(list_f):
        cur.execute("INSERT INTO last_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]))

        
cur.close()
conn.commit()
conn.close()



