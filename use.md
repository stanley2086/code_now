## 测试用例-MyClassHistory.yaml

```buildoutcfg
testinfo:
    - id: test007
      title: 我的课程浏览记录
      info: 打开知识
testcase:

    - element_info: com.huawei.works.knowledge:id/ilearning_tv_course_name
      find_type: ids
      index: 0
      operate_type: get_value
      info: 获取我的课程卡片下第一条数据对标题
    - element_info: com.huawei.works.knowledge:id/ilearning_tv_course_name
      find_type: ids
      index: 0
      operate_type: click
      info: 点击我的课程卡片下对第一条数据
    - element_info: com.huawei.works.knowledge:id/tvw_course_title
      find_type: id
      info: 查找详情页到标题
    - element_info: com.huawei.works.knowledge:id/vtb_img_left
      find_type: id
      operate_type: click
      info: 点击返回按钮
    - element_info: com.huawei.works.knowledge:id/vtb_img_right2
      find_type: id
      operate_type: click
      info: 点击首页历史记录按钮
check:
    - element_info: com.huawei.works.knowledge:id/browser_knowledge_history_text
      find_type: ids
      index: 0
      operate_type: get_value
      info: 查找是否存在历史记录
```

##  Page

```buildoutcfg
from PageObject import Pages


class MyClassHistoryPage:
    '''
    我的课程浏览历史
    isOperate: 操作失败，检查点就失败,kwargs: WebDriver driver, String path(yaml配置参数)
    '''

    def __init__(self, **kwargs):
        self.driver = kwargs["driver"]
        self.path = kwargs["path"]
        self.page = Pages.PagesObjects(driver=self.driver, path=kwargs["path"])

    def operate(self, logTest):  # 操作步骤
        self.page.operate(logTest)

    def checkPoint(self, caseName, logTest, devices):  # 检查点
        self.page.checkPoint(caseName=caseName, logTest=logTest, devices=devices)

```

## testcase调用page

```buildoutcfg
class HomeTest(ParametrizedTestCase):
      # 多次浏览后的历史记录
    def testManyHistory(self):
        page = ManyHistoryPage(driver=self.driver, path=PATH("../yaml/home/ManyHistory.yaml"))
        page.operate(logTest=self.logTest)
        page.checkPoint(caseName=sys._getframe().f_code.co_name, logTest=self.logTest, devices=self.devicesName)

    # 我的课程浏览历史记录
    def testMyClassHistory(self):
        page = MyClassHistoryPage(driver=self.driver, path=PATH("../yaml/home/MyClassHistory.yaml"))
        page.operate(logTest=self.logTest)
        page.checkPoint(caseName=sys._getframe().f_code.co_name, logTest=self.logTest, devices=self.devicesName)
        
     @classmethod
    def setUpClass(cls):
        super(HomeTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(HomeTest, cls).tearDownClass()
```

## runner.py 调用

```buildoutcfg
    .........
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=devices))
    unittest.TextTestRunner(verbosity=2).run(suite)
```

## 关于Page类中的检查点关键字说明
- contrary：相反检查点，传1表示如果检查元素存在就说明失败
- toast: 表示提示框检查点
- contrary_getval: 相反值检查点，如果对比成功，说明失败
- check_point: 自定义检查结果

调用实例

```buildoutcfg

class ManyHistoryPage:
    '''
    isOperate: 操作失败，检查点就失败,kwargs: WebDriver driver, String path(yaml配置参数)
    '''

    def __init__(self, **kwargs):
        self.driver = kwargs["driver"]
        self.path = kwargs["path"]
        self.page = Pages.PagesObjects(driver=self.driver, path=kwargs["path"])

        '''
        操作步骤
         logTest 日记记录器
        '''

    def operate(self, logTest):
        self.page.operate(logTest)

    def checkPoint(self, caseName, logTest, devices):
        self.page.checkPoint(caseName=caseName, logTest=logTest, devices=devices,  check="contrary_getval")
```