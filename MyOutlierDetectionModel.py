# normalising the data since it is distance based algorithm
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

from sklearn.neighbors import NearestNeighbors

# this is actually 8 neighbors including itself -> so it is actually 7 nearest neighbors
knn = NearestNeighbors(n_neighbors=8)

#changing dataframe to 2D array
X = X.values
knn.fit(X)

"""
Idea is to find n-nearest neighbors -> then calculate mean distance of these neighbors from the point 
-> sort the mean descending in descending order -> find the top N outliers!!

LOGIC : higher the mean distance -> chances are higher for being an outlier
"""

import warnings
warnings.filterwarnings('ignore')
outlier_df = pd.DataFrame(columns = ['fingerprint','mean_distance_of_neighbors'])
for i in range(len(X)):
    dist_array = knn.kneighbors([X[i]], return_distance=True)[0][0]
    mean = dist_array.sum()/len(dist_array)
    fingerprint = y.values[i][0]
    outlier_df = outlier_df.append({'fingerprint':fingerprint,'mean':mean},ignore_index=True)
outlier_df = outlier_df.sort_values(by='mean',ascending=False)
outlier_df = outlier_df.reset_index(drop=True)
outlier_df['index'] = outlier_df.index


# use graph to find optimum value for top n outliers
import seaborn as sns
sns.relplot(data = outlier_df.iloc[:1000,:], x='index', y='mean', kind='line')


# top n outlier 
top_n_outlier = list(outlier_df['fingerprint'].head(n))
