import requests

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + ID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestChampLists(region, AID, CID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + AID + "?beginIndex=99999" + "&champion=" + CID + "&api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestMatchLists(region, AID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + AID + "?beginIndex=99999" + "&api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestChampMastery(region, ID, CID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + ID + "/by-champion/" + CID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestChampWinrate(region, AID, CID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + AID + "?endIndex=50" + "&champion=" + CID + "&queue=420" + "&api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def RequestChampMatch(gameID):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + gameID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def winrate(winloss: list):
    return winloss[0] / (winloss[0] + winloss[1]) * 100


region = (str)(input('Region: '))
summonerName = (str)(input('Summoner Name: '))
CID = (str)(input('Champion ID: '))
APIKey = "RGAPI-########-####-####-####-############"
win_loss = [0,0]

responseJSON  = requestSummonerData(region, summonerName, APIKey)
ID = str(responseJSON['id'])
AID = str(responseJSON['accountId'])

responseJSON2 = requestRankedData(region, ID, APIKey)
print("\nTIER:", (responseJSON2[0]['tier']))
print("RANK:", (responseJSON2[0]['rank']))
print("LP:", (responseJSON2[0]['leaguePoints']))

responseJSON3 = requestChampLists(region, AID, CID, APIKey)
otGames = int(responseJSON3['totalGames'])

responseJSON4 = requestMatchLists(region, AID, APIKey)
total = int(responseJSON4['totalGames'])

if otGames / total >= 0.45:
    print("OTP: YES")
else:
    print("OTP: NO")
    
responseJSON5 = requestChampMastery(region, ID, CID, APIKey)
print("MASTERY POINTS:", (responseJSON5['championPoints']))

matchList = requestChampWinrate(region, AID, CID, APIKey)

for match in matchList['matches']:
    GID = str(match['gameId'])
    matchInfo = RequestChampMatch(GID)
    participantId = 0
    for player in matchInfo['participantIdentities']:
        if player['player']['summonerName'] == summonerName:
            participantId = player['participantId']
    if participantId <= 5:
        participantId = 0
    else:
        participantId = 1
    if matchInfo['teams'][participantId]['win'] == 'Win':
        win_loss[0] += 1
    else:
        win_loss[1] += 1
print('\n')
print(win_loss[0], 'WINS', win_loss[1], 'LOSSES')
print("RATING: " + ('%.2f'%(winrate(win_loss)) + "%"))
