# coding=utf-8

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded'
}
session = requests.session()
session.headers.update(header)

def login():
    url = ''