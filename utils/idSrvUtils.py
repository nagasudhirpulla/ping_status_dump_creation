import requests
import datetime as dt


def getAccessTokenFromSts(tokenUrl, clientId, clientSecret, clientScope):
    tokenFetchUrl = tokenUrl
    payload = {
        'grant_type': 'client_credentials',
        'client_id': clientId,
        'client_secret': clientSecret,
        'scope': clientScope
    }
    resp = requests.post(tokenFetchUrl, data=payload)
    respJson = resp.json()
    accessToken = respJson['access_token']
    return accessToken
