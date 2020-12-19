import json
from typing import TypedDict


class IAppConfig(TypedDict):
    nodesExcelPath: str
    tokenUrl: str
    clientId: str
    clientSecret: str
    clientScope: str
    pingStatusCreationEndPnt: str


def getConfig(fName: str = "config.json") -> IAppConfig:
    with open(fName) as f:
        data = json.load(f)
        return data
