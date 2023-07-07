# 인도네시아 이커머스 플랫폼 개선 프로젝트

<br>

### <목차>
1. 프로젝트 개요
2. 프로젝트 수행절차   
   2.1 데이터 소개   
   2.2 EDA   
   2.3 문제정의   
   2.4 결과   
3. 한계점 및 개선사항

<br>

#### 1. 프로젝트 개요
1.1 프로젝트 배경
- Fashion Campus는 15-35세의 젊은 층인 "Indonesian Young Urbans"의 시장 점유율을 보유한 전자 상거래 패션 회사입니다. 젊은 세대들에게 사랑받는 국내외 브랜드의 제품을 제공하며 10,000명의 고객을 확보하고, 매달 100,000건 이상의 구매가 이뤄지고 있습니다. 하지만 유기적이지 않은
사용자 수의 영향으로 인해 사용자들이 거래를 위해 플랫폼으로 돌아오지 않았고, 이탈률이 높아졌습니다. 이를 해결하고 이탈 예측하고자 합니다.

1.2 프로젝트 목표
- Fashion Campus의 현황을 파악하여 문제진단, 액션 도출
- 이탈 원인을 파악하고 이탈 예측 모델 개발
  
<br>


#### 2. 프로젝트 수행절차   
2.1 데이터 소개  
<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/11d76724-a988-4225-900a-f1ea1ddfb750" width="70%" height="70%">
    </td>
    <td>     
        <p><customer 데이터></p>
        <p>- 100,000 rows X 15 columns  </p> 
        <p>- Fashion Campus에 가입한 고객들의 데이터</p>   
        <p>- 고객 ID와 성별, 나이, 디바이스 운영체제, 거주지, 가입날짜 등에 대한 정보 제공</p>   
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/2058132c-a9c3-4c1f-b1c3-1950462282c4" width="70%" height="70%">
    </td>
    <td>     
      <p><product 데이터></p>
      <p>- 44,424 rows X 10 columns</p> 
      <p>- Fashion Campus에서 판매되는 제품에 대한 데이터</p>   
      <p>- 제품 ID, 성별, 카테고리, 출시연도, 계절 등에 대한 정보 제공</p>   
    </td>
  </tr>
    <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/84ff5aea-94d6-4344-ae91-67647ae7b5b1" width="70%" height="70%">
    </td>
    <td>     
      <p><click_stream_new 데이터></p>
      <p>- 12,833,602 rows X 12 columns</p> 
      <p>- 신규 가입 후 세션을 활성화하거나 제품 주문을 한 고객들의  로그 데이터 </p>   
      <p>- 세션 ID, 이벤트 네임과 시간, 구매 시 사용 기기 등에 대한 정보 제공</p>   
    </td>
  </tr>
    <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/51836d64-77e4-481e-8f09-ac46e6b8a4b7" width="70%" height="70%">
    </td>
    <td>     
      <p><transaction_new 데이터></p>
      <p>- 1,254,585 rows X 16 columns</p> 
      <p>- Fashion Campus에서 고객이 구매한 것에 대한 정보를 제공해 주는 구매 데이터</p>   
      <p>- 주문 일자, 고객 ID, 예약 ID, 세션 ID, 프로모션 코드, 결제 성공 여부, 배송비, 배송 제한 날짜, 결제 금액 등에 대한 정보 제공</p>   
    </td>
  </tr>
</table>

<br>

2.2 EDA  
* 결측치 & 이상치
   * transaction_new, click_stream_new, product 데이터의 NaN 값과 수치형 변수(배송비, 제품 가격, 총합 등)의 Outlier 존재하지만, 
삭제 시 고객이 주문한 상품에 대한 정보를 파악할 수 없어서 그대로 유지 후 분석    
<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/cbb3d4e6-3a71-48b3-8c1e-2231611f69a5" width="90%" height="90%">
       <p><총합 outlier></p>
    </td>
    <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/595f20e1-6a45-4ebd-8131-f7c0ae3b05de" width="100%" height="100%">  
       <p><배송비 outlier></p>
    </td>
  </tr>
