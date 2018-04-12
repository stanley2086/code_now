# -*- coding: utf-8 -*-
from Base.BaseAppiumServer import AppiumServer
from Base.BaseLog import myLog
import unittest
from appium import webdriver
import os
from Base.BaseElementEnmu import Element
import platform
import time
from Base.BaseYaml import getYam

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def appium_testcase(devices):
    desired_caps = {}

    if str(devices["platformName"]).lower() == "android":
        desired_caps['appPackage'] = devices["appPackage"]
        desired_caps['appActivity'] = devices["appActivity"]
        desired_caps['udid'] = devices["deviceName"]
        # desired_caps["recreateChromeDriverSessions"] = "True"
        # 解决多次切换到webview报错问题，每次切换到非chrome-Driver时kill掉session 注意这个设置在appium 1.5版本上才做了处理
        # desired_caps["automationName"] = "uiautomator2"
    else: #(IOS系统）
        desired_caps['bundleId'] = devices["bundleId"]
        desired_caps['udid'] = devices["udid"]
        # desired_caps['automationName'] = devices["automationName"] # Xcode8.2以上无UIAutomation,需使用XCUITest
        # desired_caps['newCommandTimeout'] = 3600  # 1 hour

    desired_caps['platformVersion'] = devices["platformVersion"]
    desired_caps['platformName'] = devices["platformName"]
    desired_caps['deviceName'] = devices["deviceName"]
    desired_caps["noReset"] = "True"
    desired_caps['noSign'] = "True"
    desired_caps["unicodeKeyboard"] = "True"
    desired_caps["resetKeyboard"] = "True"
    #desired_caps["automationName"] = devices['automationName']
    #desired_caps["systemPort"] = devices["systemPort"]
    # desired_caps['app'] = devices["app"]
    remote = "http://127.0.0.1:" + str(devices["port"]) + "/wd/hub"
    driver = webdriver.Remote(remote, desired_caps)
    return driver


class ParametrizedTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.devices = param

    def setUp(self):
        self.driver = appium_testcase(self.devices)
        self.devicesName = self.devices["deviceName"]
        self.logTest = myLog().getLog(self.devicesName)  # 每个设备实例化一个日志记录器

    def tearDown(self):
        self.driver.close_app()
        self.driver.quit()


    @staticmethod
    def parametrize(testcase_klass, param=None):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite
