import os
from colorama import init, Fore, Style # type: ignore
import shutil
import glob
import json

def save_buffer(filtereds_dir, buffers, name):
    if len(buffers[name]) <= 0:
        return

    os.makedirs(filtereds_dir, exist_ok=True)
    output_file_path =  os.path.join(filtereds_dir, f"{name}.jsonl")
    mode = "a" if os.path.exists(output_file_path) else "w"
    with open(output_file_path, mode, encoding="utf-8") as f:
        for item in buffers[name]:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            buffers[name] = []
    pass

def filter_meta():
    print("*** AMAZON FILTER META DATA ***")
    base_dir = os.path.join(os.getcwd(),"_outputs","amazon")
    jsonl_dir = os.path.join(base_dir,"jsonls")
    if not os.path.exists(jsonl_dir):
        return
    
    filtereds_dir = os.path.join(base_dir,"filtereds")
    if os.path.exists(filtereds_dir):
        shutil.rmtree(filtereds_dir)
    
    null_values = ["None","","nil","null"]
    buffers = {}

    for json_file in glob.glob(f"{jsonl_dir}/*.jsonl"):
        print(json_file)
        input_file = open(json_file, 'r', encoding='utf-8')
        for line in input_file:
            try:
                jsondata = json.loads(line)
                sub_categories = jsondata.get("categories", None)
                main_category = sub_categories[0].strip().replace("\"","").title()
                sub_category = ">".join(sub_categories).strip()
                title = jsondata.get("title", None).strip()
                features = ". ".join(jsondata.get("features", None)).strip()
                description = ". ".join(jsondata.get("description", None)).strip()
                image = jsondata.get("images",None)[0]["large"].strip()
               
                if main_category in null_values: continue
                if sub_category in null_values: continue
                if title in null_values: continue
                if features in null_values: continue
                if description in null_values: continue
                if image in null_values: continue

                features = features.replace(".. ",". ")
                description = description.replace(".. ",". ")

                item = {
                    "main_category": main_category,
                    "sub_category" : sub_category,
                    "title" : title,
                    "features" : features,
                    "description" : description,
                    "image": image
                }

                if main_category not in buffers:
                    buffers[main_category] = []

                buffers[main_category].append(item)
                if len( buffers[main_category] ) > 10000:
                    save_buffer(filtereds_dir, buffers, main_category)

            except Exception as e:
                # print(e)
                pass

        pass

    for main_category, buffer in buffers.items():
        if len(buffers[main_category]) > 0:
            save_buffer(filtereds_dir, buffers, main_category)
    pass

if __name__ == "__main__":
    filter_meta()
    # init(autoreset=True)
    # main()
    pass