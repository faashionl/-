import matplotlib.pyplot as plt
import xlrd
import pygame
import time
import pandas as pd
from pandas import DataFrame
import os
import btn
import ocrutil
import timeutil
import cv2
#窗体大小
size = 1000, 484
#帧率显示
FPS = 60
#定义背景颜色
DARKBLUE = (73,119,142)
#指定颜色
BG = DARKBLUE
BLAK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (72, 61,139)
GRAY = (96,96,96)
RED = (220,20,60)
YELLOW = (255,255,0)
txt1 = ''
txt2 = ''
txt3 = ''

Total = 100
income_switch = False
#获取文件路径
cdir = os.getcwd()
path = cdir + '/datafile/'
if not os.path.exists(path):
    os.makedirs(path)
    carnfile = pd.DataFrame(columns=['carnumber', 'date', 'price', 'state'])
    carnfile.to_excel(path + '停车场车辆表.xlsx', sheet_name='date')
    carnfile.to_excel(path + '停车场信息表.xlsx', sheet_name='date')
#读取文件内容
pi_table = pd.read_excel(r'D:\360安全浏览器下载\carnumber\datafile\停车场车辆表.xlsx', sheet_name='date')
print(pi_table)
pi_info_table = pd.read_excel(r'D:\360安全浏览器下载\carnumber\datafile\停车场信息表.xlsx', sheet_name='date')
print(pi_info_table)
cars = pi_table[['car number', 'date', 'state']].values
carn = len(cars)
#初始化
pygame.init()
#窗体名设置
pygame.display.set_caption('智能停车场车牌识别系统')
#图标


#设置图标

#设计窗体大小
screen = pygame.display.set_mode(size)
screen.fill(BG)
try:
    cam = cv2.VideoCapture(0)
except:
    print('连接摄像头')

#背景和信息文字
def text0(screen):
    pygame.draw.rect(screen, BG, (650, 2, 350, 640))
    pygame.draw.aaline(screen, GREEN, (662, 50), (980, 50), 1)
    pygame.draw.rect(screen, GREEN, (650, 350, 342, 85), 1)
    xtfont = pygame.font.SysFont('SimHei', 15)
    textstart = xtfont.render('信息', True, GREEN)
    text_rect = textstart.get_rect()
    text_rect.centerx = 675
    text_rect.centery = 365

    screen.blit(textstart,text_rect)


def text1(screen):
    k = Total-carn
    if k<10 :
        sk = '0' + str(k)
    else:
        sk = str(k)
    xtfont = pygame.font.SysFont('SimHei', 20)
    textstart = xtfont.render('共有车位：'+str(Total)+' 剩余车位：'+sk, True,WHITE)
    text_rect = textstart.get_rect()
    text_rect.centerx = 820
    text_rect.centery = 30
    screen.blit(textstart, text_rect)


def text2(screen):
    xtfont = pygame.font.SysFont('SimHei', 15)
    textstart = xtfont.render('车号   时间', True, WHITE)
    text_rect = textstart.get_rect()
    text_rect.centerx = 820
    text_rect.centery = 70
    screen.blit(textstart,text_rect)


def text3(screen):
    xtfont = pygame.font.SysFont('SimHei', 12)
    cars = pi_table[['car number', 'date', 'state']].values
    if len(cars) > 10:
        cars = pd.read_excel(path+'停车场车辆表.xlsx',skiprows=len(cars)-10,sheet_name='date').values
    n = 0
    for car in cars:
        n += 1
        textstart = xtfont.render(str(car[0])+ ' ' + str(car[1]), True, WHITE)
        text_rect = textstart.get_rect()
        text_rect.centerx = 820
        text_rect.centery = 70+ 20*n
        screen.blit(textstart,text_rect)


