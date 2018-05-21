import collections
import math
import pandas as pd
import random
from pandas import DataFrame

movies = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.item""", sep="|", header=None,encoding = "ISO-8859-1")
movies.columns = ["movie_id", "movie_title", "release_date", "video_release_date", "IMDb_URL", "unknown", "Action",
                      "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                      "Film_Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

genre = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.genre""", sep="|", header=None)
genre.columns=["genre","value"]

user_data = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.data""", sep="\t", header=None)
user_data.columns = ["user_id", "movie_id", "rating", "ts"]

global_user_id=0
user_combination_genre={}
sorted_genre_matrix={}
final_recommendation_genre_list=[]
first_filter_movies = pd.DataFrame()
final_recommendation_movies = pd.DataFrame(
        columns=["movie_id", "movie_title", "release_date", "video_release_date", "IMDb_URL", "unknown", "Action",
                 "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                 "Film_Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"])

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
    # print(sorted_genre_matrix)

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
    # print (final_recommendation_genre_list)

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
    temp_m1 = pd.DataFrame(
        columns=["movie_id", "movie_title", "release_date", "video_release_date", "IMDb_URL", "unknown", "Action",
                 "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                 "Film_Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"])
    list_keys = list(sorted_genre_matrix.keys())
    for i in range(0, len(list_keys)):
        # print("---------------------------------------------")
        # print(list_keys[i])
        temp = DataFrame(movies.loc[movies[list_keys[i]] == 1])
        # print(len(temp))
        frames = [temp_m1, temp]
        temp_m1 = pd.concat(frames)
    temp_m1 = temp_m1.drop_duplicates(subset=['movie_id'])
    global first_filter_movies
    first_filter_movies = temp_m1
    # print_full_df(first_filter_movies)
    print("Length of rows : %d" % (len(first_filter_movies)))

def secondary_movie_filtering():
    for i in range(0,len(final_recommendation_genre_list)):
        temp = DataFrame(first_filter_movies)
        for j in range(0,len(final_recommendation_genre_list[i])):
            temp = DataFrame(temp.loc[temp[final_recommendation_genre_list[i][j]]==1])
            if(len(temp)==0):
                break
        if(len(temp)!=0):
            recommending_movies(temp)
        # print (temp)
def print_full_df(x):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(x)


def check_if_already_saw(id):
    # print((user_data.loc[(user_data["movie_id"]==id) &(user_data["user_id"]==int (global_user_id))] ))
    return (len(user_data.loc[(user_data["movie_id"]==id) &(user_data["user_id"]==int (global_user_id))] ))!=0


def alredy_added_movie(temp):
    # print(temp)
    return not ((len(final_recommendation_movies.loc[final_recommendation_movies["movie_id"]==temp.iloc[0,0]])))!=0

def add_movie_to_dataframe(temp):
    global  final_recommendation_movies
    if len(final_recommendation_movies)==0:
        frames=[final_recommendation_movies,temp]
        final_recommendation_movies=pd.concat(frames)
        # print(len(final_recommendation_movies))
        return True
    else:
        if(alredy_added_movie(temp)):
            # print (temp)
            # print (final_recommendation_movies)
            frames = [final_recommendation_movies, temp]
            final_recommendation_movies = pd.concat(frames)
            # print((final_recommendation_movies))
        return True
    return False

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
            # print("in adding")
            # print(temp)
            flag=add_movie_to_dataframe(temp)
            # print("-----------------------------------------------------------------------Flag recomeding movies "+ str(flag))
            # print (final_recommendation_movies)
            if(flag):
                movie_counter+=1
        while_counter+=1

    # check_if_already_saw(101)
    # print(len(x))

    pass


def show_movie_names():
    if(len(final_recommendation_movies)<5):
        for i in range(0,len(final_recommendation_movies)):
            print (final_recommendation_movies.iloc[i,1])
    else:
        for i in range(0,5):
            print(final_recommendation_movies.iloc[i,1])




def main():
    global global_user_id
    global_user_id = input("Enter User ID :")
    user_data_df=user_ratings(global_user_id)
    gener_values=get_average_genre_ratings(user_data_df)
    top_genere_values(gener_values)
    calculate_recommended_genres()
    filter_movies_according_to_most_viewed_genre()
    secondary_movie_filtering()
    show_movie_names()
    print (len(final_recommendation_movies))


main()
