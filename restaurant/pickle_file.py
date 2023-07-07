import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from time import sleep, time
import numpy as np
from konlpy.tag import Okt
from tqdm import tqdm
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import psycopg2
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import re
from collections import namedtuple


conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="1234")

cur = conn.cursor()
cur.execute("select * from last_data")
rows = cur.fetchall()

meta = pd.DataFrame(rows, columns=[i[0] for i in cur.description])

#텍스트의 정규식 적용(숫자, 영어 제거)
meta['kakao_blog_review_txt'] = meta['kakao_blog_review_txt'] .apply (lambda x: re.sub(r'[a-zA-Z0-9]+', '', x)) 

#형태소 분석
okt = Okt()
data_okt = []
for sentence in tqdm(meta['kakao_blog_review_txt']):
    temp_X = []
    temp_X = okt.morphs(sentence, stem=True)
    data_okt.append(temp_X)


#불용어 제거
stopwords = ['하다','이','도','에','너무','요','은','는','가','을','를','그리고','그러나','하지만','있다','없다','아','휴','아이구','아이쿠','아이고',
            '어','나','우리','저희','따라','의해','에','의','가','으로','로','에게','뿐이다','의거하여','근거하여','입각하여','기준으로',
            '예하면','예를 들면','예를 들자면','저','소인','소생','저희','지말고','하지마','하지마라','다른','물론','또한','그리고','비길수 없다',
            '해서는 안된다','불가능하다','무엇','어느','어떤','아래윗','조차','한데','그럼에도 불구하고','여전히','심지어','까지도','조차도',
            '하지 않는다면','않으면','만 못하다','하는 편이 낫다','불완전하다','투자한다','생각한다','입니다','요','ㅎ','ㅎㅎ','ㅎㅎㅎ','ㅠ','ㅠㅠ',
            'ㅠㅠㅠ','ㅜ','ㅜㅜ','ㅜㅜㅜ','네','때','에는','가','각','것','ㅏ','서울','오빠','된','월요일','내','20230315','언','슈','인','다','랍니','한','제','이다','들','여','아보',
        '점','서울특별시','동작구','ㅋㅋ','답','게','이에요','시','수','ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ','션','월','일','김','얌','습','ᵒ','ㅋㅋㅋㅋㅋㅋㅋ','ㅠㅠㅜ','ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ',
        'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ','��ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ','ㅋㅋㅋㅋㅋㅋㅋㅋ','ㅋㅋㅋㅋㅋㅋ','_','랑','ㅋㅋㅋㅋㅋㅋㅋㅋㅋ','ㅋㅋㅎ']
data_okt_clean = []
for sentence in data_okt:
    temp_X = [word for word in sentence if not word in stopwords]     
    data_okt_clean.append(temp_X)




# doc2vec 모델
doc_vectorizer = Doc2Vec(dm=1, vector_size=300, window=5, alpha=0.025, min_alpha=0.025, seed=1234)


agg = meta[['name', 'middle_category', 'kakao_blog_review_txt']]
breakpoint()
TaggedDocument = namedtuple('TaggedDocument', 'words tags')
breakpoint()
tagged_train_docs = [TaggedDocument((c), [d]) for d, c in agg[['name', 'kakao_blog_review_txt']].values]
breakpoint()

doc_vectorizer.build_vocab(tagged_train_docs)
breakpoint()
print(str(doc_vectorizer))

# 벡터 문서 학습


start = time()

for epoch in tqdm(range(5)):
    doc_vectorizer.train(tagged_train_docs, total_examples=doc_vectorizer.corpus_count, epochs=doc_vectorizer.epochs)
    doc_vectorizer.alpha -= 0.002 # decrease the learning rate
    doc_vectorizer.min_alpha = doc_vectorizer.alpha # fix the learning rate, no decay

#doc_vectorizer.train(tagged_train_docs, total_examples=doc_vectorizer.corpus_count, epochs=doc_vectorizer.iter)


result = doc_vectorizer.dv.most_similar('슬로우캘리', topn=5)
print(result)

model_filename = "doc2vec_model.pkl"

# 모델 객체를 피클링
with open(model_filename, "wb") as f:
    pickle.dump(doc_vectorizer, f)
#------------------------------------------------------------------------
# df = pd.read_csv('last_data.csv',index_col=0)

# # 형태소분석
# okt = Okt()
# data_okt = []



# for sentence in tqdm(df['kakao_blog_review_txt']):
#     temp_X = []
#     temp_X = okt.morphs(sentence, stem=True)
#     data_okt.append(temp_X)
    
