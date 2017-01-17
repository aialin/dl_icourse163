# dl_icourse163
用来下载中国大学mooc的课程视频

由于还是一个简单的实现版本，目前仍需要手动对代码一些基本配置进行修改。


#使用方法:
1.登录icourse163。

2.按F12进入开发者模式,选择Network,再按F5刷新页面，可以看到网页加载过程中发起的请求。

3.随便选择Name中的一个请求，在Headers中找到Request Headers中的Cookie，添加到代码的cookie选项中，如下所示：

    headers = {

        'Cookie':'',#添加到这儿
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

4.点进想要下载的课程的学习页面，如课件页面，复制所在页面的地址，修改地址，如下所示：
    
    content_url = 'http://www.icourse163.org/learn/JLU-1001540001?tid=1001855008#/learn/content'

5.在开发者工具Network中找到CourseBean.getLastLearnedMocTermDto.dwr链接，点击查看其Request Payload,修改代码中content_data的值与之一致。

6.随便点开一个课程，在Network中找到CourseBean.getLessonUnitLearnVo.dwr链接，点击查看其Request Payload,修改get_video_link函数中的data的值与之一致。

7.修改课程的名称：如下所示：content['name'] = '课程名称'

    def parser_lesson_content(content):
        lines = content.splitlines(True)
        content = {}

        content['name'] = '计算机网络技术'
        ````````
      
8.至此，修改完成，执行python dl_icourse163.py,等待下载完成吧。


由于对http协议的理解及应用上仍有不足，以及爬虫时icourse163有些信息是js代码生成的，对这方面的处理经验不足，所以需要手动操作的环节较多。

下一步优化目标即为解决js代码生成部分的网页内容的抓取，以及对cookie的处理。

如果您有好的建议，欢迎指点，谢谢～
