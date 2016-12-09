from CONFIG import *

from pyshorteners import Shortener
google = Shortener('Google', api_key=GOOGLE_API_KEY, timeout=10)
tinyurl = Shortener('Tinyurl', timeout=10)
adfly = Shortener('Adfly', uid=ADFLY_UID, key=ADFLY_API_KEY, type='int', timeout=10)
isgd = Shortener('Isgd', timeout=10)
bitly = Shortener('Bitly', bitly_token=BITLY_ACCESS_TOKEN)

import sqlite3
conn = sqlite3.connect(DATABASE_PATH)
c = conn.cursor()

try:
    c.execute('CREATE TABLE users(user_id INTEGER)')
except sqlite3.OperationalError:
    pass

def add_user(user_id):
    c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    if not c.fetchall():
        c.execute('INSERT INTO users VALUES(?)', (user_id,))
    conn.commit()

def remove_user(user_id):
    c.execute('DELETE FROM users WHERE user_id=?', (user_id,))
    conn.commit()

def count_users():
    c.execute('SELECT COUNT(*) FROM users')
    for res in c.fetchall():
        return res[0]

def short(service, url):
    url = 'http://' + url.replace('https://', '').replace('http://', '') # Simple but it works

    if service.lower() == 'google':
        return google.short(url)

    if service.lower() == 'tinyurl':
        return tinyurl.short(url)

    if service.lower() == 'adfly':
        return adfly.short(url)

    if service.lower() == 'isgd':
        return isgd.short(url)

    if service.lower() == 'bitly':
        return bitly.short(url)
