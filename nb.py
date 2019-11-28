import os
scripts_path="/home/ops/ib-apps/apps/"
file_list = []
for root,dirs,files in os.walk(scripts_path):
    if files:
            for file in files:
                if file.startswith("version"):
                    file_list.append(file)

