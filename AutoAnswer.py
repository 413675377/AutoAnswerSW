#!/usr/bin/env python3
import pytesseract
import sys
import subprocess
import shutil
import time
import random
import re
import os
from PIL import Image
from question_and_answer import data_list
from question_and_answer import shi_list
from question_and_answer import fou_list


colors = ''
test_image_file = '/Users/zhouguohui/Desktop/Q/test.png'
t = 1
convert_image_file = '/Users/zhouguohui/Desktop/A/covert_image_{x}.png'.format(x='description')
num = 0
record_time = 0

record_d_ratio = []
record_a_ratio = []
def init():
    pass


def pull_screenshot():
    global test_image_file
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    #if sys.platform == 'win32':
    #    screenshot = screenshot.replace(b'\r\n', b'\n')
    f = open(test_image_file, 'wb')
    f.write(screenshot)
    f.close()


def click_random():
    # TODO the click function should be more artificial
    heigh = 830 + int(random.uniform(0, 3)) * 140
    click_cmd = 'adb shell input tap 540 %d' % heigh
    print('click_cmd: %s' % click_cmd)
    p1 = subprocess.Popen(click_cmd, shell=True, stdout=subprocess.PIPE)
    #out, err = p.communicate()
    #for line in out.splitlines():
    #    print(line)


def choice_answer_location(img):
    # TODO need improve the process logical
    #img = Image.open(source)
    im_pixel = img.load()
    w, h = img.size
    blue_pixel = [161, 210, 75, 255]
    red_pixel = [250, 108, 77, 255]
    white_pixel = [253, 253, 254, 255]
    choice_y = []
    Range = 5
    Num = 6
    n = 0
    skip_point_y = int(h / 3)

    # 以20px为步长，从高1/3到4/5处开始遍历，出现蓝色RGB值则判断为正确答案
    for i in range(skip_point_y, int(h * 7 / 8), 20):
        last_pixel = im_pixel[int(w / 5), i]
        # 以2px为步长
        for j in range(int(w / 5), int(w * 4 / 5), 20):
            pixel = im_pixel[j, i]
            # print('RGB:', pixel, j, i)
            # 判断横向为同色线
            if abs(pixel[0] - last_pixel[0]) < Range and \
               abs(pixel[1] - last_pixel[1]) < Range and \
               abs(pixel[2] - last_pixel[2]) < Range:
                if j >= int(w * 4 / 5 - 20) and i >= skip_point_y:
                    #print('---------------------line RGB:%s x:%d y:%d' % (pixel, j, i))
                    for k in range(i, int(h * 19 / 20), 20):
                        vertical_pixel = im_pixel[int(w / 5), k]
                        #print('Debug: **********%s i:%d j:%d k:%d' % (choice_y, i, j, k))
                        if abs(pixel[0] - vertical_pixel[0]) < Range and \
                           abs(pixel[1] - vertical_pixel[1]) < Range and \
                           abs(pixel[2] - vertical_pixel[2]) < Range:
                            n += 1
                            choice_y.append(k)
                        else:
                            #print('Debug: **********%s i:%d j:%d' % (choice_y, i, j))
                            if n >= Num and \
                                    (abs(pixel[0] - red_pixel[0]) < Range and
                                     abs(pixel[1] - red_pixel[1]) < Range and
                                     abs(pixel[2] - red_pixel[2]) < Range):
                                pass
                                #print('================== red choice %s' % choice_y)
                            if n >= Num and \
                                    (abs(pixel[0] - white_pixel[0]) < Range and
                                     abs(pixel[1] - white_pixel[1]) < Range and
                                     abs(pixel[2] - white_pixel[2]) < Range):
                                pass
                                #print('================== white choice %s' % choice_y)
                            if n >= Num and \
                                    (abs(pixel[0] - blue_pixel[0]) < Range and
                                     abs(pixel[1] - blue_pixel[1]) < Range and
                                     abs(pixel[2] - blue_pixel[2]) < Range):

                                #print('================== blue choice %s' % choice_y)
                                return [choice_y[0], choice_y[-1]]
                            n = 0
                            skip_point_y = k
                            choice_y.clear()
                            break

            # 不是纯色的线，准备跳出x循环
            if abs(pixel[0] - last_pixel[0]) >= Range and \
                abs(pixel[1] - last_pixel[1]) >= Range and \
                abs(pixel[2] - last_pixel[2]) >= Range:
                break


