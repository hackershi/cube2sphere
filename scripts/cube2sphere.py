import os
from pathlib import Path
import subprocess, time


# Opens the Video file
file_dir = Path(r"E:\1117\2021-11-17_17-03-42\back_cam_v03")
files = list(file_dir.iterdir())
file_names = [x.name for x in files]

folder_path = r"E:\1117\2021-11-17_17-03-42"
folder_name = ['back_cam_v03',
 'down_cam_v03',
 'left_cam_v03',
 'main_cam_v03',
 'right_cam_v03',
 'top_cam_v03',
 ]

outdir = r"synthesis"

start_time = time.time()
for idx,file_name in enumerate(file_names):
    back_name = rf'{folder_path}\{folder_name[0]}\{file_name}'
    down_name = rf'{folder_path}\{folder_name[1]}\{file_name}'
    left_name = rf'{folder_path}\{folder_name[2]}\{file_name}'
    main_name = rf'{folder_path}\{folder_name[3]}\{file_name}'
    right_name = rf'{folder_path}\{folder_name[4]}\{file_name}'
    top_name = rf'{folder_path}\{folder_name[5]}\{file_name}'
    out_name = rf'{folder_path}\{outdir}\{file_name}'
    cmd_string = rf'cube2sphere {back_name}  {main_name} {right_name} {left_name}  {top_name} {down_name} -r 4096 2048 -fPNG -o  {out_name} -t 20 -R 0 0 180 '
    cmd = cmd_string.split()
    subprocess.run(cmd)
    os.rename(f'{out_name}0001.png', f'{out_name}')
    print(idx, end = (',' if idx%5!=4 else "\n"))

total_time = time.time() - start_time
print(f"total time {total_time} seconds")