</table>

* 데이터 처리시 주의 사항
   * transaction_new의 경우 각 행에 고객의 구매 내역을 제품별로 기록한 데이터. 하지만 총합의 경우 모든 행에 동일한 값으로 입력되어 있어서 이를 인지하지 않고 그대로 사용하면 잘못된 정보를 얻게 될 수 있기 때문에 주의 필요

<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/a43bba88-06e5-404c-9dad-9fb3de299f31" width="90%" height="90%">
       <p><연령층></p>
          <p>15-35세가 주요 연령층인 만큼 20대가 52%</p>
    </td>
    <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/7396ed48-3dd7-4b4b-b9da-521b4a530cdf" width="100%" height="100%">  
       <p><성별></p>
      <p>여성 64%, 남성 36%</p>
    </td>
   <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/d62696a9-8aa1-4000-a8ed-f459aa825a6c" width="100%" height="100%">  
       <p><거주지 분포></p>
          <p>인도네시아 전 지역에 고루 분포</p>
    </td>
  </tr>
 <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/21f85d39-b093-4ec6-ae20-6be9077111c3" width="100%" height="100%">
       <p><결제방식></p>
          <p>많이 사용하는 방식으로는 신용카드 35%, Gopay & OVO 20% </p>
    </td>
    <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/76c63ff7-2771-4d70-a2ee-b6cc7a46a1dc" width="100%" height="100%">  
       <p><프로모션 적용 여부></p>
          <p>적용하지 않는 경우가 61.7%로 고객들이 프로모션을 잘 사용하지 않고 있음</p>
    </td>
   <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/4f2e1ca0-792b-4260-83bd-bdee3f99d2db" width="85%" height="85%"> 
       <p><계절별 상품비율></p>
          <p>여름 제품 48%, 가을 제품 26% 순으로 많음</p>
    </td>
  </tr>
 <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/b803764b-c4d7-48c2-b05f-6b7737a6578f" width="90%" height="90%">
       <p><성별에 따른 상품></p>
          <p>여성이 64%로 많지만 남성 제품이 약 50%로 가장 많음</p>
    </td>
    <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/5fc3458f-d0f6-4302-b4ed-6c3d970c0cfb" width="100%" height="100%">  
       <p><상품 스타일></p>
          <p>인도네시아 특성상 캐주얼 제품이 78%로 가장 많음</p>
    </td>
    <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/d454e5a4-ed37-4380-9b94-e8b4678d2361" width="90%" height="90%"> 
       <p><상품 카테고리></p>
          <p>Apparel이 49.2%로 가장 많이 차지</p>
    </td>
  </tr>
 <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/d8a42558-6faa-40ea-9637-d885fea8fc98" width="90%" height="90%">
       <p><세부 카테고리></p>
          <p>Topwear(34.7%), shoes(16.5%) 순으로 가장 많이 차지</p>
    </td>
    <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/d99aa517-74ba-4b02-af8c-a14835131645" width="100%" height="100%">  
       <p><형식 카테고리></p>
          <p>Tshirts (15.9%) 가 가장 많이 차지</p>
    </td>
  </tr>
</table>

* 세션 재정의
   * 인도네시아 타 이커머스 플랫폼의 평균 체류시간은 평균 3분에서 6분 정도. 하지만 현 이커머스 플랫폼의 평균 체류 시간이 10일    이상이고, 이를 이상치로 판단하여 세션 재정의 진행
   * 30분 이상 동작이 존재하지 않으면 다른 세션으로 정의(세션 수 5,904,346개로 기존보다 약 10.7배 증가)
   * 평균 체류 시간 : 2분 26초
   * 구매 전환율 : 8.61%
