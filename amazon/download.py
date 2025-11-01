import os
from colorama import init, Fore, Style # type: ignore
from huggingface_hub import list_repo_files, hf_hub_download
import shutil


def get_ignores() -> list[str]:
    ignore_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"ignore_download.txt")
    if not os.path.exists(ignore_file):
        return []
    
    ignore_files = []
    try:
        with open(ignore_file,"r", encoding="utf-8") as f:
            for line in f:
                if line:
                    ignore_files.append(line.strip())

    except Exception as e:
        pass
    return ignore_files

def remove_temp(jsonl_dir):
    # Remove cache folders
    need_remove_dirs = [
        os.path.join(jsonl_dir, ".locks"),
        os.path.join(jsonl_dir, "datasets--McAuley-Lab--Amazon-Reviews-2023")
    ]

    for dir in need_remove_dirs:
        if os.path.exists(dir):
            try:
                shutil.rmtree(dir)
            except Exception as e:
                print(e)
                pass

def main():
    repo_id = "McAuley-Lab/Amazon-Reviews-2023"
    files = list_repo_files(repo_id, repo_type="dataset")

    print("*** AMAZON HUGGINGFACE DATA DOWNLOADER ***")
    # parts = []
    # parts.append("raw/meta_categories")

    current_dir = os.getcwd()
    base_dir = os.path.join(current_dir,"_outputs","amazon")
    jsonl_dir = os.path.join(base_dir,"jsonls")
    os.makedirs(jsonl_dir, exist_ok=True)
    
    ignores = get_ignores()

    plans = {}

    file_start_withs = "raw/meta_categories/meta_"
    for file in files:
        if not file.lower().startswith(file_start_withs):
            continue

        file_name = file[len(file_start_withs):]
        if file_name in ignores or file_name.replace(".jsonl","") in ignores:
            continue

        plans[file_name] = file

    print("Plan to download:")
    for file_name, link in plans.items():
        print(Fore.CYAN + file_name + Style.RESET_ALL)


    for file_name, link in plans.items():
        output_file = os.path.join(jsonl_dir, file_name)
        print(output_file)
        if os.path.exists(output_file):
            remove_temp(jsonl_dir)
            continue

        try:
            local_path = hf_hub_download(repo_id, link, repo_type="dataset", cache_dir=jsonl_dir)
            shutil.move(local_path, output_file)
            print(local_path)
            pass
        except Exception as e:
            print(e)
            pass
        
        remove_temp(jsonl_dir)

       

            
if __name__ == "__main__":
    init(autoreset=True)
    main()
    pass