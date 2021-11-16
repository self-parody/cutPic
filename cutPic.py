import cv2
import tkinter as tk
from tkinter import ttk
import threading
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import os
import time
import numpy as np

root = tk.Tk()
root.title('批量裁剪图片')
root.geometry('450x350+500+100')
root.resizable(False, False)
tip=tk.Label(root,text='注意：路径、文件名中不能含有中文！',bg='#FFE4E1')
tip.place(x=10,y=5)

# 变量组件
img_path = tk.StringVar()
save_path = tk.StringVar()
top_width=tk.StringVar()
top_height=tk.StringVar()
middle_width=tk.StringVar()
middle_height=tk.StringVar()
bottom_width=tk.StringVar()
bottom_height=tk.StringVar()
pb_value=tk.StringVar()

#进度条组件
pb = ttk.Progressbar(root, length = 140, value = 0, mode = "determinate")

# 路径选择功能
def select_img_path(event):
    temp_path = askdirectory()
    img_path.set(temp_path)

def select_save_path(event):
    temp_path = askdirectory()
    save_path.set(temp_path)

# 提交功能
def submit_path(event):
    # 存储输入值
    global img_path_value,save_path_value,top_width_value,top_height_value,middle_width_value,middle_height_value,bottom_width_value,bottom_height_value
    img_path_value=img_path.get()
    save_path_value=save_path.get()
    top_width_value=top_width.get()
    top_height_value=top_height.get()
    middle_width_value = middle_width.get()
    middle_height_value = middle_height.get()
    bottom_width_value = bottom_width.get()
    bottom_height_value = bottom_height.get()

    if(img_path_value=='' or save_path_value=='' or top_width_value=='' or top_height_value=='' or middle_width_value=='' or middle_height_value=='' or bottom_width_value=='' or bottom_height_value==''):
        tk.messagebox.showwarning('Warning', '路径选择和尺寸输入不能为空')
    else:

        start_thread()  # 在子线程中进行裁剪功能，解决窗体长时间无响应的问题
        pb.place(x=150, y=300)  # 显示进度条
        pb_start()
        tk.messagebox.showinfo('Message', '成功!')
        close_window() # 关闭所有窗口

def start_thread(): # 运行裁剪功能的子线程
    insert_data = threading.Thread(target=cut_picture)
    insert_data.start()

def pb_start(): # 进度条动画
    if(img_path_value):
        file_num = len(os.listdir(img_path_value))
        pb["maximum"] = file_num
        for i in range(file_num):
            pb["value"] = i + 1
            root.update()
            time.sleep(0.05)
    else:
        return

# 输入路径的相关组件
img_path_info = tk.Label(root, text='选择图片路径',bg='#B0C4DE')
img_path_info.place(x=10, y=50)
path_input = tk.Entry(root, textvariable=img_path)
path_input.place(x=120, y=50, width='200')
select_btn1 = tk.Button(root, text='select',bg='#6495ED')
select_btn1.place(x=350, y=48)
select_btn1.bind('<Button-1>', select_img_path)

save_path_info = tk.Label(root, text='选择结果保存路径',bg='#B0C4DE')
save_path_info.place(x=10, y=100)
save_path_input = tk.Entry(root, textvariable=save_path)
save_path_input.place(x=120, y=100, width='200')
select_btn3 = tk.Button(root, text='select',bg='#6495ED')
select_btn3.place(x=350, y=98)
select_btn3.bind('<Button-1>', select_save_path)

cutsize_info=tk.Label(root,text='输入裁剪尺寸',bg='#B0C4DE')
cutsize_info.place(x=10,y=150)

top_info=tk.Label(root,text='上（宽*高）')
top_info.place(x=100,y=150)
top_width_input=tk.Entry(root,textvariable=top_width)
top_width_input.place(x=170,y=150,width=50)
top_height_input=tk.Entry(root,textvariable=top_height)
top_height_input.place(x=230,y=150,width=50)

middle_info=tk.Label(root,text='中（宽*高）')
middle_info.place(x=100,y=180)
middle_width_input=tk.Entry(root,textvariable=middle_width)
middle_width_input.place(x=170,y=180,width=50)
middle_height_input=tk.Entry(root,textvariable=middle_height)
middle_height_input.place(x=230,y=180,width=50)

bottom_info=tk.Label(root,text='下（宽*高）')
bottom_info.place(x=100,y=210)
bottom_width_input=tk.Entry(root,textvariable=bottom_width)
bottom_width_input.place(x=170,y=210,width=50)
bottom_height_input=tk.Entry(root,textvariable=bottom_height)
bottom_height_input.place(x=230,y=210,width=50)

submit_path_btn = tk.Button(root, text='submit',font=('Arial',12), bg='#6495ED')
submit_path_btn.place(x=170, y=260, width='100')
submit_path_btn.bind('<Button-1>', submit_path)

#解决读取文件路径中有中文时的报错问题
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img

# 裁剪功能
def cut_picture():
    print(img_path_value)
    for filename in os.listdir(img_path_value):
        top_filename = os.path.splitext(filename)[0] + '_1' + os.path.splitext(filename)[-1]
        middle_filename = os.path.splitext(filename)[0] + '_2' + os.path.splitext(filename)[-1]
        bottom_filename = os.path.splitext(filename)[0] + '_3' + os.path.splitext(filename)[-1]

        file=img_path_value + '/' + filename
        img=cv_imread(file)
        # img = cv2.imread(file)
        # print(img.shape)
        # 分别进行上、中、下裁剪，并创建相应文件夹，将剪裁后的图片分别写入
        top_width_num=int(top_width_value)
        top_height_num = int(top_height_value)
        middle_width_num=int(middle_width_value)
        middle_height_num = int(middle_height_value)
        bottom_width_num = int(bottom_width_value)
        bottom_height_num = int(bottom_height_value)

        cropped_top = img[0:top_height_num, 0:top_width_num]  # 裁剪坐标为[y0:y1, x0:x1]
        cropped_middle = img[top_height_num:top_height_num + middle_height_num, 0:middle_width_num]
        cropped_bottom = img[top_height_num + middle_height_num:top_height_num + middle_height_num+bottom_height_num, 0:bottom_width_num]

        top_dir=save_path_value + '/top'
        middle_dir=save_path_value + '/middle'
        bottom_dir=save_path_value + '/bottom'
        if not os.path.exists(top_dir):
            os.makedirs(top_dir)
        if not os.path.exists(middle_dir):
            os.makedirs(middle_dir)
        if not os.path.exists(bottom_dir):
            os.makedirs(bottom_dir)
        # cv2.imwrite(top_dir + '/' + top_filename, cropped_top)

        #解决写入文件的路径有中文时报错的问题
        cv2.imencode('.jpg', cropped_top)[1].tofile(top_dir + '/' + top_filename)
        cv2.imencode('.jpg', cropped_middle)[1].tofile(middle_dir + '/' + middle_filename)
        cv2.imencode('.jpg', cropped_bottom)[1].tofile(bottom_dir + '/' + bottom_filename)

def close_window():
    root.destroy()
root.protocol('WM_DELETE_WINDOW', close_window)  # 点击窗体按钮x则关闭程序

root.mainloop()
