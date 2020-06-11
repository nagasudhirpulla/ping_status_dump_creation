from nodeStatusFetcher import fetchNodeStatus
import pandas as pd
import sys
import datetime as dt
import argparse
import os

parser = argparse.ArgumentParser()
# add argument with flag --chunksFolder
parser.add_argument(
    '--chunksFolder', help='The folder path for dumping the status files')
parser.add_argument('--nodesInfoPath',
                    help='The file path of excel that contains the nodes info')

args = parser.parse_args()
# read chunksFolder from arguments
chunksFolder = args.chunksFolder
if chunksFolder == None:
    chunksFolder = ''

# read chunksFolder from arguments
nodesInfoPath = args.nodesInfoPath
if nodesInfoPath == None:
    nodesInfoPath = 'nodes.xlsx'

# read the nodes info
nodesDf = pd.read_excel(nodesInfoPath)

ipCol = 'ip'
nameCol = 'name'
if (ipCol not in nodesDf) or (len(nodesDf[ipCol]) == 0):
    sys.exit('IPs not present or not found in nodes.xlsx file...')

if (nameCol not in nodesDf) or (len(nodesDf[nameCol]) == 0):
    sys.exit('Names not present or not found in nodes.xlsx file...')

# remove duplicate rows based on the name and ip columns

statusList = []

for nRow in range(nodesDf.shape[0]):
    nIp = nodesDf[ipCol].iloc[nRow]
    nName = nodesDf[nameCol].iloc[nRow]
    nodeStatus = fetchNodeStatus(nIp, 0.5)
    nowTimeStr = dt.datetime.strftime(dt.datetime.now(), '%d_%m_%Y_%H_%M_%S')
    statusList.append([nowTimeStr, nIp, nName, nodeStatus])

statusDf = pd.DataFrame(data=statusList, columns=['data_time', 'ip', 'name', 'status'])
# print(statusDf)

# get the filepath of the status dump file
dumpfileName = 'node_status_{0}.csv'.format(
    int(1e6 * dt.datetime.timestamp(dt.datetime.now())))
dumpfileName = os.path.join(chunksFolder, dumpfileName)
# print(dumpfileName)

statusDf.to_csv(dumpfileName, index=False)
