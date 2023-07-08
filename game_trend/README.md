# 🎮게임 트렌드와 출시를 위한 분석 프로젝트
<br>

- 분석 기간 : 2022.12.30 ~ 2023.01.05
- 1인 프로젝트
- 기술 스택
- 
|Programming & Markup Language|__Python__|
|:--------:|:-------:|
|__IDE & Environment__|__colab__|

<br>

### <목차>
1. 프로젝트 개요
2. 프로젝트 수행절차
- 데이터 소개
- 데이터 전처리
- EDA, 가설설정 및 검증
3. 결과
4. 회고

<br>

### 1. 프로젝트 개요

* 시장 조사 업체인 NPD에 따르면 미국 뿐만 아니라 전세계적으로 게임 시장 매출 감소가 포착되고 있다. 코로나 19 회복 국면에서 게임 이용 시간 감소가 더해지고 게임 시장이 장기 침체 국면에 빠져드는 것 아니냐는 우려가 나오고 있다. 대부분의 게임 기업들이 매출 하락을 겪고 있는 가운데, EA의 매출은 전년 동기 대비 14% 증가한 17억 6,700만 달러를 기록했고,  EA는  시리즈의 성공적인 출시 덕분이라고 한다.    
* 그렇다면 우리 회사도 어떤 게임을 설계하고 출시 할지에 대한 고민이 필요하다.

<br>

### 2. 프로젝트 수행절차  
#### 2.1. 데이터 소개
 |columns|explanation|Dtype|
|----------|-----------|----------|
|name|게임 이름|Oject|
|platform|게임이 지원되는 플랫폼 이름|Oject|
|year|게임 출시 연도|float|
|genre|게임 장르|Oject|
|publisher|게임 배급하는 회사|Oject|
|NA_Sales|북미지역의 출고량|Oject|
|EU_Sales|유럽지역의 출고량|Oject|
|JP_Sales|일본지역의 출고량|Oject|
|Other_Sales |기타지역의 출고량|Oject|

<br>

#### 2.2. 데이터 전처리
* Year는 실수형이 아닌 정수형으로 변경해준다.
* Year의 경우 nan값이 71개로 결측치 처리 후에 타입 변환.
* Genre, Publisher의 결측치 처리
* NA_Sales, EU_Sales, JP_Sales, Other_Sales 은 object가 아닌 float으로 데이터 타입 변경.데이터에 문자열이 없는지 체크하고 타입변환.
* Genre Year Publisher   
  * 결측치 비율 - 각각 0.3%, 16%, 0.3%
  * genre, publisher는 결측치 비율이 낮아서 drop하지만, year의 경우 16%이다.
  * Year의 평균값이나 최빈값을 넣거나, 그룹을 지어서 그룹의 평균값을 넣으려고 했지만, 어떤 그룹으로 묶냐에 따라서도 결과가 달라지기 때문에 과감히 drop
  * Year : 연도는 실수형이 아닌 정수형으로 변경. 그리고 2자리에서 4자리로 변경.
* NA_sales EU_Sales JP_Sales Other_Sales
  * 각 지역의 출고량 단위 맞추기
  * 중복값 확인

```
# 연도 2자리에서 4자리로 바꾸기
for i in range(20):
  df.loc[df['Year'] == i, 'Year'] = 2000+i
df.loc[df['Year'] < 100, 'Year'] += 1900

# 출고량 컬럼들 단위 맞춰주기
df[df['NA_Sales'].str.contains(r"[a-zA-Z]")==True]


# 단위가 k인 경우 정수형이고, M인 경우 실수형으로 표현되어있따. 
# M인 경우는 단위를 없애주고, k인경우 0.001을 곱해 단위 맞춰준다.
df['NA_Sales'] = df['NA_Sales'].replace({'[kK]': '*0.001', '[mM]': ''}, regex=True).map(pd.eval).astype(float)
df['EU_Sales'] = df['EU_Sales'].replace({'[kK]': '*0.001', '[mM]': ''}, regex=True).map(pd.eval).astype(float)
df['JP_Sales'] = df['JP_Sales'].replace({'[kK]': '*0.001', '[mM]': ''}, regex=True).map(pd.eval).astype(float)
df['Other_Sales'] = df['Other_Sales'].replace({'[kK]': '*0.001', '[mM]': ''}, regex=True).map(pd.eval).astype(float)

# 중복값
df.duplicated().sum()
```