# #불용어 제거
# stopwords = ['하다','이','도','에','너무','요','은','는','가','을','를','그리고',
#             '그러나','하지만','있다','없다','아','휴','아이구','아이쿠','아이고',
#              '어','나','우리','저희','따라','의해','에','의','가','으로',
#              '로','에게','뿐이다','의거하여','근거하여','입각하여','기준으로',
#              '예하면','예를 들면','예를 들자면','저','소인','소생','저희','지말고',
#              '하지마','하지마라','다른','물론','또한','그리고','비길수 없다',
#              '해서는 안된다','불가능하다','무엇','어느','어떤','아래윗','조차',
#              '한데','그럼에도 불구하고','여전히','심지어','까지도','조차도',
#              '하지 않는다면','않으면','만 못하다','하는 편이 낫다','불완전하다',
#              '투자한다','생각한다','입니다','요','ㅎ','ㅎㅎ','ㅎㅎㅎ','ㅠ','ㅠㅠ',
#              'ㅠㅠㅠ','ㅜ','ㅜㅜ','ㅜㅜㅜ','네','때','에는','가','각','것','ㅏ','서울','오빠','된','월요일',
#             '내','20230315','언','슈','인','6','다','랍니','한','제','이다','들','여','아보',
#             '점','서울특별시','동작구','ㅋㅋ','답','게','이에요','시','수','']
# # chatGPT에서 검색하여 나온 불용어와 문맥적으로 큰 의미가 없는 단어들을 불용어 사전으로 만듬.

# data_okt_clean = []
# for sentence in data_okt:
#     temp_X = [word for word in sentence if not word in stopwords]     
#     data_okt_clean.append(temp_X)


# def find_simi_place(df,place_name, top_n):
    

#     df['cate_mix'] = df['category2'] +  df['category3']
#     df['cate_mix'] = df['cate_mix'].str.replace("/", " ")

#     # 카테고리 벡터화
#     vect_category = CountVectorizer(ngram_range=(1,2))
#     place_category = vect_category.fit_transform(df['cate_mix']) 
#     # 카테고리간 코사인 유사도
#     place_simi_cate = cosine_similarity(place_category, place_category).argsort()[:, ::-1]

#     # 텍스트 벡터화
#     vect_review = CountVectorizer(ngram_range=(1,2))
#     place_review = vect_review.fit_transform(df['kakao_blog_review_txt']) 

#     # 리뷰 텍스트 간의 코사인 유사도
#     place_simi_review = cosine_similarity(place_review, place_review).argsort()[:, ::-1]
    
#     place_simi_co = (
#                  + place_simi_cate * 1 # 공식 1. 카테고리 유사도
#                  + place_simi_review * 0.7 # 공식 2. 리뷰 텍스트 유사도
#                  + np.repeat([df['kakao_blog_review_qty'].values], len(df['kakao_blog_review_qty']) , axis=0) * 0.001  # 공식 3. 블로그 리뷰가 얼마나 많이 올라왔는지
#                  + np.repeat([df['kakao_star_point'].values], len(df['kakao_star_point']) , axis=0) * 0.005            # 공식 4. 블로그 별점이 얼마나 높은지
#                  + np.repeat([df['kakao_star_point_qty'].values], len(df['kakao_star_point_qty']) , axis=0) * 0.001    # 공식 5. 블로그 별점 평가가 얼마나 많이 됐는지
#                  )



#     # 아래 place_simi_co_sorted_ind 는 그냥 바로 사용하면 됩니다.
#     sorted_ind = place_simi_co.argsort()[:, ::-1] 
    
#     compare = 0
#     index = 0
    
#     contains_name = df[df['name'].str.contains(place_name)]
#     contains_name = contains_name.iloc[0:1]
    
#     if contains_name.empty:
#         print('DataFrame is empty!\nSearch blog review..')
#         contains_name = df[df['kakao_blog_review_txt'].str.contains(place_name)]
        
#         for i in range(len(contains_name['kakao_blog_review_txt'])):
#             if contains_name['kakao_blog_review_txt'].iloc[i].count(place_name) > compare:
#                 compare = contains_name['kakao_blog_review_txt'].iloc[i].count(place_name)
#                 index = i
#         contains_name = contains_name.iloc[index:index+1]
        
#         if contains_name.empty:
#             print('No Data')
            
#     place_index = contains_name.index.values
#     similar_indexes = sorted_ind[place_index, :(top_n)]
#     similar_indexes = similar_indexes.reshape(-1)
    
#     return df.iloc[similar_indexes]

# result = find_simi_place(df,'냉면',5)
# for i in result:
#     print(i)
