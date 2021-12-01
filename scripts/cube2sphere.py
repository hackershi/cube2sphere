#coding=utf-8
import os,json,subprocess, time, shutil
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed

cwd =  Path(__file__).parents[0]
config_data = json.load(open(cwd/"config.json", 'r'))

width = config_data['width']
height = config_data['height']
img_dirs = config_data['image_dirs']
process_num = config_data['process_num']

start_index = int(config_data['start_index'])
end_index = int(config_data['end_index'])


def process_task(back_name, main_name, right_name, left_name, top_name, down_name, out_name):
    global width, height
    cmd_string = rf'cube2sphere {back_name}  {main_name} {right_name} {left_name}  {top_name} {down_name} -r {width} {height} -fPNG -o  {out_name} -t 5 -R 0 0 180 '
    cmd = cmd_string.split()
    try:
        subprocess.run(cmd)
        os.rename(f'{out_name}0001.png', f'{out_name}')
    except:
        print(f"{back_name} failed")


if __name__ == '__main__':
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
        if end_index == -1 or end_index > len(files):
            end_index = len(files)
        file_names = [x.name for x in files]
        file_names.sort()        
        file_names = file_names[start_index:end_index]

        out_dir_idx = 0
        out_dir = rf'{img_dir}\out_{out_dir_idx:03d}'
        while os.path.exists(out_dir):
            out_dir_idx += 1
            out_dir = rf'{img_dir}\out_{out_dir_idx:03d}'

        start_time = time.time()
        futures = []
        with ProcessPoolExecutor(max_workers=process_num) as executor:
            for idx,file_name in enumerate(file_names):
                back_name = rf'{back_folder}\{file_name}'
                down_name = rf'{down_folder}\{file_name}'
                left_name = rf'{left_folder}\{file_name}'
                main_name = rf'{main_folder}\{file_name}'
                right_name = rf'{right_folder}\{file_name}'
                top_name = rf'{top_folder}\{file_name}'
                out_name = rf'{out_dir}\{file_name}'

                names = [back_name, main_name, top_name, down_name, left_name, right_name]
                ok = True
                for name in names:
                    if not os.path.exists(name):
                        print(f"{name} not exist")
                        ok = False

                if not ok:
                    continue

                futures.append(executor.submit(process_task,back_name, main_name, right_name, left_name, top_name, down_name, out_name))
            
            cnt = 0
            for future in as_completed(futures):
                cnt += 1
                print(cnt, end = (',' if cnt%10!=0 else "\n"))


        total_time = time.time() - start_time
        print(f"time {total_time:0.2f} seconds")
