import collections
import math
import pandas as pd
import random
from pandas import DataFrame
import time

movies = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.item""", sep="|", header=None,encoding = "ISO-8859-1")
movies.columns = ["movie_id", "movie_title", "release_date", "video_release_date", "IMDb_URL", "unknown", "Action",
                      "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                      "Film_Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

genre = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.genre""", sep="|", header=None)
genre.columns=["genre","value"]

user_data = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.data""", sep="\t", header=None)
user_data.columns = ["user_id", "movie_id", "rating", "ts"]

global_int_user_id=0
user_combination_genre={}
sorted_genre_matrix={}
final_recommendation_genre_list=[]
first_filter_movies = pd.DataFrame()
final_recommendation_movies = pd.DataFrame(
        columns=["movie_id", "movie_title", "release_date", "video_release_date", "IMDb_URL", "unknown", "Action",
                 "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                 "Film_Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"])

# Creating a list of ratings from a specific user with ratings more than avg. rating
# Input : userId as int
# Output : DataFrame consisting of ratings for the input userId with more than the avg rating
def user_ratings(user_id):
    df_user_data = user_data.loc[(user_data['user_id'] == int (user_id)) & (user_data['rating']>=3)]
    print("USER RATINGS - Total number of ratings under consideration :"+str(len(df_user_data)))
    return df_user_data

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
    return gener_matrix

# Ratings of Each Genre depending on the user rating
def get_average_genre_ratings(d):
    df = DataFrame(d)
    list_gener_matrix =create_genre_combination(df)
    gener_main=[]
    for i in range (len(list_gener_matrix[0])):
        sum=0
        for j in range (len(list_gener_matrix)):
            sum +=list_gener_matrix[j][i]
        gener_main.append((int)((sum/len(list_gener_matrix)*5)))
    return gener_main

# Top Genre dict
def top_genere_values(gener_values):

    avg=sum(gener_values)/len(gener_values)
    for i in range(len(gener_values)):
        if(gener_values[i]>=avg):
            sorted_genre_matrix[genre.iat[i,0]]=gener_values[i]
    print("Genres Watched Regularly : "+str(sorted_genre_matrix))

#calculate recommended genre combinations
def find_accurate_recomendation_genre(combination_genres_sorted_list):
    sum=0
    items = list(combination_genres_sorted_list.items())
    for i in range(0,len(items)):
        sum+=items[i][1]
    avg = math.ceil (sum/len(combination_genres_sorted_list))
    for i in range(0,len(items)):
        if(items[i][1]>=avg):
            final_recommendation_genre_list.append(items[i][0])
    print ("Combination of genres that can be recommended :"+ str (final_recommendation_genre_list))

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
    find_accurate_recomendation_genre(combination_genres_sorted_list)

#input : nothing, output : movie dict , all movies with the sorted_genre_matrix
def filter_movies_according_to_most_viewed_genre():
    temp_m1 = pd.DataFrame(
        columns=["movie_id", "movie_title", "release_date", "video_release_date", "IMDb_URL", "unknown", "Action",
                 "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                 "Film_Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"])
    list_keys = list(sorted_genre_matrix.keys())
    for i in range(0, len(list_keys)):
        temp = DataFrame(movies.loc[movies[list_keys[i]] == 1])
        frames = [temp_m1, temp]
        temp_m1 = pd.concat(frames)
    temp_m1 = temp_m1.drop_duplicates(subset=['movie_id'])
    global first_filter_movies
    first_filter_movies = temp_m1
    # print("Number of Movies that can be recommended: %d" % (len(first_filter_movies)))

#input : nothing, output : movie dict , all movies which are to be recommended to the user
def secondary_movie_filtering():
    for i in range(0,len(final_recommendation_genre_list)):
        temp = DataFrame(first_filter_movies)
        for j in range(0,len(final_recommendation_genre_list[i])):
            temp = DataFrame(temp.loc[temp[final_recommendation_genre_list[i][j]]==1])
            if(len(temp)==0):
                break
        if(len(temp)!=0):
            recommending_movies(temp)

def print_full_df(x):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(x)

#input : movie id, output : boolean value based on whether the movie has been watched or not
def check_if_already_saw(id):
    return (len(user_data.loc[(user_data["movie_id"]==id) &(user_data["user_id"]==int (global_int_user_id))] ))!=0

#input : dataframe, output : boolean value based on whether the movie has been added to the final list or not
def alredy_added_movie(temp):
    return not ((len(final_recommendation_movies.loc[final_recommendation_movies["movie_id"]==temp.iloc[0,0]])))!=0

#input : dataframe, output : movie dict , final movie recomendation list
def add_movie_to_dataframe(temp):
    global  final_recommendation_movies
    if len(final_recommendation_movies)==0:
        frames=[final_recommendation_movies,temp]
        final_recommendation_movies=pd.concat(frames)
        return True
    else:
        if(alredy_added_movie(temp)):
            frames = [final_recommendation_movies, temp]
            final_recommendation_movies = pd.concat(frames)
        return True
    return False

#input : dataframe, output : picking up random movies from each genre and preparing a list of 5 movies to be recommended to the user.
def recommending_movies(x):
    while_counter=0
    movie_counter=0
    while(True):
        if(while_counter==len(x) or movie_counter==2):
            return
        rand = random.randint(0,len(x)-1)
        temp=(x.iloc[rand,0])
        temp=movies.loc[(movies['movie_id']==temp)]
        if(not check_if_already_saw(temp.iloc[0,0])):
            flag=add_movie_to_dataframe(temp)
            if(flag):
                movie_counter+=1
        while_counter+=1

#display the final list of recommended movies to the user
def show_movie_names():
    print("RECOMMENDED MOVIES")
    if(len(final_recommendation_movies)<5):
        for i in range(0,len(final_recommendation_movies)):
            print (final_recommendation_movies.iloc[i,1])
    else:
        for i in range(0,5):
            print(final_recommendation_movies.iloc[i,1])

#main method invoking all the other user defined functions
def main():

    global global_int_user_id
    global_int_user_id = input("Enter User ID :")
    time_start = time.time()
    df_user_data=user_ratings(global_int_user_id)
    list_avg_gener_values=get_average_genre_ratings(df_user_data)
    top_genere_values(list_avg_gener_values)
    calculate_recommended_genres()
    filter_movies_according_to_most_viewed_genre()
    secondary_movie_filtering()
    show_movie_names()
    print ("Total number of movies that can be recommended after filtering :"+ str(len(final_recommendation_movies)))
    time_end = time.time()
    print ("Execution Time :"+ str(time_end-time_start))

main()
