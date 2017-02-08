# dl_icourse163说明

---
## 目的
+ 下载中国大学mooc的课程视频

---
## 测试环境
+ 目前的测试环境为:Python2.7 + Ubuntu 16

---
## 使用详细说明

#### 方法一：采用dl_icourse163_selenium
---
##### 需要的环境准备
+ chrome浏览器

+ 对应chrome版本的chromedriver 
 + 下载地址:http://chromedriver.storage.googleapis.com/index.html
 + 文件夹内的notes可以看到与Chrome的版本对应
 + 下载完成后，放置到环境变量路径之下
---
##### 操作步骤
1. 打开dl_icourse163_selenium，在以下代码处，将content_url地址改为对应的课程地址，如下：

   ```Python
    def get_lesson_name(self):
        content_url = 'http://www.icourse163.org/learn/JLU-1001540001?tid=1001855008#/learn/content'
   ```
2. 接着用python执行dl_icourse163_selenium，如下：

    ```Shell
    python dl_icourse163_selenium.py
    ```

3. 等待下载完毕即可。

#### 方法二：使用dl_icourse163版本
1. 登录icourse163。
2. 按F12进入开发者模式,选择Network,再按F5刷新页面，可以看到网页加载过程中发起的请求。
3. 随便选择Name中的一个请求，在Headers中找到Request Headers中的Cookie，添加到代码的cookie选项中，如下所示：
headers = { 'Cookie':'',#添加到这儿 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' }

4. 点进想要下载的课程的学习页面，如课件页面，复制所在页面的地址，修改地址，如下所示：
content_url = 'http://www.icourse163.org/learn/JLU-1001540001?tid=1001855008#/learn/content'

5. 在开发者工具Network中找到CourseBean.getLastLearnedMocTermDto.dwr链接，点击查看其Request Payload,修改代码中content_data的值与之一致。

6. 随便点开一个课程，在Network中找到CourseBean.getLessonUnitLearnVo.dwr链接，点击查看其Request Payload,修改get_video_link函数中的data的值与之一致。

7. 修改课程的名称：如下所示：content['name'] = '课程名称'
def parser_lesson_content(content): lines = content.splitlines(True) content = {} content['name'] = '计算机网络技术' ````````

8. 至此，修改完成，执行python dl_icourse163.py,等待下载完成吧。

