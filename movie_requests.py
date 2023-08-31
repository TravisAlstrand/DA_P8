import requests, csv
from keys import api_key as API_KEY


def read_csv():
  movie_data_list = []
  with open("oscar_winners.csv") as csvfile:
    data = csv.reader(csvfile)
    # skip header line
    next(data)
    for row in data:
      movie_data = get_movie_data(row)
      movie_data_list.append(movie_data)
  clean_for_csv(movie_data_list)


def get_movie_data(row):
  res = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&i={row[1]}")
  return res.json()


def clean_for_csv(movies):
  data_for_csv = []
  for movie in movies:
    movie_list = []
    runtime = int(''.join(i for i in movie["Runtime"] if i.isdigit()))
    awards = movie["Awards"].split(". ")
    wins_and_losses = awards[1].split(" & ")
    wins = int(''.join(i for i in wins_and_losses[0] if i.isdigit()))
    losses = int(''.join(i for i in wins_and_losses[1] if i.isdigit()))
    box_office = int(''.join(i for i in movie["BoxOffice"] if i.isdigit()))
    movie_list.append(movie["Title"])
    movie_list.append(runtime)
    movie_list.append(movie["Genre"])
    movie_list.append(wins)
    movie_list.append(losses)
    movie_list.append(box_office)
    data_for_csv.append(movie_list)
  create_csv(data_for_csv)


def create_csv(movies):
  print(movies)
    


if __name__ == "__main__":
  read_csv()
