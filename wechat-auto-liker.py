import os
import time
import pyautogui
import pygetwindow as gw
from pynput import keyboard  # 用于手动停止程序

# 停止标志
stop_script = False
processed_locations = []  # 已处理评论按钮的位置列表

def on_press(key):
    global stop_script
    if key == keyboard.Key.esc:  # 按下 `ESC` 键时停止
        stop_script = True
        print("手动停止程序。")
        return False  # 停止监听器

def open_wechat_and_maximize():
    # 打开 WeChat 程序
    wechat_path = r"C:\Program Files\Tencent\WeChat\WeChat.exe"  # 替换为你的 WeChat 安装路径
    os.startfile(wechat_path)

    # 等待 WeChat 程序启动
    time.sleep(5)  # 根据电脑性能调整等待时间

    # 查找 WeChat 窗口并最大化
    for window in gw.getAllTitles():
        if "WeChat" in window or "微信" in window:  # 支持英文或中文标题
            wechat_window = gw.getWindowsWithTitle(window)[0]
            if not wechat_window.isMaximized:  # 确保窗口没有被最大化
                wechat_window.maximize()  # 最大化窗口
            return wechat_window
    return None

def click_friend_circle():
    # 通过图像识别查找朋友圈图标并点击
    friend_circle_image_path = r"C:\Users\80959\Desktop\test\pyq.png"  # 替换为朋友圈图标截图路径
    
    # 使用图像识别找朋友圈图标
    location = pyautogui.locateOnScreen(friend_circle_image_path, confidence=0.8)
    if location:
        center = pyautogui.center(location)
        print(f"朋友圈图标位置: {center.x}, {center.y}")  # 打印调试信息
        pyautogui.click(center.x, center.y)
        print(f"点击了朋友圈图标: {center.x}, {center.y}")
        time.sleep(2)  # 等待朋友圈加载完成
    else:
        print("未找到朋友圈图标，请检查截图是否准确。")

def click_top_button():
    # 定位并点击朋友圈置顶按钮
    top_button_image_path = r"C:\Users\80959\Desktop\test\zd.png"  # 替换为置顶按钮截图路径
    location = pyautogui.locateOnScreen(top_button_image_path, confidence=0.8)
    if location:
        center = pyautogui.center(location)
        pyautogui.click(center.x, center.y)
        print("置顶按钮已点击...")
        time.sleep(1)  # 等待朋友圈刷新
    else:
        print("未找到置顶按钮，请检查截图或页面状态。")

def is_location_processed(location):
    """检查评论按钮的位置是否已处理过"""
    for loc in processed_locations:
        if abs(loc[0] - location[0]) < 10 and abs(loc[1] - location[1]) < 10:  # 判断是否接近
            return True
    return False

def find_and_like_comments():
    global stop_script
    while not stop_script:  # 循环直到手动停止
        # 先下滑页面一段距离，准备查找评论按钮
        print("下滑页面...")
        
        # 确保鼠标位置在页面可滚动区域
        pyautogui.moveTo(989, 405)  # 移动鼠标到页面中间或其他位置
        pyautogui.scroll(-800)  # 增大滚动幅度，确保有效滚动
        time.sleep(2)  # 等待页面加载

        # 定位评论按钮
        comment_image_path = r"C:\Users\80959\Desktop\test\pl.png"  # 替换为评论按钮截图路径
        location = pyautogui.locateOnScreen(comment_image_path, confidence=0.7)  # 调低confidence，增加容错性
        if location:
            # 获取评论按钮中心位置
            center = pyautogui.center(location)
            print(f"评论按钮位置: {center.x}, {center.y}")  # 打印调试信息

            # 检查是否已处理过
            if not is_location_processed((center.x, center.y)):
                # 点击评论按钮
                pyautogui.click(center.x, center.y)
                print(f"点击评论按钮: {center.x}, {center.y}")
                time.sleep(0.8)  # 减少等待时间

                # 优先定位点赞按钮
                like_image_path = r"C:\Users\80959\Desktop\test\dz.png"  # 替换为点赞按钮截图路径
                like_location = pyautogui.locateOnScreen(like_image_path, confidence=0.8)
                if like_location:
                    # 如果是点赞按钮，点击它
                    like_center = pyautogui.center(like_location)
                    pyautogui.click(like_center.x, like_center.y)
                    print(f"点击点赞按钮: {like_center.x}, {like_center.y}")
                    time.sleep(0.8)  # 减少等待时间
                else:
                    pyautogui.scroll(-800)
                    print("未找到点赞按钮，继续下滑。")

                # 记录已处理的评论按钮位置
                processed_locations.append((center.x, center.y))
            else:
                pyautogui.scroll(-800)
                print("已处理过的评论按钮，跳过。")
        else:
            pyautogui.scroll(-800)
            print("未找到评论按钮，继续下滑。")
        
        # 每次处理完一个评论后继续下滑并查找下一个
        pyautogui.scroll(-800)  # 增加滚动距离，继续查找新的评论按钮
        time.sleep(2)  # 等待页面加载

def main():
    # 启动手动停止监听器
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # 打开 WeChat 并最大化
    wechat_window = open_wechat_and_maximize()
    if wechat_window:
        # 点击朋友圈功能
        click_friend_circle()
        # 点击置顶按钮
        click_top_button()
        # 查找评论按钮并点赞
        find_and_like_comments()
    else:
        print("未找到 WeChat 窗口，请确保程序已正确启动。")

if __name__ == "__main__":
    main()