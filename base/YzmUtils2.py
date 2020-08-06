#图鉴打码平台：http://www.ttshitu.com/
import json
import requests
import base64
from io import BytesIO
from PIL import Image
from sys import version_info

#验证码识别工具2（即墨推荐用这个）
class YzmUtil2:
    #形参zanhao:图鉴打码平台的登录账号
    #形参pwd:图鉴打码平台的登录密码
    # 形参driver:WebDriver类对象。Selenium的WebDriver对象，即浏览器驱动！
    # 形参img_yzm:WebElement类对象。某验证码图片Img标签对应的WebElement类对象。例如:drver.find_elementXXX的返回值
    # 形参temp_screen_path: String类型，屏幕截图的临时保存目录！
    # 形参temp_yzm_path:String类型。验证码小图的临时保存目录！
    def __init__(self,zanhao,pwd,driver,img_yzm,temp_screen_path="C:/A/screen.png",temp_yzm_path="C:/A/yzm.png"):
        self.zanhao=zanhao;
        self.pwd=pwd;
        self.driver = driver;
        self.temp_screen_path = temp_screen_path;
        self.img_yzm = img_yzm;
        self.temp_yzm_path = temp_yzm_path;

    #返回验证码字符串或错误提示信息
    def returnYzmStr(self):
        # 屏幕截图
        self.driver.save_screenshot(self.temp_screen_path);
        img_yzm_zuosanjiao = self.img_yzm.location;  # 验证码图片的左上角的xy坐标
        # print(img_yzm_zuosanjiao);##{'x': 384, 'y': 413}
        left_x = img_yzm_zuosanjiao["x"];
        left_y = img_yzm_zuosanjiao["y"];
        # 获取验证码图片的宽度和高度
        img_yzm_width = self.img_yzm.size["width"];
        img_yzm_height = self.img_yzm.size["height"];
        right_x = left_x + img_yzm_width;
        right_y = left_y + img_yzm_height;
        # print(left_x,left_y,right_x,right_y);

        a = Image.open(self.temp_screen_path);
        # 截真正的验证码部分，截图4个坐标区域
        yzm = a.crop((left_x, left_y, right_x, right_y));
        yzm.save(self.temp_yzm_path);

        img_path = self.temp_yzm_path;#img_path="C:/A/yzm.jpg"
        img1 = Image.open(img_path)
        img = img1.convert('RGB')
        buffered = BytesIO()
        #img.save(buffered, format="JPEG")
        img.save(buffered,format="PNG");
        if version_info.major >= 3:
            b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
        else:
            b64 = str(base64.b64encode(buffered.getvalue()))
        data = {"username": self.zanhao, "password": self.pwd, "image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]