def choice_location(img):
    # img = Image.open(source)
    im_pixel = img.load()
    w, h = img.size
    white_pixel = [253, 253, 254, 255]
    choice_y = []
    choice = []
    Range = 5
    Num = 6
    n = 0
    skip_point_y = int(h / 3)

    # 以20px为步长，从高1/3到4/5处开始遍历，出现蓝色RGB值则判断为正确答案
    for i in range(skip_point_y, int(h * 7 / 8), 20):
        pixel = im_pixel[int(w / 5), i]
        if abs(pixel[0] - white_pixel[0]) < Range and \
           abs(pixel[1] - white_pixel[1]) < Range and \
           abs(pixel[2] - white_pixel[2]) < Range:
            # print('---------------------line RGB:%s x:%d y:%d' % (pixel, j, i))
            n += 1
            choice_y.append(i)
        else:
            # 不是纯色的线的点
            if n >= Num:
                choice.append([choice_y[0], choice_y[-1]])
                # print('====== white choice: %s' % choice)
            n = 0
            choice_y.clear()
    return choice


def is_empty(img):
    # TODO need a more effiency way to judge photo is empty or ready to choice
    pass


def convert_image(img, y1):
    #img = Image.open(image_file)
    # TODO use ratio would be better
    w, h = img.size
    box = (100, 659, 980, y1)
    # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    if img.size == (880, y1 - 659):
        Img = img.convert('L')
    else:
        #print('cropping the image...')
        Img = img.convert('L').crop(box)

    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = 100
    table = []
    for i in range(256):
        if i > threshold:
            table.append(0)
        else:
            table.append(1)
    # 图片二值化
    photo = Img.point(table, '1')
    photo.save(convert_image_file, dpi=(300.0, 300.0))
    return Image.open(convert_image_file)


def convert_box_image(img, y1, y2):
    #img = Image.open(image_file)
    # TODO use ratio would be better
    convert_box_image_file = '/Users/zhouguohui/Desktop/A/covert_box_image_{x}_{y}.png'.format(x='choice', y=y1)
    w, h = img.size
    global colors
    #print('Debug: covert box image: y', y1, y2)
    box = (int(w / 5) + 66, y1, int(w * 4 / 5), y2)
    # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    if img.size == (int(w * 3 / 5) - 66, y2 - y1):
        Img = img.convert('L')
    else:
        #print('cropping the box image...')
        Img = img.convert('L').crop(box)

    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = 200
    table = []
    for i in range(256):
        if colors == "black_white":
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        if colors == "white_blue":
            if i > threshold:
                table.append(0)
            else:
                table.append(1)

    # 图片二值化
    photo = Img.point(table, '1')
    photo.save(convert_box_image_file, dpi=(300.0, 300.0))

    return Image.open(convert_box_image_file)


def parse_string(q_string, is_a):
    q_all = {}
    if is_a:
        q_all["answer"] = ''.join(q_string.split('\n'))
        # print('Debug: answer:', q_all['answer'])

        return q_all
    #print(r'%s' % q_string)
    #message = re.compile(r'^第\d题【.{2,}题】\n(.*)\n(.*\n)+', re.DOTALL).search(q_string).group()
    #message = re.compile(r'\n.*\n((.*)\n.*)+', re.DOTALL).search(q_string).group()
    #message = re.compile('^.*\n(.*\n?.*)+', re.DOTALL).search(q_string).group()
    message = re.compile('^.*\n?(.*)+', re.DOTALL).search(q_string).group()
    # q_all["id"] = message[1]
    # q_all["type"] = message[4:6]
    if len(message.split('\n')) >= 2:
        q_all["description"] = ''.join([message.split('\n')[0], message.split('\n')[1]])
    else:
        q_all["description"] = ''.join([message.split('\n')[0]])
    # print('Debug: description:', q_all["description"])
    return q_all


def identify_image(img, is_a=False):
    # return a dict which include the image full info
    # img = Image.open(image_file)
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    text = ''.join(text.split(' '))
    # print(text)
    return parse_string(text, is_a)


def click_answer(y):
    return
    click_cmd = 'adb shell input tap {x} {y}'.format(x=540, y=int((y[0] + y[1]) / 2))
    print(click_cmd)
    process = os.popen(click_cmd)
    output = process.read()
    return output


def compete_string(str_a, str_b):
    import difflib
    seq = difflib.SequenceMatcher(None, str_a, str_b)
    return seq.ratio()