def text4(screen):
    cars = pi_table[['car number', 'date', 'state']].values
    if len(cars)>0:
        longcar = cars[0][0]
        cartime = cars[0][1]
        xtfont = pygame.font.SysFont('SimHei',15)
        localtime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        htime = timeutil.DtCalc(cartime, localtime)
        textscar = xtfont.render('停车时间最长车辆：' + str(longcar), True, RED)
        texttime = xtfont.render('已停车：'+str(htime) + '小时', True, RED)
        text_rect1 = textscar.get_rect()
        text_rect2 = textscar.get_rect()
        text_rect1.centerx = 820
        text_rect2.centerx = 820
        text_rect1.centery = 320
        text_rect2.centery = 335
        screen.blit(textscar, text_rect1)
        screen.blit(texttime, text_rect2)


def text5(screen,txt1,txt2,txt3):
    xtfont = pygame.font.SysFont('SimHei', 15)

    texttxt1 = xtfont.render(txt1, True, GREEN)
    text_rect = texttxt1.get_rect()
    text_rect.centerx = 820
    text_rect.centery = 355 + 20
    screen.blit(texttxt1, text_rect)

    texttxt2 = xtfont.render(txt2, True, GREEN)
    text_rect = texttxt2.get_rect()
    text_rect.centerx = 820
    text_rect.centery = 355 + 40
    screen.blit(texttxt2, text_rect)

    texttxt3 = xtfont.render(txt3, True, GREEN)
    text_rect = texttxt3.get_rect()
    text_rect.centerx = 820
    text_rect.centery = 355 + 60
    screen.blit(texttxt3, text_rect)

def text6(screen):
    kcar = pi_info_table[pi_info_table['state']==2]
    kcars = kcar['date'].values

    week_number = 0
    for k in kcars:
        week_number = timeutil.get_week_number(k)

    localtime = time.strftime('%Y-%m-%d %H:%M',time.localtime())
    week_localtime = timeutil.get_week_number(localtime)
    if week_number == 0:
        if week_number == 6:
            text7(screen,'根据数据分析，明天可能出现车位紧张')
        elif week_localtime == 0:
            text7(screen,'根据数据分析，明天可能出现车位紧张')
    else:
        if week_localtime +1 == week_number:
            text7(screen,'根据数据分析，明天可能出现车位紧张')
        elif week_localtime == week_number:
            text7(screen,'根据数据分析，明天可能出现车位紧张')
    text7(screen,'根据数据分析，明天可能出现车位紧张')
def text7(screen,week_info):
    pygame.draw.rect(screen,YELLOW,((2,2),(640,40)))
    xtfont = pygame.font.SysFont('SimHei',15)
    textweek_day = xtfont.render(week_info,True,RED)
    text_rect = textweek_day.get_rect()
    text_rect.centerx = 322
    text_rect.centery = 20
    screen.blit(textweek_day,text_rect)

def text8(screen):

    sum_price = pi_info_table['price'].sum()
    xtfont = pygame.font.SysFont('SimHei', 20)
    #获取总收入
    textstart = xtfont.render('共计收入：' + str(int(sum_price))+'元', True, WHITE)

    text_rect = textstart.get_rect()
    text_rect.centerx = 1200
    text_rect.centery = 30
    screen.blit(textstart, text_rect)
    image2 = pygame.image.load(r'D:\360安全浏览器下载\carnumber\file\income.png')
    image2 = pygame.transform.scale(image2, (390, 430))
    screen.blit(image2, (1000, 50))


clock = pygame.time.Clock()


