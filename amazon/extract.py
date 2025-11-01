import os
import io
import glob
from colorama import init, Fore, Style # type: ignore
import shutil
import json

def create_db(path):
    import sqlite3
    if os.path.exists(path):
        os.remove(path)

    if not os.path.exists(path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                main_category TEXT NOT NULL,
                features TEXT NOT NULL,
                description TEXT NOT NULL,
                image TEXT NOT NULL
            )
            """)
        conn.commit()
        conn.close()
    pass

def save_to_db(path, data):
    import sqlite3
    if not os.path.exists(path):
        return
    
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO Products 
        (title, main_category, features, description, image) 
        VALUES (:title, :main_category, :features, :description, :image)""", 
        data)
    conn.commit()
    conn.close()
    pass

def main():
    print("*** AMAZON EXTRACT DATA ***")
    base_dir = os.path.join(os.getcwd(), "_outputs", "amazon")
    filtered_dir = os.path.join(base_dir,"filtereds")
    if not os.path.exists(filtered_dir):
        return
    
    output_dir = os.path.join(base_dir,"extracts")
    os.makedirs(output_dir, exist_ok=True)

    create_db(os.path.join(output_dir,"Amazon Products.db"))
    create_db(os.path.join(output_dir,"Amazon Products Ex.db"))

    input_text = input("Enter number of item for each category (default 20000): ")
    min_item = 200
    max_item = 20000
    try:
        max_item = int(input_text)
    except Exception as e:
        max_item = 20000
        pass

    print(f"Min {min_item} and max {max_item} for each category.")

    for json_file in glob.glob(f"{filtered_dir}/*.jsonl"):
        input_file = open(json_file, 'r', encoding='utf-8')
        line_count = 0
        for _ in input_file:
            line_count += 1
        
        if line_count < (min_item * 2):
            continue

        input_file.seek(0, io.SEEK_SET)
        direct = False
        item_count = 0
        main_buffers = []
        sub_buffers = []
        for line in input_file:
            json_data = json.loads(line)
            if direct:
                main_buffers.append(json_data)
            else:
                sub_buffers.append(json_data)
            direct = not direct
            item_count += 1
            if item_count >= (max_item * 2):
                break
            pass

        save_to_db(os.path.join(output_dir,"Amazon Products.db"), main_buffers)
        save_to_db(os.path.join(output_dir,"Amazon Products Ex.db"), sub_buffers)
    pass

if __name__ == "__main__":
    main()
    pass