#需求：登录 http://192.168.3.254/Home/user/login.html
import unittest
import os,sys
import ddt
from selenium import webdriver
from time import sleep
from base.YzmUtils2 import YzmUtil2
from base.ExcelUtil import ExcelUtil


#测试数据
cesi_data=ExcelUtil(os.getcwd()+"/data/data.xlsx", "Sheet1").return_dict_data();

@ddt.ddt
class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        url = "http://192.168.3.254/Home/user/login.html"
        self.driver.get(url)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self):
        sleep(5)
        self.driver.quit()

    @ddt.data(*cesi_data)
    def test01(self,dict_data):
        zanhao=dict_data["zanhao"];
        pwd=dict_data["pwd"];
        self.driver.find_element_by_id("username").send_keys(zanhao)
        self.driver.find_element_by_id("password").send_keys(pwd);
        #输入验证码的方法1：API技术自动识别验证码
        img_yzm=self.driver.find_element_by_id("verify_code_img");
        yzm=YzmUtil2("jimo","JIMOqinyu319",self.driver,img_yzm).returnYzmStr();
        print("自动识别的验证码=",yzm)
        self.driver.find_element_by_id("verify_code").send_keys(yzm);

        #输入验证码的方法2：手动输入验证码
        #sleep(15);#目的：为了让手动输入验证码

        self.driver.find_element_by_name("sbtbutton").click();

        #断言登录是否成功,这里省略



# if __name__ == '__main__':
#     unittest.main()