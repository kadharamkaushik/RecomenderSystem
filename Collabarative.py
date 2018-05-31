import ContentBased as CB
import numpy as np
import time
time_start = time.time()
mean = CB.user_data.groupby(['user_id'],as_index=False,sort=False).mean().rename(columns={'rating':'rating_mean'})[['user_id','rating_mean']]
CB.user_data = CB.pd.merge(CB.user_data,mean,on='user_id',how='left',sort=False)
CB.user_data['rating_adjusted']=CB.user_data['rating']-CB.user_data['rating_mean']
distinct_users = np.unique(CB.user_data['user_id'])
user_data_append = CB.pd.DataFrame()
user_data_all = CB.pd.DataFrame()

print (CB.global_int_user_id)
user1_data = CB.user_data[(CB.user_data['user_id']==int (CB.global_int_user_id))]
user1_mean = user1_data['rating'].mean()
user1_data = user1_data.rename(columns={'user_id':'user_id1'})
user1_data = user1_data.rename(columns={'rating_adjusted':'rating_adjusted1'})
user1_val = np.sqrt(np.sum(np.square(user1_data['rating_adjusted1']),axis=0))
# print(user1_data)
i=1
distinct_movie = np.unique(CB.user_data['movie_id'])

for movie in distinct_movie:
    item_user = CB.user_data[(CB.user_data['movie_id']== int (movie))]
    distinct_users1=np.unique(item_user['user_id'])
    j=1
    for user2 in distinct_users1:
        if j% 200 == 0:
            print (j,"out of",len(distinct_users1), i , "out of", len(distinct_movie))
        user2_data = CB.user_data[(CB.user_data['user_id']==user2)]
        user2_mean = user2_data['rating'].mean()
        user2_data = user2_data.rename(columns={'user_id':'user_id2'})
        user2_data = user2_data.rename(columns={'rating_adjusted': 'rating_adjusted2'})
        user2_val = np.sqrt(np.sum(np.square(user2_data['rating_adjusted2']), axis=0))
        user_data = CB.pd.merge(user1_data,user2_data[['rating_adjusted2','movie_id','user_id2']],on='movie_id',how='inner',sort=False)
        user_data['vector_product'] = (user_data['rating_adjusted1']*user_data['rating_adjusted2'])
        user_data = user_data.groupby(['user_id1','user_id2'],as_index=False,sort=False).sum()
        user_data['dot'] = user_data['vector_product'] / (user1_val*user2_val)
        user_data_all = user_data_all.append(user_data,ignore_index=True)
        j =j + 1
    # print (len(user_data_all),"---------------------------------------")
    user_data_all = user_data_all[(user_data_all['dot']<1) & (user_data_all['dot']>(-1))]
    user_data_all = user_data_all.sort_values(['dot'],ascending=False)
    user_data_all = user_data_all.head(30)
    # print(user_data_all)
    # print("------------------------------------------")
    user_data_all['movie_id'] = movie
    user_data_append = user_data_append.append(user_data_all,ignore_index=True)
    # print(user_data_all)
    # print (len(user_data_all),"+++++++++++++++++++++++++++++++++++++++")
    i=i+1
User_dot_adj_rating_all = CB.pd.DataFrame()
distinct_movie = np.unique(CB.user_data['movie_id'])
j = 1
for movie in distinct_movie:
    user_data_append_movie= user_data_append[user_data_append['movie_id'] == movie]
    User_dot_adj_rating = CB.pd.merge(CB.user_data,user_data_append_movie[['dot','user_id2','user_id1']],how='inner',left_on='user_id',right_on='user_id2',sort='False')
    if j % 200 == 0 :
        print (j,"out of" , len(distinct_movie))
    User_dot_adj_rating1 = User_dot_adj_rating[User_dot_adj_rating['movie_id'] == movie]
    if len(np.unique(User_dot_adj_rating1['user_id'])) >=1 :
        User_dot_adj_rating1['rating'] = User_dot_adj_rating1['dot']*User_dot_adj_rating1['rating_adjusted']
        User_dot_adj_rating1['dot_abs'] = User_dot_adj_rating1['dot'].abs()
        User_dot_adj_rating1 = User_dot_adj_rating1.groupby(['user_id1'],as_index=False,sort=False).sum()[['user_id1','rating','dot_abs']]
        User_dot_adj_rating1['Rating'] = int((User_dot_adj_rating1['rating'] / User_dot_adj_rating1['dot_abs']) + user1_mean)
        User_dot_adj_rating1['movie_id'] = movie
        User_dot_adj_rating1 = User_dot_adj_rating1.drop(['rating','dot_abs'],axis=1)
        User_dot_adj_rating_all = User_dot_adj_rating_all.append(User_dot_adj_rating1,ignore_index=True)
    j = j+1
User_dot_adj_rating_all = User_dot_adj_rating_all.sort_values(['Rating'],ascending=False)
print ( User_dot_adj_rating_all)

s1 = CB.pd.merge(CB.final_recommendation_movies, User_dot_adj_rating_all, how='inner', on=['movie_id'])
for i in range(len(s1)):
    print (s1.iloc[i,1])
# print (user_data_append)
time_end = time.time()
print("Execution Time :" + str(time_end - time_start))

    # print(user_data_all)





# print(CB.user_data)