Running = True
while Running:
    sucess,img = cam.read()
    cv2.imwrite('file/test.jpg', img)
    image = pygame.image.load(r'D:\360安全浏览器下载\carnumber\file\test05.jpg')
    image = pygame.transform.scale(image, (640, 480))
    screen.blit(image, (2, 2))

    text0(screen)
    text1(screen)
    text2(screen)
    text3(screen)
    text4(screen)
    text5(screen, txt1, txt2, txt3)
    text6(screen)

    btn.Button(screen, (640, 480), 150, 60, BLUE, WHITE, "识别", 40)
    btn.Button(screen, (640, 120), 100, 40, GREEN, WHITE, "图片选择", 25)

    btn.Button(screen, (990, 480), 100, 40, RED, WHITE, "收入统计", 30)

    if income_switch:
        text8(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()            #退出
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(str(event.pos[0])+':'+str(event.pos[1]))
            if 492 <= event.pos[0] and event.pos[0] <= 642 and 422 <= event.pos[1] and event.pos[1] <= 482:
                print('点击识别')
                try:
                    carnumber = ocrutil.getcn()
                    localtime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                    carsk = pi_table['car number'].values
                    if carnumber in carsk:
                        txt1 = '车牌号：' + carnumber
                        y = 0
                        kcar = 0
                        cars = pi_table[['car number', 'date', 'state']].values
                        for car in cars:
                            if carnumber == car[0]:
                                y = timeutil.DtCalc(car[1], localtime)
                                break
                            kcar = kcar+1
                        if y == 0:
                            y = 1
                        txt2 = '停车费：' + str(3 * y) + '元'
                        txt3 = '出停车场时间：' + localtime

                        pi_table = pi_table.drop([kcar],axis=0)
                        pi_info_table = pi_info_table.append({'car number': carnumber,
                                                              'date': localtime,
                                                              'price': 3 * y,
                                                              'state': 1}, ignore_index=True)
                        DataFrame(pi_table).to_excel(path + '停车场车辆表.xlsx',
                                                     sheet_name='date', index=False, header=True)
                        DataFrame(pi_info_table).to_excel(path + '停车场信息表.xlsx',
                                                     sheet_name='date', index=False, header=True)
                        carn -= 1

                    else:
                        print('输出：'+str(carn))
                        if carn <= Total:
                            pi_table = pi_table.append({'car number': carnumber,
                                                        'date': localtime,
                                                        'state': 0}, ignore_index=True)
                            DataFrame(pi_table).to_excel(path + '停车场车辆表.xlsx',
                                                         sheet_name='date', index=False, header=True)
                            if carn < Total:
                                pi_info_table = pi_info_table.append({'car number': carnumber,
                                                                      'date': localtime,
                                                                      'state': 1}, ignore_index=True)
                                carn += 1
                            else:
                                pi_info_table = pi_info_table.append({'car number': carnumber,
                                                                      'date': localtime,
                                                                      'state': 2}, ignore_index=True)
                            DataFrame(pi_info_table).to_excel(path + '停车场信息表.xlsx',
                                                              sheet_name='date', index=False, header=True)
                            txt1 = '车牌号：' + carnumber
                            txt2 = '有空余车位，可以进入停车场'
                            txt3 = '进停车场时间:' + localtime
                        else:
                            txt1 = '车牌号：' + carnumber
                            txt2 = '没有空余车位，不可以进入停车场'
                            txt3 = '时间:' + localtime

                except Exception as e:
                    print('错误原因：',e)
                    continue
                pass
#收入统计按钮
            if 890<= event.pos[0] and event.pos[0] <= 990 and 440<= event.pos[1] and event.pos[1] <= 480:
                print('收入统计按钮')
                if income_switch:
                    income_switch = False
                    size = 1000, 484
                    screen = pygame.display.set_mode(size)
                    screen.fill(BG)
                else:
                    income_switch = True
                    size = 1500, 484
                    screen = pygame.display.set_mode(size)
                    screen.fill(BG)

                    attr = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
                    v1 = []
                    for i in range(1, 13):
                        k = i
                        if i < 10:
                            k = '0' + str(k)
                        kk = pi_info_table[pi_info_table['date'].str.contains('2023-' + str(k))]
                        kk = kk['price'].sum()
                        v1.append(kk)
                    print(v1)

                    plt.rcParams['font.sans-serif'] = ['SimHei']
                    plt.figure(figsize=(3.9, 4.3))
                    plt.bar(attr, v1, 0.5, color='green')
                    for a, b in zip(attr, v1):
                        plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=7)
                    plt.title('每月收入统计')
                    plt.ylim((0, max(v1) + 50))
                    plt.savefig(r'D:\360安全浏览器下载\carnumber\file\income.png')
                pass
            #图片选择
            if  540<= event.pos[0] and event.pos[0] <= 640 and 80 <= event.pos[1] and event.pos[1] <= 120:
                print('图片选择')

    pygame.display.flip()
    clock.tick(FPS)

