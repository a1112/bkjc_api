
import requests


def getOracleData(steelNo="4B038871010301"):
    jsData = requests.get(f"http://172.25.2.43:1002/search/steelNo/{steelNo}").json()
    if jsData:
        return {
            "pout_ackAgeNo": jsData[0],
            "steelType": jsData[1],
            "steelNo": jsData[2]
        }


def getPackageNo(steelNo):
    try:
        return getOracleData(steelNo)
    except:
        return ""


if __name__=="__main__":
    print(getOracleData())
