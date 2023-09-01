import requests
import csv
from keys import api_key as API_KEY


def read_csv():
    movie_data_list = []
    with open("oscar_winners.csv") as csvfile:
        data = csv.reader(csvfile)
        # skip header line
        next(data)
        for row in data:
            # call api function for each movie append to list
            movie_data = get_movie_data(row)
            movie_data_list.append(movie_data)
    # send all movies data list for cleaning
    clean_for_csv(movie_data_list)


def get_movie_data(row):
    # call api and return the data of single movie
    res = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&i={row[1]}")
    return res.json()


def clean_for_csv(movies):
    data_for_csv = []
    for movie in movies:
        movie_list = []
        runtime = int(''.join(i for i in movie["Runtime"] if i.isdigit()))
        awards = movie["Awards"].split(". ")
        wins_and_nomnoms = awards[1].split(" & ")
        wins = int(''.join(i for i in wins_and_nomnoms[0] if i.isdigit()))
        nom_noms = int(''.join(i for i in wins_and_nomnoms[1] if i.isdigit()))
        box_office = int(''.join(i for i in movie["BoxOffice"] if i.isdigit()))
        movie_list.extend(
            (movie["Title"], runtime, movie["Genre"], wins, nom_noms, box_office))
        data_for_csv.append(movie_list)
    create_csv(data_for_csv)


def create_csv(movies):
    header = ["title", "runtime", "genre",
              "award_wins", "award_nominations", "box_office"]
    with open("movies.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for movie in movies:
            writer.writerow(movie)


if __name__ == "__main__":
    read_csv()
