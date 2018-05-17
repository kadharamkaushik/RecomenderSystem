import operator

import pandas as pd
from pandas import DataFrame

movies = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.item""", sep="|", header=None,encoding = "ISO-8859-1")
movies.columns = ["movie_id", "movie_title", "release_date", "video_release_date", "IMDb_URL", "unknown", "Action",
                      "Adventure", "Animation", "Childrens", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                      "Film_Noir", "Horror", "Musical", "Mystery", "Romance", "Sci_Fi", "Thriller", "War", "Western"]

genre = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.genre""", sep="|", header=None)
genre.columns=["genre","value"]

user_data = pd.read_csv(r"""D:\Kaushik\PycharmProjects\untitled\data\u.data""", sep="\t", header=None)
user_data.columns = ["user_id", "movie_id", "rating", "ts"]

user_combination_genre={}
sorted_genre_matrix=[]

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
    print(user_combination_genre)
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
    print(gener_main)
    return gener_main

# Top Genre dict
def top_genere_values(gener_values):

    avg=sum(gener_values)/len(gener_values)
    ls={}
    for i in range(len(gener_values)):
        if(gener_values[i]>=avg):
            ls[genre.iat[i,0]]=gener_values[i]
    sorted_genre_matrix = sorted(ls.items(), key=operator.itemgetter(1))

# Creating Specific User above avg ratings data
def user_ratings(user_id):
    user_id_data = user_data.loc[user_data['user_id'] == int (user_id)]
    user_id_df = DataFrame(user_id_data.loc[user_id_data['rating'] >= 3])
    return user_id_df

def main():
    user = input("Enter User ID :")
    user_data_df=user_ratings(user)
    gener_values=get_average_genre_ratings(user_data_df)
    top_genere_values(gener_values)


main()
