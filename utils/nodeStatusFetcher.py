import random
import requests
from subprocess import Popen, PIPE, TimeoutExpired
import datetime as dt


def fetchPingStr(nodeIp, timeoutSecs=0.5):
    proc = Popen('ping {0} -n 1 -w {1}'.format(nodeIp,
                                               int(timeoutSecs*1000)).split(' '), stdout=PIPE)
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
    if errs != None:
        return ''
    resp = outs.decode("utf-8")
    return resp


def deriveStatusFromCmdStr(cmdStr):
    if 'host unreachable' in cmdStr:
        return 0
    else:
        if 'Received = 1' in cmdStr:
            return 1
    return 0


def fetchNodeStatus(nodeIp, timeoutSecs=0.5):
    cmdStr = fetchPingStr(nodeIp, timeoutSecs)
    nodeStatus = deriveStatusFromCmdStr(cmdStr)
    return nodeStatus
