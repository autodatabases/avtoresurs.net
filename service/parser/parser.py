import datetime
import os
from avtoresurs_new.settings import DIR, MEDIA_ROOT

def get_filename(filename):
    dir = 'default'
    if filename == 'Klients.csv':
        dir = DIR['KLIENTS']
    elif filename == 'NewsAuto.csv':
        dir = DIR['PRICE']
    elif 'News_auto_' in filename:
        dir = DIR['PRICE']
    elif filename == 'Priz.csv':
        dir = DIR['BONUS']
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    new_filename = os.path.join(MEDIA_ROOT, DIR['CSV'], dir, year, month, day, filename)
    return new_filename



