import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
from urllib.request import urlopen as uReq
from statistics import mean

## IMDB site link
_url = "https://www.imdb.com/search/title/?groups=top_250"
main_url = 'https://www.imdb.com'


# function to get page soup from html page
def get_page_soup(url):
    # opening connection
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    #html parser
    return soup(page_html, "html.parser")


# functon to get new url from the html page
def get_new_url_from_page(page_soup):
    
    url = page_soup.find("div", {
        "class": "desc"
    }).find("a", {"class": "lister-page-next next-page"})
    if url != None:
        url = url['href']
        url = main_url + url
    return url


class ImdbData:

    def __init__(self):
        self.movies = self.__scrap_site()
        self.numerical_features = ['year', 'rate', 'votes', 'gross', 'duration']
        self.categorical_features = ['title', 'directors', 'genre']
        self.directors = self.__create_transformed_df('directors', ['rate', 'gross', 'duration'])
        self.genre =  self.__create_transformed_df( 'genre',  ['rate','duration'])


    def __scrap_site(self):
        # create list films with films from all pages
        films = []
        url = _url
        while url is not None:
            page = get_page_soup(url)
            url = get_new_url_from_page(page)

            films_on_page = page.findAll("div", {"class": "lister-item-content"})
            films = films + films_on_page

        #Create a data frame with the movies

        headers = ['title', 'year', 'rate', 'votes', 'gross', 'directors', 'duration', 'genre']

        df = pd.DataFrame(columns=headers)

        for i, m in enumerate(films):
            row = []
            #title
            titre = films[i].h3.a.text
            row.append(titre)
            #year
            annee = films[i].h3.find("span", {
                "class": "lister-item-year text-muted unbold"
            }).text.strip('I ()')
            row.append(annee)
            ## rate
            rate = films[i].find("div", {
                "class": "inline-block ratings-imdb-rating"
            }).strong.text
            row.append(rate)
            ## votes & gross
            vote_and_recette = films[i].find("p", {
                "class": "sort-num_votes-visible"
            }).findAll('span')
            if len(vote_and_recette) < 4:
                row.append(vote_and_recette[1]['data-value'])
                row.append(None)
            else:
                row.append(vote_and_recette[1]['data-value'])
                row.append(vote_and_recette[4]['data-value'].replace(',', ''))
            ## director
            realisateur = films[i].find("p", {
                "class": ""
            }).text.strip().split(':\n')[1].replace(', ', '').split('\n')[:-2]
            row.append(realisateur)
            ## duration
            durée = films[i].find("span", {"class": "runtime"}).text.strip(' min')
            row.append(durée)
            ## genre
            genre = films[i].find("span", {
                "class": "genre"
            }).text.strip(" ").strip('\n').split(', ')
            row.append(genre)
            length = len(df)
            df.loc[length] = row

            for f in ['year', 'rate', 'votes', 'gross', 'duration']:
                df[f] = df[f].astype('float')
            df['year'] = df['year'].astype('int')

        return df

    def export_to_csv(self):
        self.df.to_csv('imdb-top250.csv', index = False) 
        return


    ## Function to create new data frame

    def __create_transformed_df(self, elem_list, features_list):
        """elem_list should be in type list"""
        old_df = self.movies

        new_dict = {}
        for index, elems in zip(old_df.index, old_df[elem_list]):
            for elem in elems:
                if elem in new_dict.keys():
                    for j, feature in enumerate(features_list):
                        new_dict[elem][j].append(float(old_df.loc[index, feature]))
                else:
                    new_dict[elem] = [[] for i in range(len(features_list))]
                    for j, feature in enumerate(features_list):
                        new_dict[elem][j].append(float(old_df.loc[index, feature]))

        headers = [elem_list]
        for i in features_list:
            headers.append(f'avg_movie_{i}')
        headers.append('number_of_movies')  ##? how to name?

        new_df = pd.DataFrame(columns=headers)

        for key in new_dict:
            row = []
            row.append(key)
            for i, col in enumerate(headers[1:-1]):
                mean_val = mean(new_dict[key][i])
                row.append(mean_val)
            num = len(new_dict[key][0])
            row.append(num)

            length = len(new_df)
            new_df.loc[length] = row

        return new_df



