# -*- coding: utf-8 -*-

__author__ = 'shikun'
import sys

sys.path.append("..")
import platform
from Base.BaseAndroidPhone import *
from Base.BaseAdb import *
from Base.BaseRunner import ParametrizedTestCase
from TestCase.Settings_Search01 import test_Setting_20_01 #20代表search
from TestCase.Settings_Search02 import test_Setting_20_02
from TestCase.MyMoney_MainUI_01 import test_MainUI_01_01
from Base.BaseAppiumServer import AppiumServer
from multiprocessing import Pool
import unittest
from Base.BaseInit import init, mk_file
from Base.BaseStatistics import countDate, writeExcel, countSumDevices
from Base.BasePickle import *
from datetime import datetime

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

def kill_adb():
    if platform.system() == "Windows":
        # os.popen("taskkill /f /im adb.exe")
        os.system(PATH("/01code_relevant/Automator_SZ_Support/app/kill5037.bat"))
    else:
        os.popen("killall adb")
    os.system("adb start-server")

def runnerPool(getDevices):
    devices_Pool = []

    for i in range(0, len(getDevices)):
        #_pool = []
        print("----runnerPool------")
        print(getDevices[i])
        #配置Appium Driver
        desired_c = {}
        desired_c["deviceName"] = getDevices[i]["devices"]
        desired_c["platformVersion"] = getPhoneInfo(devices=desired_c["deviceName"])["release"]
        # desired_c["platformVersion"] = "6.0"
        desired_c["platformName"] = "android"
        desired_c["port"] = getDevices[i]["port"]
        # desired_c["appPackage"] = "com.android.settings"
        # desired_c["appActivity"] = ".Settings"
        desired_c["appPackage"] = "com.mymoney"
        desired_c["appActivity"] = ".biz.main.MainActivity"
        #desired_c["automationName"] = "uiautomator2"
        #desired_c["systemPort"] = getDevices[i]["systemPort"]
        # desired_c["appPackage"] = apkInfo.getApkBaseInfo()[0]
        # desired_c["appActivity"] = apkInfo.getApkActivity()
        # desired_c["app"] = getDevices[i]["app"]
        #_pool.append(desired_c)
        devices_Pool.append(desired_c)

    pool = Pool(len(devices_Pool))
    pool.map(runnerCaseApp, devices_Pool)
    pool.close()
    pool.join()


def runnerCaseApp(devices):
    starttime = datetime.now()
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(test_MainUI_01_01, param=devices))
    #suite.addTest(ParametrizedTestCase.parametrize(test_Setting_20_01, param=devices))
    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.now()
    countDate(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str((endtime - starttime).seconds) + "秒")

if __name__ == '__main__':

    kill_adb()

    Devices = AndroidDebugBridge().attached_devices()
    if len(Devices) > 0:
        mk_file()
        l_devices = []
        #l_devices 会把多个phone_config添加进去，每1个phone_config包括基础的driver配置信息
        for device in Devices:
            phone_config = {}
            phone_config["devices"] = device
            #init(device)  #初始化每一台设备，安装 uiautomato2两个apk
            phone_config["port"] = str(random.randint(4700, 4900))
            phone_config["bport"] = str(random.randint(4700, 4900))
            #phone_config["systemPort"] = str(random.randint(4700, 4900))
            l_devices.append(phone_config)

        appium_server = AppiumServer(l_devices)
        appium_server.start_server()
        runnerPool(l_devices)
        writeExcel()
        appium_server.stop_server(l_devices)
    else:
        print("没有可用的安卓设备")
