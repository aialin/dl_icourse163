# -*- coding:utf-8 -*-
import time
from selenium import webdriver
import getpass
import requests
import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Icourse:
    def __init__(self):
        pass

    def login(self):
        url = 'http://www.icourse163.org/'
        self._driver= webdriver.Chrome()
        self._driver.get(url)
        self._driver.find_element_by_id('navLoginBtn').click()
        self._driver.switch_to_frame(self._driver.find_element_by_tag_name('iframe').get_attribute('id'))

        while True:
            username = raw_input('Input your email:')
            password = getpass.getpass('Input your password:')

            email = self._driver.find_element_by_name('email')
            email.clear()
            email.send_keys(username)
            psw = self._driver.find_element_by_name('password')
            psw.clear()
            psw.send_keys(password)

            self._driver.find_element_by_id('dologin').click()
            time.sleep(2)
            try:
                self._driver.find_element_by_tag_name('iframe')
                continue
            except Exception,e:
                return True
        
    def create_cookie(self):
        self._cookie = ''
        for cookie in self._driver.get_cookies():
            self._cookie += cookie['name'] + '=' + cookie['value']+ ';'
        return self._cookie       

    def create_headers(self):
        self._headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self._headers['Cookie'] = self._cookie

    def create_content_data(self):
        self._content_data = {
            'callCount': 1,
            'scriptSessionId': '${scriptSessionId}190',
            'c0-scriptName': 'CourseBean',
            'c0-methodName': 'getLastLearnedMocTermDto',
            'c0-id': 0,
            'c0-param0': 'number:1001855008',
            'batchId': '1484662263376'
        }       
        pattern = re.compile('NTESSTUDYSI=(.*?);')
        self._str_session_id = re.search(pattern, self._cookie).groups()[0]
        self._content_data['httpSessionId'] = self._str_session_id

    def get_content_map(self):
        return self._content

    def close_driver(self):
        self._driver.close()

    def get_lesson_content(self):
        url = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLastLearnedMocTermDto.dwr'
        response = requests.post(url, headers=self._headers, data=self._content_data)
        self._lesson_content = response.content.decode('unicode_escape')

    def parse_lesson_content(self):
        lines = self._lesson_content.splitlines(True)
        self._content = {}
 
        self._content['name'] = self._lesson_name
        self._content['chapters'] = []
    
        chapter_reg = 'contentId=null.+lessons=.+name="(.+)";.+releaseTime='
        vid_reg = 'contentId=([0-9]+);.+contentType=1;.+name=\"(.+)\";'
        doc_id_reg = 'contentId=([0-9]+);.+contentType=3;'
        lecture_reg = 'contentId=null.+name=\"(.+)\";.+releaseTime='
    
        chapter_index = -1
        for line in lines:
            is_chapter = re.search(chapter_reg, line)
    	    if is_chapter:
                name = is_chapter.group(1)
                chapter = {}
                chapter['name'] = name.replace('/','_') if name.find('/') is not -1 else name
                chapter_index += 1
                chapter['lessons'] = []
                self._content['chapters'].append(chapter)
            else:
               is_video = re.search(vid_reg, line)
               if is_video:
                   lesson = {}
                   name = is_video.group(2)
                   lesson['name'] = name.replace('/','_') if name.find('/') is not -1 else name
                   lesson['id'] = is_video.group(1)
                   self._content['chapters'][chapter_index]['lessons'].append(lesson)            
    
        return self._content       

    def print_content(self):
        print "content_name:%s" %self._content['name']
        print "chapters:" 
        for each in self._content['chapters']:
            print "\tchapter_name:%s" %each['name']
            print "\tlessons:"
            for lesson in each['lessons']:
                print "\t\tlesson_name:%s" %lesson['name']
                print "\t\tlesson_id:%s" %lesson['id']

    def get_video_link(self, id):
        get_lesson_url = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
        data = {
            'callCount':1,
            'scriptSessionId':'${scriptSessionId}190',
            'httpSessionId': self._str_session_id,
            'c0-scriptName':'CourseBean',
            'c0-methodName':'getLessonUnitLearnVo',
            'c0-id':0,
            'c0-param0':'number:{}'.format(id),
            'c0-param1':'number:1',
            'c0-param2':'number:0',
            'c0-param3':'number:%s'%self._content_id,
            'batchId':'1484662263450'
        }
        response = requests.post(get_lesson_url, data=data, headers=self._headers)
        mp4_reg = r'mp4SdUrl="(.+?)";'
        lines = response.content.splitlines(True)
        for line in lines:
            is_mp4 = re.search(mp4_reg, line)
            if is_mp4:
               return is_mp4.group(1)

    def get_video(self, link, filename):
        print "downloading:%s"%filename
        from contextlib import closing
        headers = {
    	    'Connection': 'keep-alive',
    	    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
    
        with closing(requests.get(link, headers=headers, stream=True)) as response:
            with open(filename, 'wb') as fd:
                for chunk in response.iter_content(1024):
                    fd.write(chunk)
     
        
    def download_video(self, path, lesson):
        if not os.path.isfile(path):
           link = self.get_video_link(lesson['id'])
           self.get_video(link, path) 
           print path


    def get_lesson_name(self):
        content_url = 'http://www.icourse163.org/learn/JLU-1001540001?tid=1001855008#/learn/content'
        self._driver.get(content_url)
        self._lesson_name = self._driver.find_element_by_class_name('courseTxt').text
        pattern = re.compile(r'.*?tid=(.*?)#')
        self._content_id = re.search(pattern, content_url).groups()[0]
    
if __name__ == '__main__':
    icourse = Icourse()
        
    icourse.login()
    icourse.get_lesson_name()
    icourse.create_cookie()
    icourse.create_headers()
    icourse.create_content_data()
    icourse.close_driver()
    icourse.get_lesson_content()
    icourse.parse_lesson_content()
    icourse.print_content()
    
    content = icourse.get_content_map()
    if not os.path.exists(content['name']):
        os.mkdir(content['name'])
    for chapter in content['chapters']:
        path = content['name']+ "/" + chapter['name']
        if not os.path.exists(path):
            os.mkdir(path)
        count = 0
        for lesson in chapter['lessons']:
            file_path = path + "/"+ lesson['name'] + ".mp4"
            if not os.path.isfile(file_path):
                icourse.download_video(file_path, lesson)
