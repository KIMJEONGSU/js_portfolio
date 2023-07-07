import pickle
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

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS result;")
cur.execute("""CREATE TABLE result(
            input_name VARCHAR(10),
            name VARCHAR(10),
            number FLOAT);""")

# 저장된 모델을 불러올 파일 이름
model_filename = "doc2vec_model.pkl"

# 모델 객체를 언피클링
with open(model_filename, "rb") as f:
    doc_vectorizer = pickle.load(f)

input_name = input()

# 불러온 모델을 이용하여 추론
result = doc_vectorizer.dv.most_similar(input_name, topn=5)

for row in result:
    cur.execute(f"INSERT INTO result VALUES (%s,%s,%s)",(input_name,row[0],row[1]))


        
cur.close()
conn.commit()
conn.close()
