from utils.nodeStatusFetcher import fetchNodeStatus
from appConfig import getConfig
import pandas as pd
import sys
import datetime as dt
import requests
from utils.idSrvUtils import getAccessTokenFromSts

appConfig = getConfig()

# read the nodes info
nodesInfoPath = appConfig["nodesExcelPath"]
nodesDf = pd.read_excel(nodesInfoPath)

ipCol = 'ip'
nameCol = 'name'
if (ipCol not in nodesDf) or (len(nodesDf[ipCol]) == 0):
    sys.exit('IPs not present or not found in nodes.xlsx file...')

if (nameCol not in nodesDf) or (len(nodesDf[nameCol]) == 0):
    sys.exit('Names not present or not found in nodes.xlsx file...')

# remove duplicate rows based on the name and ip columns
nodesDf = nodesDf.drop_duplicates(subset=nameCol, keep="first")
nodesDf = nodesDf.drop_duplicates(subset=ipCol, keep="first")

statusList = []

for nRow in range(nodesDf.shape[0]):
    nIp = nodesDf[ipCol].iloc[nRow]
    nName = nodesDf[nameCol].iloc[nRow]
    nodeStatus = fetchNodeStatus(nIp, 0.5)
    nowTimeStr = dt.datetime.strftime(dt.datetime.now(), '%d_%m_%Y_%H_%M_%S')
    statusList.append({'data_time': nowTimeStr, 'ip': nIp,
                       'name': nName, 'status': nodeStatus})

payload = {
    "statusList": statusList
}
# print(statusList)

# get access token from STS
tokenUrl = appConfig["tokenUrl"]
clientId = appConfig["clientId"]
clientSecret = appConfig["clientSecret"]
clientScope = appConfig["clientScope"]
accessToken = getAccessTokenFromSts(tokenUrl, clientId, clientSecret, clientScope)
# print(accessToken)

endpoint = appConfig["pingStatusCreationEndPnt"]
res = requests.post(endpoint, json=payload, headers={'Authorization': 'Bearer {}'.format(accessToken)})
# print(res.text)