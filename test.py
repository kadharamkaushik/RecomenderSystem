import collections
import math
import operator

import pandas as pd
from pandas import DataFrame
# import collections

movies = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.item""", sep="|", header=None,encoding = "ISO-8859-1")
movies.columns = ["movie_id", "movie_title", "release_date", "video_release_date", "IMDb_URL", "unknown", "Action",
                      "Adventure", "Animation", "Childrens", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                      "Film_Noir", "Horror", "Musical", "Mystery", "Romance", "Sci_Fi", "Thriller", "War", "Western"]

genre = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.genre""", sep="|", header=None)
genre.columns=["genre","value"]

user_data = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.data""", sep="\t", header=None)
user_data.columns = ["user_id", "movie_id", "rating", "ts"]

user_combination_genre={}
sorted_genre_matrix={}
final_recommendation_genre_list=[]

# Creatng each movie rating accordignt to genre and finding the user's combinations in genre
def create_genre_combination(df):
    gener_matrix = []
    k=[]
    for i in range(len(df.index)):
        movie_df = movies.loc[movies["movie_id"] == df.iat[i, 1]]
        temp_ls = []
        temp_combi_genre=[]
        for j in range(5, len(movies.columns)):
            temp_ls.append((movie_df.iat[0, j])*(df.iat[i, 2]))
            if(movie_df.iat[0, j]==1):
                temp_combi_genre.append(genre.iat[j-5,0])
        gener_matrix.append(temp_ls)
        if (tuple(temp_combi_genre) not in user_combination_genre.keys()):
            user_combination_genre[tuple(temp_combi_genre)] = 1
        else:
            user_combination_genre[tuple(temp_combi_genre)]+=1
    # user_combination_genre=set(tuple(i) for i in k)
    # user_combination_genre=k
    # print(user_combination_genre)
    return gener_matrix

# Ratings of Each Genre depending on the user rating
def get_average_genre_ratings(d):
    df = DataFrame(d)
    gener_matrix =create_genre_combination(df)
    gener_main=[]
    for i in range (len(gener_matrix[0])):
        sum=0
        for j in range (len(gener_matrix)):
            sum +=gener_matrix[j][i]
        gener_main.append((int)((sum/len(gener_matrix)*5)))
    # print(gener_main)
    return gener_main

# Top Genre dict
def top_genere_values(gener_values):

    avg=sum(gener_values)/len(gener_values)
    # ls={}
    for i in range(len(gener_values)):
        if(gener_values[i]>=avg):
            sorted_genre_matrix[genre.iat[i,0]]=gener_values[i]
    # print (ls)
    # sorted_genre_matrix = sorted(ls.items(), key=operator.itemgetter(1))
    print(sorted_genre_matrix)

# Creating Specific User above avg ratings data
def user_ratings(user_id):
    user_id_data = user_data.loc[user_data['user_id'] == int (user_id)]
    user_id_df = DataFrame(user_id_data.loc[user_id_data['rating'] >= 3])
    return user_id_df

#calculate recommended genre combinations
def find_accurate_recomendation_genre(combination_genres_sorted_list):
    sum=0
    items = list(combination_genres_sorted_list.items())
    for i in range(0,len(items)):
        # print(items[i])
        sum+=items[i][1]
    avg = math.ceil (sum/len(combination_genres_sorted_list))
    # main_ls=[]
    for i in range(0,len(items)):
        if(items[i][1]>=avg):
            final_recommendation_genre_list.append(items[i][0])


#Calculating recommended Genre Lists
def calculate_recommended_genres():
    temp_dict=user_combination_genre
    for i in temp_dict.keys():
        sum=0
        for j in range(0,len(i)):
            if(i[j] in sorted_genre_matrix):
                sum+=sorted_genre_matrix[i[j]]*user_combination_genre[i]
        temp_dict[i]=sum
    temp_dict=sorted(temp_dict.items(),key=lambda x : x[1],reverse=True)
    combination_genres_sorted_list = collections.OrderedDict(temp_dict)
    # print(combination_genres_sorted_list)
    find_accurate_recomendation_genre(combination_genres_sorted_list)

#input : nothing, output : movie dict , all movies with the sorted_genre_matrix
def filter_movies_according_to_most_viewed_genre():





def main():
    user = input("Enter User ID :")
    user_data_df=user_ratings(user)
    gener_values=get_average_genre_ratings(user_data_df)
    top_genere_values(gener_values)
    calculate_recommended_genres()
    filter_movies_according_to_most_viewed_genre()


main()
