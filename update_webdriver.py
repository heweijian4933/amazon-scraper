import os
import re
import sys
import winreg
import zipfile
from pathlib import Path
import requests
from win32com.client import *


# python_root = Path(sys.executable).parent  # python安装目录
python_root = os.path.join(os.getcwd(), 'tool')
base_url = 'http://npm.taobao.org/mirrors/chromedriver/'  # chromedriver在国内的镜像网站
version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本信息


def get_version_number(file_path):
      
    information_parser = Dispatch("Scripting.FileSystemObject")
    version = information_parser.GetFileVersion(file_path)
    return version


def get_chrome_version():
    """通过注册表查询Chrome版本信息: HKEY_CURRENT_USER\SOFTWARE\Google\Chrome\BLBeacon: version"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             'SOFTWARE\Google\Chrome\BLBeacon')
        value = winreg.QueryValueEx(key, 'version')[0]
        return version_re.findall(value)[0]
    except WindowsError as e:
        print("没有安装Chrome浏览器")
        return '0.0.0'  # 没有安装Chrome浏览器


def get_chrome_driver_version():
    """ try:
        result = os.popen('chromedriver --version').read()
        version = result.split(' ')[1]
        return '.'.join(version.split('.')[:-1])
    except Exception as e:
        print("没有安装ChromeDriver")
        return '0.0.0'  # 没有安装ChromeDriver """
    try:
        chromedriver_path = os.path.join(python_root, 'chromedriver.exe')
        print(chromedriver_path)
        print(get_version_number(chromedriver_path))
        version = ".".join(get_version_number(chromedriver_path))
        return version
    except:
        print("没有安装ChromeDriver")
        return '0.0.0'  # 没有安装ChromeDriver """


def get_latest_chrome_driver(chrome_version):
    url = f'{base_url}LATEST_RELEASE_{chrome_version}'
    latest_version = requests.get(url).text
    download_url = f'{base_url}{latest_version}/chromedriver_win32.zip'
    print('正在下载{}'.format(download_url))
    # 下载chromedriver zip文件
    response = requests.get(download_url)
    # local_file = python_root / 'chromedriver.zip'
    local_file = os.path.join(python_root,'chromedriver.zip')
    with open(local_file, 'wb') as zip_file:
        zip_file.write(response.content)

    # 解压缩zip文件到python安装目录
    try:
        print('正在解压{}'.format(local_file))
        f = zipfile.ZipFile(local_file, 'r')
        for file in f.namelist():
            f.extract(file, python_root)
        f.close()

        # local_file.unlink()  # 解压缩完成后删除zip文件
        os.remove(local_file)
    except Exception as e:
        print(e)
        print("解压失败或者没有权限")
        pass


def check_chrome_driver_update():
    chrome_version = get_chrome_version()
    print("chrome浏览器版本", chrome_version)
    driver_version = get_chrome_driver_version()
    print("webdriver版本", driver_version)
    if chrome_version == driver_version:
        print('No need to update')
    else:
        try:
            get_latest_chrome_driver(chrome_version)
        except Exception as e:
            print(f'Fail to update: {e}')


if __name__ == '__main__':
    check_chrome_driver_update()