def match_answer(img, database, Y):
    # 获取题目，搜索答案，依次识别选项至找到正确答案
    right_answer = ''
    description = identify_image(convert_image(img, 740), is_a=False)["description"]
    print('Debug: description:', description)

    global record_d_ratio
    global record_a_ratio
    for data in database:
        # how to improve the rule of matching?
        # TODO collect ratio
        #if compete_string(data["description"], description) >= 0.4:
        #    print('data:%s, description:%s, ratio:%f' % (data["description"], description, compete_string(data["description"], description)))
        #    print(data["description"], description)
        if compete_string(data["description"], description) >= 0.7:
        #if description == data["description"]:
            #record_d_ratio.append(compete_string(data["description"], description))
            right_answer = data["answer"]
            #database.remove(data)
            print('================================================> Debug: right_answer:', right_answer)
            break
        if data == database[-1]:
            # how to add the new question
            print('New question not include in database?')
    """
    for y in Y:
        global colors
        global record_time
        colors = "black_white"
        choice_answer = identify_image(convert_box_image(img, y[0], y[1]), is_a=True)["answer"]
        print('  Choice answer:%s y:%s' % (choice_answer, y))
        yes_no = [right_answer, choice_answer]

        # how to improve the rule of matching
        # TODO collect ratio
        if compete_string(right_answer, choice_answer) >= 0.4 or (set(yes_no) < set(shi_list)) or (set(yes_no) < set(fou_list)):
            print('right_answer:%s, choice_answer:%s, ratio:%f' % (right_answer, choice_answer, compete_string(right_answer, choice_answer)))
        # if choice_answer == right_answer or yes_no == shi_list or yes_no == fou_list:
        if compete_string(right_answer, choice_answer) >= 0.76 or (set(yes_no) < set(shi_list)) or (set(yes_no) < set(fou_list)):
            click_answer(y)
            record_time = time.time()
            print('**** Click time %s' % time.asctime())
            return True
        else:
            print('  Choice %s is not the right answer' % y)
    """
    return True


# ----------------for database------------
def collect_data(source):
    # 获取答案坐标，处理图像，获取题目，截取答案，识别答案
    data = {"description": None, "answer": None}
    img = Image.open(source)
    y = choice_answer_location(img)
    data["description"] = identify_image(convert_image(img, 740), is_a=False)["description"]
    # print('---', y)
    global colors
    colors = "white_blue"
    data["answer"] = identify_image(convert_box_image(img, y[0], y[1]), is_a=True)["answer"]
    return data


def create_database():
    database = []
    d_list = []
    for i in range(1, 43):
        data = {}
        data["id"] = i
        image = '/Users/zhouguohui/Desktop/A/A{num}.png'.format(num=i)
        data.update(collect_data(image))
        # print(d_list)
        if i <= 22:
            d_list.append(data["description"])
            database.append(data)
            print(data)
            # print(database)
        else:
            if data["description"] not in d_list:
                d_list.append(data["description"])
                # print('good question image；', data["id"])
                data["id"] = len(d_list)
                os.rename(image, '/Users/zhouguohui/Desktop/A/A{num}.png'.format(num=data["id"]))
                database.append(data)
                print(data)
            #else:
            #    os.remove(image)
            #    print('removed', image)
    print(database)
    #ld = 'database = {database}'.format(database=database)
    #cmd = 'echo -e "{ld}" >> question_and_answer.py'.format(ld=ld)
    #os.system(cmd)
    return database
# ----------------------------------------------


#create_database()
#pull_screenshot()
#source = '/Users/zhouguohui/Desktop/Q/Q1.png'
#convert_image(source)
#print(identify_image(source))
#is_right_answer('/Users/zhouguohui/Desktop/A/A1.png')


def main():
    # Q_image_dir = '/Users/zhouguohui/Desktop/Q'
    # A_image_dir = '/Users/zhouguohui/Desktop/A'
    """
    source = '/Users/zhouguohui/Desktop/Q/Q1.png'
    database = [{'id': 1, 'description': '宝龙达质量管理“三不“政策是(《)。', 'answer': '不接收不合格品、不制作不合格品、不流出不合格品'},
                {'id': 2, 'description': '企业的社会责任是指企业依法经营,不生', 'answer': '叻'}]
    imgg = Image.open(source)
    # print(choice_location(img))
    Y = choice_location(imgg)
    match_answer(imgg, database, Y)
    """
    database = []
    global num
    global record_time
    # database = create_database()
    database = data_list
    Y = []
    input('please enter to start')
    while True:

        pull_screenshot()
        imgg = Image.open(test_image_file)
        #print(abs(Y[0][0] - Y[0][1]) )
        #exit(0)

        while len(choice_location(imgg)) >= 1:
            #if num > 44:
            #   print('d ratio:', record_d_ratio)
            #   print('a ratio', record_a_ratio)
            pull_screenshot()
            imgg = Image.open(test_image_file)
            Y = choice_location(imgg)
            print(len(Y))
            if len(Y) == 1 and abs(Y[0][0] -Y[0][1]) > 260:
                click_answer([1452, 1620])
                time.sleep(2)
            elif 2 <= len(Y) <= 4:
                if match_answer(imgg, database, choice_location(imgg)):
                    break
            else:
                time.sleep(2)



            #if len(choice_location(imgg)) < 2:
            #    time.sleep(1)
        num += 1
        input('Ready on the phone, please input to continue>>>')
        #print('Next question ready time: %s -------------> used %ds' % (time.asctime(), time.time() - record_time ))
        #time.sleep(1)
        #record_time = time.time()



if __name__ == '__main__':
    main()
    # create_database()
