#参考：https://www.cnblogs.com/wangx123sec/p/11495103.html
#阿里云验证码识别API：https://market.aliyun.com/products/57124001/cmapi00035185.html?spm=5176.730005.productlist.d_cmapi00035185.17953524KGOdQG&innerSource=search_%E5%9B%BE%E7%89%87%E9%AA%8C%E8%AF%81%E7%A0%81%E8%AF%86%E5%88%AB#sku=yuncode2918500001
from PIL import Image
import base64
import urllib
import json

#验证码识别工具1
class YzmUtil1:
    #形参driver:WebDriver类对象。Selenium的WebDriver对象，即浏览器驱动！
    #形参img_yzm:WebElement类对象。某验证码图片Img标签对应的WebElement类对象。例如:drver.find_elementXXX的返回值
    #形参appCode:String类型。阿里云的签约APPCode！
    #形参temp_screen_path: String类型，屏幕截图的临时保存目录！
    #形参temp_yzm_path:String类型。验证码小图的临时保存目录！
    def __init__(self,driver,img_yzm,appCode,temp_screen_path="C:/A/screen.png",temp_yzm_path="C:/A/yzm.png"):
        self.driver=driver;
        self.temp_screen_path=temp_screen_path;#"C:/A/screen.png"
        self.img_yzm=img_yzm;
        self.temp_yzm_path=temp_yzm_path;
        self.appCode=appCode;

    #函数功能：返回验证码字符串。即墨：貌似只能识别4位图形验证码
    def returnYzmStr(self):
        #屏幕截图
        self.driver.save_screenshot(self.temp_screen_path);
        img_yzm_zuosanjiao=self.img_yzm.location;#验证码图片的左上角的xy坐标
        #print(img_yzm_zuosanjiao);##{'x': 384, 'y': 413}
        left_x=img_yzm_zuosanjiao["x"];
        left_y=img_yzm_zuosanjiao["y"];
        #获取验证码图片的宽度和高度
        img_yzm_width=self.img_yzm.size["width"];
        img_yzm_height=self.img_yzm.size["height"];
        right_x=left_x+img_yzm_width;
        right_y=left_y+img_yzm_height;
        #print(left_x,left_y,right_x,right_y);

        a=Image.open(self.temp_screen_path);
        #截真正的验证码部分，截图4个坐标区域
        yzm=a.crop((left_x,left_y,right_x,right_y));
        yzm.save(self.temp_yzm_path);

        #阿里云api识别
        host = 'https://codevirify.market.alicloudapi.com'
        path = '/icredit_ai_image/verify_code/v1'
        # 阿里云APPCODE
        #appcode = '1be2786f607f49a69ee7848a4906384b'
        url = host + path
        bodys = {}
        querys = ""

        f=open(self.temp_yzm_path,"rb");
        yzm_stream=base64.b64encode(f.read());
        f.close();
        bodys['IMAGE'] = yzm_stream
        bodys['IMAGE_TYPE'] = '0'

        post_data = urllib.parse.urlencode(bodys).encode('utf-8')

        request = urllib.request.Request(url, post_data)
        request.add_header('Authorization', 'APPCODE ' + self.appCode)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        result_yzm="";
        if (content):
            result_json_str=content.decode('utf-8');
            result_json=json.loads(result_json_str);
            result_yzm=result_json["VERIFY_CODE_ENTITY"]["VERIFY_CODE"];

        return result_yzm;