<br>

#### 2.3. EDA, 가설설정 및 검증
- 전체적으로  ACTION, SPORTS 순으로 많이 출시되고 있음.
<img src="https://user-images.githubusercontent.com/23291338/233901819-7755657d-2a96-4734-b1e0-0edd47a5f282.png" alt="image" width="700" height="500">

- 북미, 유럽, 기타 지역의 경우 동일하게 ACTION, SPORTS 를 선호하고, 다른 지역과 다르게 일본은 ROLE-PLAYING, ACTION을 선호한다.
<img src="https://user-images.githubusercontent.com/23291338/233901848-450813a1-890d-4285-b842-7f62cae74cfb.png" alt="image" width="700" height="500">

- 지역별 장르다 다른지 알고 싶기 때문에 이것을 대립가설로 설정하고 지역별 장르가 같다를 귀무가설로 설정.
현재 비교하려는 집단은 북미, 유럽, 일본, 기타 총 4개이므로 ANOVA 가설검정 진행하려고 했지만, 한 집단에서 정규성을 위배하여 KRUSKAL WALIIS TEST 진행.
결과적으로 P-VALUE는 0.0002로 기준인 0.05보다 작으므로 귀무가설 기각, 대립가설 채택.
<img src="https://user-images.githubusercontent.com/23291338/233901881-e8d00504-8f9f-4ecd-ba74-ee1e6463f049.png" alt="image" width="700" height="500">

- 트렌드는 어떤 방향으로 쏠리는 현상을 뜻한다. 
어떤 제품을 유저들이 많이 선호하고, 그만큼 회사에서 많이 출시하는 것. 이것이 어떤 방향으로 쏠리는 현상인 트렌드라고 생각했다. 
게임 출시량과 출고량 즉 선호도가 높은 기준으로 트렌드를 파악하였다.
현재 이 그래프에서는 2003~2016s까지는 action 출시량이 많은 것을 알 수 있다.
<img src="https://user-images.githubusercontent.com/23291338/233901924-254a7e68-f282-4277-af38-0d6f8548b8a5.png" alt="image" width="700" height="500">

- 출고량이 많은 즉, 선호도가 높은 장르는 2001~2016s 까지는 대부분 action 장르의 게임이 많이 선호된 것을 확인할 수 있었고, 이를 통해 action 게임 장르의 트렌드가 있는 것을 확인할 수 있었다.
<img src="https://user-images.githubusercontent.com/23291338/233901959-496a74b4-1696-427e-9f35-ee5a62010ac9.png" alt="image" width="700" height="500">

- 플랫폼 종류가 너무 많아서 범주를 축소하고자 3대 콘솔게임인 플레이 스테이션, 닌텐도, 엑스박스 그리고 나머지 콘솔게임, PC게임, 모바일게임으로 범주를 축소하였다.
모두 플레이스테이션이 40.3%,21.7%로 가장 많이 차지하고 있었다.
<img src="https://user-images.githubusercontent.com/23291338/233902048-735515c7-b502-46d3-a1b5-b409ac4cadd3.png" alt="image" width="700" height="500">

- 지역별 게임 출고량을 통해 선호하는 플랫폼이 어떤것인지 알아보았다. 마찬가지로 플레이스테이션이 우세했다.
<img src="https://user-images.githubusercontent.com/23291338/233902096-97c53193-029d-4bab-9550-f2d7e9c27b43.png" alt="image" width="700" height="500">

