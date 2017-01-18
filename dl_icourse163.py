# -*- coding:utf-8 -*-

import requests
import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

content_url = 'http://www.icourse163.org/learn/JLU-1001540001?tid=1001855008#/learn/content'

lesson_url = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLastLearnedMocTermDto.dwr'

headers = {
	'Cookie':'',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

content_data = {
	'callCount': 1,
	'scriptSessionId': '${scriptSessionId}190',
	'httpSessionId': '',
	'c0-scriptName': 'CourseBean',
	'c0-methodName': 'getLastLearnedMocTermDto',
	'c0-id': 0,
	'c0-param0': 'number:1001855008',
	'batchId': '1484662263376'
}


def get_lesson_content_info(headers,data,url):
    response = requests.post(lesson_url, headers=headers, data=data)
    return response.content.decode('unicode_escape')

def get_lesson_name(headers):
    response = requests.get(content_url,headers=headers)
    courseTxt_reg = 'courseTxt\"\>(.+?)\<\/h4\>'

    lines = response.content.splitlines(True)
    for line in lines:
        result = re.search(courseTxt_reg, line)
        if result:
            return result.group(1)

def parser_lesson_content(content):
    lines = content.splitlines(True)
    content = {}

    content['name'] = '计算机网络技术'#get_lesson_name(headers)
    content['chapters'] = []

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
            content['chapters'].append(chapter)
        else:
           is_video = re.search(vid_reg, line)
           if is_video:
               lesson = {}
               name = is_video.group(2)
               lesson['name'] = name.replace('/','_') if name.find('/') is not -1 else name
               lesson['id'] = is_video.group(1)
               content['chapters'][chapter_index]['lessons'].append(lesson)            

    return content
       
def print_content(content):
    print "content_name:%s" %content['name']
    print "chapters:" 
    for each in content['chapters']:
        print "\tchapter_name:%s" %each['name']
        print "\tlessons:"
        for lesson in each['lessons']:
            print "\t\tlesson_name:%s" %lesson['name']
            print "\t\tlesson_id:%s" %lesson['id']
        
def get_video_link(id):
    get_lesson_url = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
    data = {
        'callCount':1,
        'scriptSessionId':'${scriptSessionId}190',
        'httpSessionId':'',
        'c0-scriptName':'CourseBean',
        'c0-methodName':'getLessonUnitLearnVo',
        'c0-id':0,
        'c0-param0':'number:{}'.format(id),
        'c0-param1':'number:1',
        'c0-param2':'number:0',
        'c0-param3':'number:1002572090',
        'batchId':'1484662263450'
    }
    response = requests.post(get_lesson_url, data=data, headers=headers)
    mp4_reg = r'mp4SdUrl="(.+?)";'
    lines = response.content.splitlines(True)
    for line in lines:
        is_mp4 = re.search(mp4_reg, line)
        if is_mp4:
           return is_mp4.group(1)

def get_video(link, filename):
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
 
    
def download_video(path, lesson):
    if not os.path.isfile(path):
       link = get_video_link(lesson['id'])
       get_video(link, path) 
       print path
    

lesson_content = get_lesson_content_info(headers,content_data,content_url)
content = parser_lesson_content(lesson_content)
print_content(content)
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
            download_video(file_path, lesson)
