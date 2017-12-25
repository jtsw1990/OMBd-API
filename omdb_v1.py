# File: omdb_v1.py

import sys
import requests
import json
import numpy as np
import pandas as pd

domain = 'http://www.omdbapi.com/?apikey='
query = '&i='
code = 'tt'

print('Welcome to the omdb.py, this program will extract a subset')
print('of films based on the ID numbers')

sys.stdout.write('Please enter your API key: ')
sys.stdout.flush()


while True:
    api_key = input()
    if requests.get(domain + str(api_key) + query + 'tt0000001').json()['Response'] == 'False':
        sys.stdout.write('Invalid API key. Please re-enter your API key: ')
        sys.stdout.flush()
        continue
    else:
        sys.stdout.write('Successfully connected to the omdb server. Please enter the ID of \n')
        sys.stdout.write('the film you want to start with in the integer format XXXXXXX: ')
        sys.stdout.flush()
        break


while True:
    start_id = input()
    try:
        int(start_id)
    except ValueError:
        sys.stdout.write('Please re-enter a valid ID number as a 7-digit integer: ')
        sys.stdout.flush()
        continue

    else:
        if len(start_id) != 7:

            sys.stdout.write('Please re-enter a valid 7-digit ID: ')
            sys.stdout.flush()
            continue

        else:

            sys.stdout.write('Start ID selected is %s \n' % start_id)
            sys.stdout.write('Please select the number of films to be extracted as an integer value: ')
            sys.stdout.flush()
            break


len_id = int(input())
total_list = []
throw_away = []
series_list = []
id_collected = []


def gen_id(start_id, len_id):

    for num in range(len_id):

        imdb_ord = int(start_id) + num
        imdb_id = code + str(imdb_ord)
        id_collected.append(imdb_id)

    return id_collected


id_collected = gen_id(start_id, len_id)


def get_series(api_key):

    for series in id_collected:

        url = domain + api_key + query + series
        data_dict = dict(requests.get(url).json())
        total_list.append(data_dict)

    return total_list


total_list = get_series(api_key)


sys.stdout.write('You have selected ID %s to %s \n' % (id_collected[0],id_collected[len(id_collected)-1]))
sys.stdout.write('Please select the country of the movie: ')
sys.stdout.flush()
country = input()

def get_sublists(country):

    resp_check = [film for film in total_list if film['Response'] == 'True']
    chosen_list = {film['Title']:film['imdbRating'] for film in resp_check if film['Country'] == country}

    return chosen_list


final = pd.DataFrame(get_sublists(country), index=[0]).unstack().reset_index()
final = final.drop('level_1', axis=1)
columns = ['Title', 'ImdbRating']
final.columns = columns
print(final.replace('N/A', np.nan).dropna(how='any'))
