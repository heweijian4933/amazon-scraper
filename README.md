# 关于

**关键词**在电商平台的SEO中发挥着极为重要的作用, 一个精准的关键词有的时候能够为商品带来许多意想不到的流量. 尽管现在各大电商平台的流量竞争非常激烈, 各个商家对于关键词的覆盖度相比十年前都已经非常完善. 但关键词依然是发布产品前需要做好的工作.

基于以上背景, 我开发了一个用于自动爬取亚马逊商品信息的爬虫, 方便后续做商品关键词筛选.

# 项目目录

```
|-amazon-keword-scraper //通过virtualenv建立的虚拟环境
|-build //pyinstaller的打包中间文件
|-dist //pyinstaller打包好的文件
|-tool //通过脚本运行时,脚本自动下载chromedriver.exe的所在目录
|-gui.py //gui运行的主脚本
|-scraper.py //selenium运行并爬取数据的模块, 是项目的主要业务模块
|-update_webdriver.py //selenium运行前首先检查是否安装了google chrome浏览器和chromedriver(并更新)的模块
```



# 运行依赖

> 需要提前安装好Chrome浏览器

运行方式

1. 直接运行已经打包好的exe文件:
   
   文件目录./build/gui.exe
   **exe文件复制到其他电脑使用的时候需要连同./build/tool文件夹一起复制**

2. 通过脚本运行
 ```terminal终端/powershell
   //激活虚拟环境(命令行运行时请勿带注释)
   amazon-keword-scraper\Scripts\activate
   
   python gui.py
 ```

# 使用的技术

python + selenium + pysimplegui + requests

selenium用于模拟人为浏览操作

requests用在自动更新chromedriver.exe文件的模块中. 因chrome浏览器经常自动更新, 而手动维护selenium的必须依赖chromedriver.exe这个工作就会变得很麻烦, 所以为了方便操作, 脚本会自动检测系统是否安装了chrome浏览器和chromedriver, 并且自动下载最新的chromedriver

pysimplegui 用于制作gui界面方便用户交互

打包工具采用pyinstaller

# 效果展示

![image-20220105140852214](https://s2.loli.net/2022/01/05/Gd6IMgafwYZLJQj.png)



# 其他

pyinstaller 打包以后的exe文件在自动运行时会启动chromedriver的console控制台,为了隐藏该控制台改善用户体验, 需要做如下配置:

修改源码：Lib \ site-packages \ selenium \ webdriver \ common \ services.py

找到start()，如下图，添加配置参数 **creationflags=134217728** 即可

![image-20220105141430560](https://s2.loli.net/2022/01/05/yrGInKFS5VPwjTx.png)

> 方法来自：[https://stackoverflow.com/questions/33983860/hide-chromedriver-console-in-python?rq=1](https://stackoverflow.com/questions/33983860/hide-chromedriver-console-in-python?rq=1)