#coding=utf-8
import os,json,subprocess, time, shutil
from pathlib import Path

cwd =  Path(__file__).parents[0]
config_data = json.load(open(cwd/"config.json", 'r'))

width = config_data['width']
height = config_data['height']
img_dirs = config_data['image_dirs']
thread_num = config_data['thread_num']



for img_dir in img_dirs:
    main_folder = ""
    back_folder = ""
    left_folder = ""
    right_folder = ""
    top_folder = ""
    down_folder = ""

    img_dir = Path(img_dir)
    folders = list(img_dir.iterdir())

    for folder in folders:
        if "main" in str(folder):
            main_folder = folder
        if "back" in str(folder):
            back_folder = folder
        if 'top' in str(folder):
            top_folder = folder
        if "down" in str(folder):
            down_folder = folder
        if "left" in str(folder):
            left_folder = folder
        if "right" in str(folder):
            right_folder = folder

    if main_folder == "" or back_folder == "" or left_folder == "" or right_folder == "" or top_folder == "" or down_folder == "":
        print(f"folder {img_dir} folder not complete:[main, back, left, right, top, down]")
        continue


    files = list((img_dir/main_folder).iterdir())
    file_names = [x.name for x in files]


    out_dir = rf'{img_dir}\out'
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    start_time = time.time()
    for idx,file_name in enumerate(file_names):
        back_name = rf'{back_folder}\{file_name}'
        down_name = rf'{down_folder}\{file_name}'
        left_name = rf'{left_folder}\{file_name}'
        main_name = rf'{main_folder}\{file_name}'
        right_name = rf'{right_folder}\{file_name}'
        top_name = rf'{top_folder}\{file_name}'
        
        names = [back_name, main_name, top_name, down_name, left_name, right_name]
        for name in names:
            if not os.path.exists(name):
                raise Exception(f"{name} not exist")

        out_name = rf'{out_dir}\{file_name}'
        cmd_string = rf'cube2sphere {back_name}  {main_name} {right_name} {left_name}  {top_name} {down_name} -r {width} {height} -fPNG -o  {out_name} -t {thread_num} -R 0 0 180 '
        cmd = cmd_string.split()
        subprocess.run(cmd)
        os.rename(f'{out_name}0001.png', f'{out_name}')
        print(idx, end = (',' if idx%10!=9 else "\n"))

    total_time = time.time() - start_time
    print(f"time {total_time:0.2f} seconds")
