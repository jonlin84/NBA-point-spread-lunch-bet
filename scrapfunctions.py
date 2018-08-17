
import time
import requests
from bs4 import BeautifulSoup


#returns basketball-refrence.com/teams/{teamname}/{year}_games.html
def box_score_url_creator(team:str,year:str,baseurl:str)->list:
    return [baseurl + '/teams/' + team + '/' + year + '_games.html']


#returns big dictionary of teams:{'year'{year:[html]}}
#team name, 'year' dictornary with year# key and list of string value
#example {'HOU':{'year':{1994:[www.worldchampions.com]}}}
def url_list_generator(teams:list,years:list):
    biglist = {}
    baseurl = 'https://www.basketball-reference.com'
    for team in teams:
        biglist[team] = {}
        biglist[team]['year'] = {}
        for year in years:
            biglist[team]['year'][int(year)] = box_score_url_creator(team,year,baseurl)
    return biglist

#taking big list and making containers
def soup_maker(dct:dict):
    boxscores = {}
    for team in dct.getkeys():
        boxscores[team] = {}
        for year in dct[team]['year'].getkeys():
            boxscores[team]['year'] = {}
            url = dct[team]['year'][year][0]
            r = requests.get(url)
            soup = BeautifulSoup(r.content,'html.parser')
            boxscores[team]['year'][int(year)] = get_box_score_url(soup)
            time.sleep(3)

#returns a list of urls extensions to boxscores from a team for a particular year
#soup should be the parsed content from a team/year's url
def get_box_score_url(soup):
    container = []
    for link in soup.find_all('a'):
        k = str(link.get('href'))
        if k.startswith('/boxscores/20'):
            container.append(k)
    return container[:82]

#second attempt to make soup
def soup_maker(dct:dict):
    boxscores = {}
    for team in dct.keys():
        boxscores[team] = {}
        for year in dct[team]['year'].keys():
            boxscores[team]['year'] = {}
            url = dct[team]['year'][int(year)][0]
            r = requests.get(url)
            soup = BeautifulSoup(r.content,'html.parser')
            boxscores[team]['year'][int(year)] = get_box_score_url(soup)
            time.sleep(3)
    return boxscores

#Write a function that extracts data and stores it in proper dictionaries
#Basica box score stats for each team and also information on officals
#assume first official is HEAD OFFICIAL?

#html = r.content, returns dictionary of box score totals
def scrape_stats_from_page(html,team:str):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select(f'#box_{team.lower()}_basic tfoot tr td')
    return {item.attrs.get('data-stat'): item.text for item in items}

