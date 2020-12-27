import pandas as pd
import numpy as np
books_df = pd.read_csv('books.csv',usecols=['book_id','title'],dtype={'book_id': 'int64', 'title': 'str'})
rating_df=pd.read_csv('ratings.csv',usecols=['user_id', 'book_id', 'rating'],
    dtype={'user_id': 'int64', 'book_id': 'int64', 'rating': 'float32'})
df = pd.merge(rating_df,books_df,on='book_id')
combine_book_rating = df.dropna(axis = 0, subset = ['title'])
book_ratingCount = (combine_book_rating.groupby(by = ['title'])['rating'].count().reset_index().rename(columns = {'rating': 'totalRatingCount'})[['title', 'totalRatingCount']])
rating_with_totalRatingCount = combine_book_rating.merge(book_ratingCount, left_on = 'title', right_on = 'title', how = 'left')
pd.set_option('display.float_format', lambda x: '%.3f' % x)
popularity_threshold = 50
rating_popular_book= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')

book_features_df=rating_popular_book.pivot_table(index='title',columns='user_id',values='rating').fillna(0)
from scipy.sparse import csr_matrix

book_features_df_matrix = csr_matrix(book_features_df.values)

from sklearn.neighbors import NearestNeighbors


model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(book_features_df_matrix)

helo=book_features_df.iloc[:, 0]
#helo.to_csv('book_name.csv')
hel=pd.read_csv('book_name.csv')
hel.insert(0, 'id', hel.index)
nam=hel.drop(hel.columns[2], axis=1)
#nam.to_csv('book_name_final.csv')
nam1=pd.read_csv('book_name_final.csv')

def combine(bookname):

    query_index = nam1[nam1['title']==str(bookname)].index.values
    distances, indices = model_knn.kneighbors(book_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)
    lst = []
    for i in range(0, len(distances.flatten())):
        
        if i == 0:
            lst.append('Recommendations for {0}: '.format(book_features_df.index[query_index[0]]))
        else:
            lst.append('{0}: {1}'.format(i, book_features_df.index[indices.flatten()[i]]))
    return lst