<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/cff5f065-dc8b-4107-ae9c-482087f65c1d" width="90%" height="90%">
       <p><시간별 구매전환율></p>
          <p>오후 3시이후부터 오전 5시이전까지 높은 구매전환율</p>
    </td>
    <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/43cde7f6-3336-452e-b2f7-4b00cd0d3f3e" width="100%" height="100%">  
       <p><월별 구매전환율></p>
      <p>7월에 높은 구매전환율</p>
    </td>   
</table>  

- 신규 가입자의 유입 : 매년 신규 가입자가 꾸준히 증가하고 7월에 폭발적인 신규 가입자가 유입되고 있음.
![image](https://github.com/KIMJEONGSU/Portfolio/assets/23291338/5cc9189b-d837-417b-a8a9-93179bb6cca6)

- 매출의 감소 : 꾸준히 상승세였던 매출이 2022년 6월과 7월, 2개월 연속으로 감소함.
   - 전월 대비 7월 감소율 ▼11.67% ( 전월 대비 6,7월 총 감소율 ▼16.26%)
![image](https://github.com/KIMJEONGSU/Portfolio/assets/23291338/75ac0a12-235f-4ce9-8ec3-03c86e65e944)

<br>

2.3 문제정의   
* **최근 2개월 연속 매출하락**이라는 문제를 정의했고, 3가지 내부 요인을 찾을 수 있었음.

1. 일회성 고객의 증가
<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/2c772e1e-8549-4a37-bbf1-bdba7779dd89" width="100%" height="100%">
       <p><연도별 비활성 고객률></p>
    </td>
    <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/441945ac-c475-4ddc-9a83-84b3373ea58e" width="90%" height="90%"> 
       <p><연도별 일회성 고객의 매출></p>
    </td>
</tr>
</table>  
          
* 최근 2개월 연속 매출 하락으로 인해 비활성 고객 비율 조사 결과, 가입연도가 2021년, 2022년인 경우 비활성 고객률이 53.1%, 59.5%를 차지했고, 재구매율 또한 계속 상승하다가 2022년 하락.
* 꾸준히 고객 유입이 있음에도 불구하고 매출의 하락과 비활성 고객율이 증가하였음. 재구매율의 하락을 통해 일회성 고객이 증가하고 있는지에 대한 의문 제기.

<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/1e92a6fc-3098-445c-aa41-6eda0a7c50e4" width="100%" height="100%">
       <p><연도별 일회성 고객률></p>
    </td>
    <td>     
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/01ac09c2-8af4-42c6-a4cc-d825d26d11c2" width="90%" height="90%"> 
       <p><연도별 일회성 고객의 매출></p>
    </td>   
</table>  

* 일회성 고객률이 하락하고 있었지만,  유지 또는 상승하는 경향으로 바뀐 2022년 시점에서 매출이 감소함을 확인하고 일회성 고객의 유지 또는 증가하는 경향성이 영향을 주었다고  생각되어 일회성 고객을 충성고객으로 전환시킬 필요가 있다고 판단
<img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/d0a03dde-0b74-4f07-b253-86767e4d7a1b" width="70%" height="70%">

* 한 번도 구매하지 않은 고객을 제외한 후(50,705명), 고객별 평균 구매주기를 봤을 때 당일에 구매 후 이탈하는 고객이 20%, 29일 이후로 구매하는 고객이 60%를 차지. 이 그래프를 통해서도 일회성 고객을 더 세부적으로 분석해 볼 필요가 있다고 판단
* 일회성 고객의 특징
<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/4c7b074f-41f4-4066-b0b2-7d0f075d21a1" width="50%" height="50%">
      <p><일회성 고객의 구매 상품 카테고리></p>
    </td>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/622812c1-f16e-47c2-8679-46eb2761a1a0" width="100%" height="100%">
      <p><일회성 고객의 구매 요일></p>
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <p><일회성 고객의 특징 1></p>
      <p>일회성 고객의 특징 1
        주로 구매하는 제품은 Apparel(48%), Accessories(25%), Footwear(20%) 순으로 많이 구매
        일회성 고객들은 일, 월, 토 순으로 구매</p>  
    </td>
  </tr>
 <tr>
    <td colspan="2">
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/2ec6e0ee-c59b-4ac2-9ee2-81f139508c5a" width="80%" height="80%">
       <p><일회성 고객의 전체 검색 비율과 중고 검색에 대한 비율></p>
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <p><일회성 고객의 특징 2></p>
      <p>Dress Kondangan(이슬람 전통복장)에 대한 검색 비율 35%, 중고에 대한 검색은 약 17% 정도</p> 
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/5b49926a-1930-458d-b4e8-3615ea750103" width="90%" height="90%">
       <p><2022년 월별 일회성 고객과 다회성 고객의 객단가 비교 그래프></p>
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <p><일회성 고객의 특징 3></p>
      <p> 2022년 기준 매출이 하락했던 6월~7월에는 일회성 고객의 객단가가 다른 월과 비교했을 때 낮고, 
그중 7월이 가장 낮음</p>   
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/3936ea69-e56c-4c19-adf2-4a887b1c62ca" width="80%" height="80%">
      <p><일회성 고객의 프로모션 사용 여부></p>
    </td>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/56d467c4-f34c-493e-a4c3-35df7d5fd921" width="100%" height="100%">
      <p><다회성 고객의 프로모션 적용 여부></p>
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <p>일회성 고객의 특징 4</p>
      <p>일회성 고객 프로모션 사용 비중을 확인했을 때, 사용하지 않는다가 63.5% 차지.
        추가로 다회성 고객 또한 68.3%로 프로모션을 사용하지 않음</p>
    </td>
  </tr>
         
<tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/3d71abca-3ae2-4427-8b0a-0accba704055" width="80%" height="80%">
      <p><일회성 고객의 나이대 분포></p>
    </td>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/de66acf6-4317-46c9-a6ff-81b5be2c738d" width="100%" height="100%">
      <p><나이별 평균 이탈율></p>
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <p>일회성 고객의 특징 5</p>
      <p>20대가 51%로 가장 많이 차지하며, 나이가 적고 많을수록 이탈률이 낮음</p>
    </td>
  </tr>

   <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/23380622-5716-4dfe-acf0-31aeffcc914f" width="80%" 
         height="80%">
      <p><고객의 재구매율></p>
    </td>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/17001f6c-f68e-4fae-9f8f-00a445d76395" width="100%" height="100%">
      <p><프로모션 적용 여부에 따른 고객의 재구매율></p>
    </td>
  </tr>
  <tr>
    <td>
      <p>이커머스 평균 재구매 기간이 32.4일인 점을 참고하여 15일씩 나눠 분석한 결과 16~30일 이내가 약 20%로 재구매율이 가장 높았음</p>
    </td>
    <td>
      <p>고객의 재구매율을 높이기 위해서는 상대적으로 프로모션이 적용하는 것이 좋다는 결과</p>
    </td>
  </tr>
</table>

<br>

2. 중고상품의 충분하지 못한 공급
* 중고 상품에 대한 관심 증가
   * 마케팅 팀의 시장조사 결과, 대유행 기간 동안 인도네시아에서 15~35세의 젊은 층인 "Indonesian Young Urbans"가 헌 옷을 절약하거나 사고파는 연습을
   시작한 점에서 검색 키워드에 중고상품을 검색하는 경우가 많은 것으로 보임.
   * 중고상품을 검색한 경우가 21,22년에 644,613개 중 108,103개(16.8%)가 나오는 만큼 중고상품에 대한 관심도가 높은 편
   <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/6a9e6cc0-726d-402b-aecd-3abf276eb0b6" width="70%" height="70%">
* 사용자가 중고 검색 후 상품을 담는 경우가 전체의 11%이고, 중고를 재검색하는 경우가 전체의 63%. 이때 재검색한 경우에도 중고상품을 다시 검색하는 경우가 97%으로 나타난 것으로 보아 이는 그만큼 원하는 중고 상품이 없었기 때문이라고 판단
<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/7dfc4c8d-f52e-435b-8a7e-d48557418301" width="100%" height="100%">
       <p><중고상품 검색 후 다음 행동></p>
    </td>
    <td> 
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/3748e291-e0b5-435f-9747-963855affdb6" width="100%" height="100%">  
       <p><중고상품 검색 후 검색 키워드></p>
    </td>  
   </tr>
</table>  

* 중고상품의 경우가 전체 등록 상품(44,424개 중 17280개)의 39%임에도 불구하고, 중고 상품을 구매자는 꾸준히 증가하는 추세였지만 2022년도에 하락.

<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/fb0b28d4-dbd2-45ac-ab37-3d25dd865b26" width="60%" height="60%">
       <p><전체 구매자 수(막대), 중고상품 구매자 비율(선)></p>
    </td>
    <td> 
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/f0fd3095-0b12-466e-b68b-2c561ab0952b" width="60%" height="60%">  
       <p><등록된 상품 중 상품별 비중> </p>
    </td>  
   </tr>
</table>  
 

<br>

3. 프로모션의 개선 필요
<table>
  <tr>
    <td>
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/fb0b28d4-dbd2-45ac-ab37-3d25dd865b26" width="60%" height="60%">
       <p><월별 프로모션 사용 비율></p>
          <p>현 이커머스 플랫폼에서 프로모션을 사용하지 않는 경우가 전체 구매자의 61.7%</p>
    </td>  
   </tr>
  <tr>
 <td>
   <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/cb743429-d49e-4b59-b6e8-ec0862512c8d" width="100%" height="100%">
    <p><월별 프로모션 적용 여부에 따른 전체 경우의 수(바), 프로모션 사용률<라인)></p>
    <p>2022년 6월과 7월의 고객 프로모션 사용률 감소</p>
    <p>LIBURDONG, WEEKENDMANTAP, WEEKENDSERU 프로모션은 토요일, 일요일 전용 프로모션.</p>
    <p>2020년 ~ 2022년 기준 프로모션이 진행되지 않는 날은 없음</p>
 </td>  
</tr>
<tr>
 <td>
   <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/c24e3d6f-7b0f-4e5c-acd8-03d411a94201" width="100%" height="100%">
    <p><날짜별 프로모션 적용 여부에 따른 매출></p>
    <p>프로모션을 적용한 경우와 아닌 경우의 매출 격차가 점점 증가.</p>
    <p>매년 매출이 증가하다가 2022년 6월에서 7월까지의 가장 많은 매출 감소가 보임</p>

 </td>  
</tr>
<tr>
 <td>
   <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/f653078f-f245-48f3-bb55-71bced983562" width="100%" height="100%">
    <p><프로모션 비율별 개수></p>
    <p>프로모션 할인율은 최소 0.1%부터 최대 54.6%까지 존재</p>
    <p>평균적으로는 2.7%의 할인율 유지</p>

 </td>  
</tr>
</table> 

* 인도네시아 이커머스 플랫폼 쇼피
   * 9월 9일, 10월 10일 등과 같은 기억하기 쉬운 날짜에만 특정 상품을 파격적으로 할인하는 행사를 매달 개최함. 특정 날짜에만 프로모션을 진행하는 점이 소비자들에게 해당 날짜에는 쇼피를 이용해야 한다는 인식을 각인시킴
* 인도네시아 전자상거래 토코피디아
   * 인도네시아의 월급날이 일반적으로 월말에 있다는 점을 착안해, 월급날 기간인 월말에 인도네시아 쇼핑 기간 캠페인을 매달 개최함. 해당 할인 기간에 토코피디아의 매출은 다른 날 대비 평균 3배 증가함



          
<br>

2.4 결과  
* **액션 도출 1 _ 일회성고객**
   * 의미 있는 프로모션 제공
      * 일회성 고객들의 객단가가 가장 낮은 7월에 프로모션을 제공
         * 매년 7월 이슬람 새해가 있는 것과 일회성 고객들의 Dress-Kondangan(이슬람 전통복장)의  검색 비율이 높음을 고려하여 새해 프로모션 제공
      * 주말 프로모션 제공
         * 일, 월, 토 순으로 구매를 많이 하는 것으로 보아 주말에 구매하는 경향 파악
         * 재구매율이 높은 16~30일 이내로 다시 돌아오지 않는 경우 주말 프로모션을 제공
   * 모바일 푸시 알람 제공
      *  해당 이커머스 플랫폼의 모바일 사용자가 90%이기 때문에 이점을 활용해서 일회성 고객들에게 현 플랫폼으로 돌아올 수 있는 푸시 알람을 제공
* **액션 도출 2 _ 중고 상품**
   * 중고 상품 카테고리화
      *  검색어 키워드에 중고가 많은 것으로 보아 중고상품을 검색해야만 중고상품을 찾을 수 있는 것으로 보임. 따라서 중고상품 여부를 카테고리화하고, 그 안에 세부 카테고리별(의류,액세서리 등)로 선택 가능하도록 제공
   *  중고 상품 개수 증대
      *  소비자들의 중고상품에 대한 관심은 높지만 상품 전체 중 39%가 중고상품이므로, 그 개수를 늘려 소비자들이 현 플랫폼에서 폭넓은 선택을 할 수 있도록 개수를 증가시킴 
* **액션 도출 3 _ 프로모션**
   * 프로모션에 대한 인식 조사
      * 고객들이 프로모션을 어떻게 인식하는지, 사용하지 않는 이유에 대해 조사할 필요가 있고, 프로모션이 매일 진행되고 있음에도 불구하고 프로모션의 혜택이 고객에게 충분히 가치 있는 것으로 인식되지 않는 것으로 보임.
      * 쇼피와 토코피디아처럼 매출 증가 사례처럼 프로모션은 매출에 영향을 주는 중요한 요소이기 때문에 개선이 필요해 보임.
      * 추가로 특정 기간에만 프로모션을 진행하여 해당 날짜에는 해당 이커머스 플랫폼을 이용해야 한다는 인식을  각인시킬 필요가 있음
   * 할인율 범위 증대
      *  프로모션을 통한 금액 할인 범위는 235루피아부터 24,519루피아 이내
      *  현 이커머스 플랫폼 평균 할인율 2.7% 그러나 연말 쇼핑 시즌에는 온라인 쇼핑물 평균 할인율 약 21%
      *  타 이커머스 플랫폼과 비교했을 때 턱없이 낮은 할인율을 가지고 있기 때문에 할인율 범위를 넓힘
   * 타켓층을 선정하여 제공
      * 평균 이탈률이 가장 높은 20대 중심
      * 40,50대는 전체 고객의 5%밖에 되지 않으므로 20대를 중점으로 프로모션을 진행
      <img src="https://github.com/KIMJEONGSU/Portfolio/assets/23291338/1cb4e1e9-d8a5-4072-afb2-464a73f749e5" width="50%" height="50%">


<br>

#### 3. 한계점 및 개선사항
* 한계점
   - 구매를 하지 않은 고객에 대한 세션 정보를 알 수 없다는 점에서의 분석 한계
   - 타 이커머스의 데이터를 얻을 수 없어 정확한 데이터의 비교가 불가능
* 개선사항
   - 전체 고객의 성향이 모두 다르기 때문에 RFM, 클러스터링 등으로 고객을 세분화하지 않은 점
   - 구매전환율과 체류시간에 따른 추가 분석 필요



