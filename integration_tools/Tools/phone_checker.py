#!/usr/bin/python3
import json
import random
import requests
import httpx
from bs4 import BeautifulSoup
import sys
import hashlib
import hmac
import urllib.parse
import re

USERS_LOOKUP_URL = 'https://i.instagram.com/api/v1/users/lookup/'
SIG_KEY_VERSION = '4'
IG_SIG_KEY = 'e6358aeede676184b9fe702b30f4fd35e71744605e39d2181a34cede076b3c33'

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}


#Information from form


form = cgi.FieldStorage()
#Regex
if(re.match("[0-9]+$", form.getvalue("phone")):
    phone = form.getvalue("phone")
    result = form.getvalue("result")
else:
    print("ERROR : phone number is incorrect")

## AMAZON

async def amazon():
    async with httpx.AsyncClient(timeout=10) as client:
        url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
        req = await client.get(url, headers=headers)

        body = BeautifulSoup(req.text, 'html.parser')
        data = {x["name"]: x.get("value", "") for x in body.select('form input[name]')}

        data["email"] = "33" + phone

        login_url = 'https://www.amazon.com/ap/signin/'
        req = await client.post(login_url, data=data)

        body = BeautifulSoup(req.text, 'html.parser')

        if body.find("div", {"id": "auth-password-missing-alert"}):
            return "[{\"Amazon\":\"True\"},"
        else:
            return "[{\"Amazon\":\"False\"},"

## INSTAGRAM

def generate_signature(data):
    return 'ig_sig_key_version=' + SIG_KEY_VERSION + '&signed_body=' + hmac.new(IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + urllib.parse.quote_plus(data)

def generate_data(phone_number_raw):
    data = {
        'login_attempt_count': '0',
        'directly_sign_in': 'true',
        'source': 'default',
        'q': phone_number_raw,
        'ig_sig_key_version': SIG_KEY_VERSION
    }
    return json.dumps(data)

async def instagram():
    async with httpx.AsyncClient() as client:
        phone_number = "33" + phone
        data = generate_signature(generate_data(str(phone_number)))

        headers = {
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "X-FB-HTTP-Engine": "Liger",
            "Connection": "close"
        }

        r = await client.post(USERS_LOOKUP_URL, headers=headers, content=data)
        rep = r.json()

        if "message" in rep and rep["message"] == "No users found":
            return "{\"Instagram\":\"False\"},"
        else:
            return "{\"Instagram\":\"True\"},"


if __name__ == "__main__":
    import asyncio
    import os
    import sys
    amazon = asyncio.run(amazon())
    instagram = asyncio.run(instagram())
    res = amazon+instagram
    os.system(f"touch ~/var/www/html/result/{phone}.json")
    os.system(f"echo {res} > ~/var/www/html/result/{phone}.json")
    print(amazon+instagram)
