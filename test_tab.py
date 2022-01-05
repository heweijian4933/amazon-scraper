from selenium import webdriver

# chromedriver的绝对路径
driver_path = r'D:/Program Files/Python/python36/Lib/site-packages/chromedriver.exe'

# 初始化一个driver，并且指定chromedriver的路径
driver = webdriver.Chrome(executable_path=driver_path)

# 请求网页
driver.get("https://www.baidu.com/")

driver.execute_script("window.open('https://www.taobao.com')")

# 打印窗口句柄
print(driver.window_handles)

# 切换窗口
driver.switch_to.window(driver.window_handles[1])

print(driver.current_url)
print(driver.page_source)

# 虽然在窗口中切换到了新的页面，但是driver中还没切换
# 如果想要在代码中切换到新的页面，并爬取页面，那么应该使用driver.switch_to.window来切换到指定的窗口
# 从driver.window_handles中取出具体是 第几个窗口
# driver.window_handles是一个列表，里边存储的是窗口句柄。他会按照打开的顺序来存储窗口句柄
