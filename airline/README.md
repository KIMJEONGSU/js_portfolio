# ✈️항공사 만족도 예측 모델

<br>

- 분석 기간 : 2023.02.03 ~ 2023.02.13
- 1인 프로젝트
- 기술스택

|Programming & Markup Language|__Python__|
|:--------:|:-------:|
|__IDE & Environment__|__colab__|
|__Model__| __Logistic, DecisionTree, RandonForest, XGBoost__|

<br>

### <목차>
1. 프로젝트 개요
2. 프로젝트 수행절차
- 데이터 소개
- 데이터 전처리
- target, 가설설정
- 모델 학습 및 평가, 가설 검증
3. 결과
4. 한계점 및 개선사항

<br>

### 1. 프로젝트 개요
신생 LCC가 가파른 시장 성장세를 이어나갈 것이라는 전망과 달리 항공업계에선 우려가 만만치 않다. 신규 LCC 합류로 소비자들의 선택 폭은 넓어질 수 있지만 공급과잉과 과당경쟁에 따른 수익성 악화로 이어질 수 있다는 시각이 우세하다. 그렇다면 소비자들이 우리 항공사를 선택할 수 있도록 고객 만족도 예측을 통해 파악하고, 불만 사항이 있다면 개선하려고 한다.

<br>

### 2. 프로젝트 수행절차  
#### 2.1. 데이터 소개
- 항공사 만족도 데이터( 129,487 row X 23 Columns )
  
|columns|Dtype|
|----------|-----------|
|gender|Oject|
|customer type|Oject|
|age|int|
|type of travel|Oject|
|class|Oject|
|flight distance|int|
|inflight wifi service|int|
|departure/arrival time convenient|int|
|ease of online booking |int|
|gate location|int|
|food and drink|int|
|online boarding|int|
|seat comfort|int|
|inflight entertainment|int|
|on-board service|int|
|leg room service |int|
|baggage handlig|int|
|checkin service|int|
|inflight service|int|
|cleanliness|int|
|departure delay in minutes|int|
|arrival delay in minutes|float|
|satisfaction|int|

출처 : kaggle
  
<br>

#### 2.2. 데이터 전처리 (Hold out 기법으로 데이터 분리 후 전처리 진행)
* 결측치 : 항공기 지연 시간에 대한 결측치 총 80개 삭제(샘플 데이터의 수가 충분하다고 판단)
* 타켓(satisfaction) : 불만족(0), 만족(1) 인 int 값으로 대체.
* 불필요한 컬럼 삭제  : id
* 특성이 범주형인 경우 카디널리티가 높지 않아 그대로 유지.

<br>

#### 2.3. target, 가설설정
* target : satisfaction 만족이냐 불만족이냐의 **분류 문제**
* 가설 설정
  1. 이코노미 좌석일수록 만족도가 낮다.
  2. 연령대가 높을수록 만족도가 낮다.
  3. 비행거리가 짧을 수록 만족도가 낮다.
  4. 충성 고객은 오히려 만족도가 더 낮다.

<br>

#### 2.4. 모델 학습 및 평가, 가설검증
2.4.1 모델학습
* Hold out 기법을 통해 train, val, test 3가지로 분리 후 전처리.
* 타켓 비율이 완전 불균형하지 않기 때문에 Accuracy 와 f1-score 평가지표 사용.
* 여러 모델 학습
  * Logistic Regression (기준모델)
  * DecisionTree
  * RandomForest
  * XGBoost

2.4.2 최종모델 선정 (XGBoost)
- Accuracy(0.96) 와 f1-score(0.97)가 가장 높기도 했지만, 해당 문제는 만족하지 않았는데 만족했다고 예측한 Type 1 ERROR가 더 중요하기 때문에 Precision(0.96)이 가장 높은 모델로 선택.

<table>
  <tr>
    <td>
      <img src="https://user-images.githubusercontent.com/23291338/233939744-d093c5cd-ef05-419b-8216-2bd1d18cbb8a.png" width="100%" height="100%"> 
    </td>
    <td>
      <img src="https://user-images.githubusercontent.com/23291338/233939807-fa86eca4-afd1-4f59-90cc-3ba43df4536a.png" width="100%" height="100%">  
    </td>
  </tr>
</table>

<br>

2.4.3 가설 검정
- EDA를 통해 가설 검정을 했을때 좌석 클래스가 낮을수록,  비행거리가 짧을수록, 충성고객일수록 만족도가 낮다 그리고 나이가 많을수록 만족도가 낮다고는 할 수 없다는 결과를 얻었다. 하지만 충성고객, 클래스, 나이, 비행 거리가 만족도에 중요한 특성이라고 생각했지만, MDI를 통해 예상과는 다르게 온라인 보딩잉 가장 영향력이 높은 특성이었다. 또한, PDP를 통해 각 특성이 증감소 할 때, 모델의 예측값이 어떻게 변하는지 알아보았지만, 영향력이 없었다.
  
<table>
  <tr>
    <td>
      <img src="https://user-images.githubusercontent.com/23291338/233937365-504e5d61-1a2f-49eb-ac98-6059320d072f.png" width="100%" height="100%">
    </td>
    <td>
      <img src="https://user-images.githubusercontent.com/23291338/233937582-974c9e34-9ec6-4882-8888-12d0cbaa4143.png" width="100%" height="100%">
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://user-images.githubusercontent.com/23291338/233938080-35ce644b-0243-4abe-a10b-ec5724d26137.png" width="100%" height="100%">
    </td>
    <td>
      <img src="https://user-images.githubusercontent.com/23291338/233938351-ebb2ab1d-86d8-451f-a12d-5caf50668d57.png" width="100%" height="100%">
    </td>
  </tr>
</table>

<br>

### 3. 결과
* 만족도에는 Online boarding의 특성 영향력이 가장 크다. 보통 종이탑승권을 발권하기 위해서는 카운터나 KIOSK를 이용하기 위해 직접 방문해야한다. 하지만 모바일 탑승권을 발행하면 굳이 방문하지 않아도 바로 비행기 탑승이 가능하다. 
* 즉, 비행기 탑승까지의 과정이 축소된다면 고객의 만족도를 높일 수 있다고 생각한다. 
* 또한,  그 외에도  "Inflight wifi service“, "Inflight entertainment“의 특성 영향력도 높았다. 기내 안에서 즐길 거리가 다양하다면 고객의 만족도를 높일 수 있다고 생각한다.

<br>

### 4. 한계점 및 개선사항
* Data Set 자체로 봤을 때, 데이터 정제가 거의 필요 없는 상태라서 다양한 전처리, Feature Engineering을 해보지 못한 아쉬움. 
추후에 Kaggle Data 아닌 웹 크롤링 등을 이용해 직접 수집하고 다양한 전처리와 Feature Engineering을 시도해 볼 것.
* 모든 특성에 대해 알아보지 못한 점.
* 추후에 특성 중요도에 따라서 불필요한 컬럼을 추가로 삭제 후 성능 확인.
* PDP 해석하는데 조금 어려움이 있어서 다양한 사례를 보면서 해석해 볼 것.

