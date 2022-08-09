from bs4 import BeautifulSoup
from requests import *


class Musics:
    def __init__(self):
        self.url = 'https://9jatoday.com/top-best-nigerian-songs-of-all-time/'
        self.musics_data = get(self.url).text
        self.musics = []
        self.soup = BeautifulSoup(self.musics_data, 'html.parser')

    def getMusics(self):
        self.musics = [music.getText() for music in self.soup.select('ol li')]
        return self.musics
