from Base.BaseYaml import getYam
from Base.BaseOperate import OperateElement
from Base.BaseElementEnmu import Element as be
from PageObject.SumResult import statistics_result


class p_settings_search01:
    '''
    滑动删除历史记录
    isOperate: 操作失败，检查点就失败,kwargs: WebDriver driver, String path(yaml配置参数)
    '''

    def __init__(self, kwargs):
        self.driver = kwargs["driver"]  #Driver
        if kwargs.get("launch_app", "0") == "0":  # 若为空，重新打开app
            self.driver.launch_app()
        self.path = kwargs["path"]   #用例参数yaml路径
        self.operateElement = OperateElement(self.driver) #元素操作
        self.isOperate = True  #元素是否可执行，默认为可以。

        #从yaml文件解析操作步骤和执行结果
        test_msg = getYam(self.path)
        self.testInfo = test_msg["testinfo"]
        self.testCase = test_msg["testcase"]
        self.testcheck = test_msg["check"]
        #每一条用例由  testinfo,testcase,check3部分组成，其中testcase由多个元素组成
        self.device = kwargs["device"]
        self.logTest = kwargs["logTest"]   #myLog().getLog(cls.devicesName)
        self.caseName = kwargs["caseName"] #测试函数名
        self.get_value = ['ERASE EVERYTHING']
        self.location = []
        self.msg = ""

    '''
     操作步骤
     logTest 日记记录器
    '''
    def operate(self):
        for item in self.testCase:   #解析出测试步骤（测试步骤包括多个元素）

            m_s_g = self.msg + "\n" if self.msg != "" else ""
            #如果msg非空，加\n，否则保持空

            result = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)
            #result:True or False
            #执行测试用例，并获取结果

            #如果result["result"] 为：None,False,'' ，则：
            if not result["result"]:
                msg = "执行失败，请检查元素是否存在：" + item["element_info"]
                self.msg = m_s_g + msg
                self.testInfo[0]["msg"] = msg
                self.isOperate = False
                return False

            #如果该用例的操作类型为 location,获取该控件的坐标self.location
            if item.get("operate_type", "0") == "location":
                app = {}
                web_element = self.driver.find_elements_by_id(item["element_info"])[item["index"]]
                start = web_element.location
                # 获取控件开始位置的坐标轴
                app["startX"] = start["x"]
                app["startY"] = start["y"]
                # 获取控件坐标轴差
                size1 = web_element.size

                width = size1["width"]
                height = size1["height"]
                # 计算出控件结束坐标
                endX = width + app["startX"]
                endY = height + app["startY"]

                app["endX"] = endX - 20
                app["endY"] = endY - 60

                print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                print(self.location)
                self.location.append(app)
                # self.driver.swipe(endX, endY, starty, endY)
                print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                print(self.location)

            #如果该用例的操作类型为 ：get_value （获取text)
            if item.get("operate_type", "0") == be.GET_VALUE:
                #将操作获得的text值，注入到 self.get_value中
                self.get_value.append(result["text"])

            #如果该用例中 is_swpie 不是0 的时候：（待确认）
            if item.get("is_swpie", "0") != "0":

                self.driver.swipe(self.location[0]["endX"], self.location[0]["endY"], self.location[1]["endX"], self.location[1]["endY"]+10)

        return True #（待确认）

    def checkPoint(self, kwargs={}):
        result = self.check()
        if result is not True and be.RE_CONNECT:
            self.msg = "ERROR: 用例曾失败,重连一次，失败原因:" + self.testInfo[0]["msg"]
            self.logTest.buildStartLine(self.caseName + "_失败重连")  # 记录日志
            self.operateElement.switchToNative()
            self.driver.launch_app()
            self.isOperate = True
            self.operate()
            self.get_value = [True]
            self.location = ""
            result = self.check()
            self.testInfo[0]["msg"] = self.msg

        statistics_result(result=result, testInfo=self.testInfo, caseName=self.caseName,
                          driver=self.driver, logTest=self.logTest, devices=self.device,
                          testCase=self.testCase,
                          testCheck=self.testcheck)
        return result

    '''
    检查点
    caseName:测试用例函数名 用作统计
    logTest： 日志记录
    devices 设备名
    contrary 相反检查点，意思就是如果检查结果为真，检查点就是失败
    '''

    def check(self):
        result = True
        m_s_g = self.msg + "\n" if self.msg != "" else ""
        # 重跑后异常日志
        if self.isOperate:  #默认为True
            for item in self.testcheck: #迭代yaml中check元素
                resp = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)
                #resp : maybe =  {'result': True, 'text': 'ERASEEVERYTHING'}
                if resp["result"] == True:
                    result = True
                if not resp["result"]:
                    msg = "Error：请检查元素" + item["element_info"] + "是否存在"
                    self.msg = m_s_g + msg
                    self.testInfo[0]["msg"] = msg
                    result = False
                if resp['text'] not in self.get_value:
                    #resp : {'result': True, 'text': 'ERASEEVERYTHING'}
                    msg = "Error：期望text为" + str(self.get_value) + "。 实际text为：" + resp["text"]
                    self.msg = m_s_g + msg
                    self.testInfo[0]["msg"] = msg
                    break
        else:
            result = False
        return result


# if __name__ == "__main__":
#     pass