- 출시된 게임을 지원한 플랫폼 중에 플레이스테이션이 가장 많았다는 것과 출고된 게임 중 지원된 플랫폼도 플레이스테이션이 가장 많다는 점을 알 수 있다.
<img src="https://user-images.githubusercontent.com/23291338/233902133-9f2695a3-93db-4300-9dbe-5e14e7d47ffd.png" alt="image" width="700" height="500">

- 게임을 지원하는 플랫폼 중 플레이 스테이션이 가장 많이 차지할 수 있음을 알 수 있었다.  추가로 연도별 가장 많이 지원되는 플랫폼에 대해 알아보았다. 
1995s부터 플레이스테이션 시리즈(PS, PS2 ,PS3 ,PS4 순으로)가 인기있음을 알 수 있다.
<img src="https://user-images.githubusercontent.com/23291338/233902169-816ab0b5-d372-4475-a8f7-63ff2c321f94.png" alt="image" width="700" height="500">

- 출고됐던. 즉 선호했던 플랫폼은 PS, ps2, WILL, X360, PS3, PS4 순으로 닌텐도나 엑스박스 플랫폼도 인기 있었지만, 꾸준히 플레이스테이션이 선호했던 플랫폼이라는 점도 알 수 있다.
<img src="https://user-images.githubusercontent.com/23291338/233902197-0fb41581-0ad1-41e1-9442-d0def7996e46.png" alt="image" width="700" height="500">

- 연도별로 지역의 출고량을 나타낸 그래프이다. 지역 모두 비슷한 증감추이를 보이고 있고, 출고량으로 봤을땐 북미 지역이 가장 많다는 것을 알 수 있다.
<img src="https://user-images.githubusercontent.com/23291338/233902224-f3a8c412-6656-49f5-bba8-c553702d4227.png" alt="image" width="700" height="500">

- 장르는 액션, 플랫폼은 플레이스테이션으로 지정하여 지역별 출고량에 대해 알아보았다. 마찬가지고 북미의 출고량이 가장 많았다.
<img src="https://user-images.githubusercontent.com/23291338/233902257-06ab60c1-d3d1-488d-9b2a-6261e990300f.png" alt="image" width="700" height="500">

<br>

### 3. 결과
* 게임시장은 이미 포화상태이다.  분석을 통해서 가장 이익이 되고 인기가 있는 장르와 플랫폼에 대해서 알아보았지만, 이미 포화상태인데 플레이스테이션으로 지원되는 액션 장르의 게임을 설계했을 때 과연 이익이 날까 라는 의구심도 들었다. 그래서 내린 결론은 트렌드를 쫓아가되, 우리 회사만이 만들 수 있는 게임을 만드는 것이 가장 중요하다고 생각한다.
* 분석을 통해 플랫폼을 하나로 지정은 했지만,   2021년 자료 조사에 따르면 플랫폼의 전환은 크로스 플레이를 지원하는 양상으로 전개되고 있다고 한다. 플랫폼과 상관없이 다양한 사람들과 게임을 할 수 있는 것.  즉 멀티 플랫폼이 트렌드가 될 것이라 생각된다.

<br>

### 4. 회고
* 기간이 정해져있어서 더 다양한 분석을 하는데 조금 한계가 있었다. 그래서 시간관리와 계획이 중요하다는 것을 알게 되었다.
* 게임 도메인 지식이 부족하다보니, 결측치를 어떻게 처리할 것인지 등에 대해 막히는 부분이 많았다. 그만큼 도메인에 대한 지식이 중요하다는 것을 알게되었다.
* 목표를 정했음에도 불구하고 데이터를 분석하다가 목표와 맞지 않는 분석을 하는 경우도 종종 있는 것을 알게 되었다. 항상 목표에 맞는 분석을 하도록 해야겠다.
* 또한 다른 팀원들의 발표 영상을 보면서 다양한 분석 관점과 비즈니스 관점에 대해 습득할 수 있었다. 추후에도 다양한 사례들을 보면서 관점을 넓혀가야겠다.
