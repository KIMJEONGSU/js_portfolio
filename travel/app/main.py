# Flask 애플리케이션과 필요한 패키지 import
from flask import Flask, render_template, request, jsonify
from bigquery import clinet_bigquery
import json

# Flask 애플리케이션 생성. 정적 파일 제공을 위한 path 설정.
app = Flask(__name__, static_url_path="/static")

# 전역변수 총합 초기화
total_amount = 0

# /루트 URL에 접근하면 calendar 함수가 실행되어 main.html 템플릿을 렌더링.
@app.route('/')
def calendar():
    return render_template('main.html')

# /demo URL에 접근시 demo 함수 실행.
@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # POST 요청을 받았을시 메세지 반환.
    if request.method == 'POST':
        data = request.form.get('data')
        return "POST 요청을 받았습니다"
    # GET 요청을 받았을시 Bigquery에서 데이터를 가져와 json로 변환하여 반환.
    else:
        sql = '''
            SELECT date, CAST(AVG(charge) AS INT64) AS avgcharge, MIN(charge) AS mincharge, MAX(charge) AS maxcharge
            FROM test_db.airplanecrawl
            GROUP BY date
            LIMIT 200;
        '''
        data_list = clinet_bigquery(sql)
        json_data = data_list.to_json(orient='records')

        return jsonify(json_data)

# 항공권 데이터
air_data = clinet_bigquery('''
                            SELECT date, day, name, airport, leavetime, reachtime, seat,charge
                            FROM test_db.airplanecrawl
                            WHERE date = '2023-07-01'
                            ORDER BY charge ASC
                            LIMIT 200;
                            ''')
# 호텔 데이터
hotel_data = clinet_bigquery('''SELECT * FROM test_db.hotelcrawl
                                where rating != '평점없음' and star is not null
                                order by star desc, price asc
                                LIMIT 200;''') 
# 렌터카 데이터
car_data = clinet_bigquery('''SELECT  carname, oiltype, seater, avg_year,
                            CAST(AVG(CAST(regular_price AS INT)) AS INT) AS avg_regular_price,
                            CAST(AVG(CAST(discounted_price AS INT)) AS INT) AS avg_discounted_price
                            FROM `fightproject.test_db.car`
                            WHERE regular_price != '마감' AND discounted_price != '마감'
                            GROUP BY carname, oiltype, seater, avg_year
                            ORDER BY avg_discounted_price, avg_regular_price
                            LIMIT 200;''') 

# /filght URL에 접근시 get_flight 함수 실행.
@app.route('/filght', methods=['GET','POST'])
def get_flight():
    air_list = air_data.to_dict(orient='records')
    hotel_list = hotel_data.to_dict(orient='records')
    car_list = car_data.to_dict(orient='records')

    # POST 요청을 받았을 때 사전에 로딩한 데이터를 json 형태로 반환.
    if request.method=='POST':
        return jsonify(air_list=air_list, hotel_list=hotel_list, car_list=car_list)
    # GET 요청을 받았을때 렌더링할 flight.html 템플릿에 데이터를 넘김.
    else:
        return render_template('filght.html', air_list=air_list, hotel_list=hotel_list, car_list=car_list)


# /filghtDate URL에 접근시 filghtDate 함수 실행.
@app.route('/filghtDate', methods=['GET','POST'])
def filghtDate(selectedDate=None,statusselect1=None, statusselect2=None):
    # POST요청 시 pass
    if request.method == 'POST':
        pass
    # GET 요청 시 선택한 날짜와 기타 필터 조건에 따라 데이터를 조회하여 반환.
    else:
        selectedDate = request.args.get('selectedDate')
        statusselect1 = request.args.get('statusselect1')
        statusselect2 = request.args.get('statusselect2')
        print("geT------------------------",statusselect1)
        print("geT------------------------",statusselect2)
        sql = f'''
            SELECT date, day, name, airport, leavetime, reachtime, seat,charge
            FROM test_db.airplanecrawl
            WHERE date = '{selectedDate}' AND airport = '{statusselect2}'
            AND (
                    ({statusselect1} = 0 AND charge >= 0) OR
                    ({statusselect1} = 1 AND charge >= 0 AND charge < 50000) OR
                    ({statusselect1} = 2 AND charge >= 50000 AND charge < 100000) OR
                    ({statusselect1} = 3 AND charge >= 100000 AND charge < 150000)OR
                    ({statusselect1} = 4 AND charge >= 150000 AND charge < 200000)OR
                    ({statusselect1} = 5 AND charge >= 200000 )
                )
            ORDER BY charge ASC
            LIMIT 200
            '''
        air_data = clinet_bigquery(sql)
        air_list = air_data.to_dict(orient='records')
        hotel_list = hotel_data.to_dict(orient='records')
        car_list = car_data.to_dict(orient='records')
        return render_template('filght.html', air_list=air_list, hotel_list=hotel_list, car_list=car_list)

# /hotelprice URL에 접근 시 hotelprice함수 실행.
@app.route('/hotelprice', methods=['GET','POST'])
def hotelprice(statusselect3=None,statusselect4=None ):
    # POST 요청시 pass
    if request.method == 'POST':
        pass
    # GET 요청시 호텔 가격과 기타 필터 조건에 따라 데이터를 조회하여 반환.
    else:
        statusselect3 = request.args.get('statusselect3')
        statusselect4 = request.args.get('statusselect4')
        print("geT------------------------",statusselect3)
        print("geT------------------------",statusselect4)
        sql = f'''
                SELECT * 
                FROM test_db.hotelcrawl
                where rating != '평점없음' and star is not null
                AND (
                    ({statusselect3} = 0 AND price >= 0) OR
                    ({statusselect3} = 1 AND price >= 0 AND price < 30000) OR
                    ({statusselect3} = 2 AND price >= 30000 AND price < 50000) OR
                    ({statusselect3} = 3 AND price >= 50000 AND price < 100000)OR
                    ({statusselect3} = 4 AND price >= 100000 AND price < 200000)OR
                    ({statusselect3} = 5 AND price >= 200000 )
                )
                AND  address = '{statusselect4}'
                order by star desc, price asc
                LIMIT 200;
                '''
        hotel_data = clinet_bigquery(sql)
        air_list = air_data.to_dict(orient='records')
        hotel_list = hotel_data.to_dict(orient='records')
        car_list = car_data.to_dict(orient='records')

        return render_template('filght.html', air_list=air_list, hotel_list=hotel_list, car_list=car_list)


# /dashboard1 URL에 접근하면 dashboard1.html 템플릿을 렌더링
@app.route('/dashboard1') 
def dashboard1():
    return render_template('dashboard1.html')

if __name__ == '__main__':
    # aws 웹 api배포를 위해 host, port 설정, SSL 인증서 적용
    app.run(host='0.0.0.0',port='8080',debug=True, ssl_context=('ssl/cert.pem','ssl/cert.key'))  
