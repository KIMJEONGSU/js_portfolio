from flask import Flask, render_template, request
import pickle
import psycopg2

app = Flask(__name__, static_folder='static')

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="1234",
    port="5432"
)
# 모델 객체를 언피클링
with open("doc2vec_model.pkl", "rb") as f:
    doc_vectorizer = pickle.load(f)

@app.route('/',methods=['GET','POST'])
def first_index():
    if request.method == "POST":
        input_value = request.form['input_value']


        # 불러온 모델을 이용하여 추론
        result = doc_vectorizer.dv.most_similar(input_value, topn=5)

        cur = conn.cursor()
        # cur.execute("DROP TABLE IF EXISTS result;")
        # cur.execute("""CREATE TABLE result(
        #     input_name VARCHAR(10),
        #     name VARCHAR(10),
        #     number FLOAT);""")

        for row in result:
            cur.execute(f"INSERT INTO result VALUES (%s,%s,%s)",(input_value,row[0],row[1]))
        conn.commit()

        return render_template('first_page.html', result=result)
    return render_template('first_page.html')


# 아래 주석을 풀고, 웹 애플리케이션을 실행해 보세요.
if __name__ == "__main__":
    app.run(debug=True)