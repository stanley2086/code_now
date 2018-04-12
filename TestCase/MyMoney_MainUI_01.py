from Base.BaseRunner import ParametrizedTestCase
from PageObject.P_Base import p_base
from Base.BaseTestBase import *
import sys

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
'''
主页面点击记一笔
'''


class test_MainUI_01_01(ParametrizedTestCase):

    def setUp(self):
        super(test_MainUI_01_01, self).setUp()

    def tearDown(self):
        super(test_MainUI_01_01, self).tearDown()

    #测试用例
    def test_MainUI_MakeAnote(self):
        #建立app字典 ，其中1，2,3，参数来源于BaseRunner-->ParametrizedTestCase中的SetupClass
        app = {}
        app["logTest"] = self.logTest
        app["driver"] = self.driver
        app["device"] = self.devicesName
        app["path"] = PATH("../yaml/cards/MyMoney_MainUI_01.yaml") #定义测试步骤所在的yaml文件
        app["launch_app"] = 0 # 0 表示重启app，1表示不需重启app
        app["caseName"] = sys._getframe().f_code.co_name #定义测试用例名称，也就是testAsortCasd这个函数名
        #将app注入到用例中
        page = p_base(app) #实例化用例执行类
        page.operate()   #执行用例
        page.checkPoint() #检查用例

