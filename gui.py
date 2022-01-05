
import update_webdriver as updateWebdriver
from datetime import datetime
import PySimpleGUI as sg
import os,re

''' 检查电脑是否装了chrome浏览器和webdriver '''
updateWebdriver.check_chrome_driver_update()

import scraper as getAmazonKeywords
# 查看所有主题
# sg.preview_all_look_and_feel_themes()
# 切换主题
sg.change_look_and_feel("GreenMono")

keyword_text = sg.Text("请输入要查询的关键词")
keyword_textinput = sg.InputText()

page_text = sg.Text("请输入要查询该关键词亚马逊前几页")
page_textinput = sg.InputText()

save_text = sg.Text("请选择保存路径")
save_textinput = sg.FolderBrowse()

notice_text = sg.Text("查询美国亚马逊站点前请记得打开vpn并打开全局模式",text_color="red")
loading_text = sg.Text("正在查询中...",text_color="yellow",key="_loading_",visible = False)


bt = sg.Button('查询')
cbt = sg.Button('取消')
layout = [[keyword_text, keyword_textinput],
          [page_text, page_textinput], 
          [save_text, save_textinput], 
          [sg.Radio('隐藏浏览器(后台运行)', 'num', default=True) ,
           sg.Radio('显示浏览器(前台运行)', 'num')],
          [notice_text],
          [sg.pin(loading_text)],
          [bt, cbt]]

window = sg.Window('亚马逊关键词查询工具', layout)


while True:
    event, values = window.read()
    if event in (None, '取消'):
        break
    # print(f'Event: {event}')  # 这里的f是用来把事件按钮名称写出来
    # print(str(values))
    # print(values)
    keyword, page, save_path,option1,option2 = values.values()
    print( keyword, page, save_path,option1,option2)
    keyword = keyword.strip()
    if (keyword == None) or (keyword == ''):
        sg.popup('请输入关键词')
        continue

    try:
        page = int(page)
        if page > 30:
            sg.popup('页数较多时需要耗费的时间会比较长,请耐心等待')
        elif page <= 0:
            sg.popup('页数应该大于0')
    except:
        sg.popup('请输入合法的页数')
        continue

    if ((keyword == None) or (keyword == '')) or ( page <= 0 ):
        continue
    save_path = save_path.strip()
    save_folder = save_path
    print(save_path)
   
    alternative_path = ''
    if re.match('(?:[A-Z]:|\\\\|(?:\\.{1,2}[\\/\\\\])+)[\\w+\\\\\\s_\\(\\)\\/]+(?:\\.\\w+)*',save_path): 
        #说明能够匹配到文件路径
        now = datetime.now()
        save_path = os.path.join(save_path,'keywords-{}.csv'.format(now.strftime("%Y-%m-%d %H-%M-%S")))
        alternative_path = save_path
    else:
        now = datetime.now()
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        save_path = os.path.join(desktop,'keywords-{}.csv'.format(now.strftime("%Y-%m-%d %H-%M-%S")))
        alternative_path = os.path.join('桌面','keywords-{}.csv'.format(now.strftime("%Y-%m-%d %H-%M-%S")))
    print(keyword, page,save_path)

    window['_loading_'].Update(visible=True)
    window['_loading_'].Update('正在查询中,请耐心等待...')
    getAmazonKeywords.main(keyword,page,save_path,option1)
   
    window['_loading_'].Update(visible=True)
    window['_loading_'].Update('查询完毕请查看文件=> {}'.format(alternative_path))
    os.startfile(save_folder)

getAmazonKeywords.closeBrowser()
window.close()

# pyinstaller E:\pycharmdir\script-amazon-scraper\gui.py -F -w