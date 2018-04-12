from Base.BaseAndroidPhone import getPhoneInfo
from Base.BaseStatistics import countSum, countInfo, countSumDevices


def statistics_result(**kwargs):
    countSum(kwargs["result"])
    get_phone = getPhoneInfo(kwargs["devices"])
    phone_name = get_phone["device"] + "_" + get_phone["UDID"] #这里Devices是软件代号，UDID是设备名
    version=get_phone["internal_version"]
    print('********************************************')
    print(version)
    software_ID = get_phone["device"]




    countInfo(result=kwargs["result"], testInfo=kwargs["testInfo"], caseName=kwargs["caseName"], phoneName=phone_name,
              driver=kwargs["driver"], logTest=kwargs["logTest"], devices=kwargs["devices"], testCase=kwargs["testCase"],
              testCheck=kwargs["testCheck"])
    countSumDevices(kwargs["devices"], kwargs["result"], phone_name=phone_name,version=version,software_ID=software_ID)#这里devices是设备名
