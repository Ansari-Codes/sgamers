import os
import argparse
def format_name(name: str): return name.replace("_", " ").title().replace(" ", "")
def create_file(folder: str, file_name: str):
    folder_name = format_name(folder)
    file_name_formatted = format_name(file_name)
    file_name_final = folder_name + file_name_formatted
    if not os.path.exists(folder_name): os.makedirs(folder_name)
    full_path = os.path.join(folder_name, file_name_final + ".py")
    if folder.lower() == "page": content = "async def create(*args, **kwargs):\n    pass\n"
    elif folder.lower() == "comps": content = f"async def Comp{file_name_formatted}(*args, **kwargs):\n    pass\n"
    else: content = "# Auto-generated file\n"
    with open(full_path, "w") as f: f.write(content)
    print(f"Created file: {full_path}")
def main():
    parser = argparse.ArgumentParser(description="CLI file creator")
    parser.add_argument("command", choices=["create"], help="Command to run")
    parser.add_argument("folder", help="Folder name")
    parser.add_argument("file", help="File name")
    args = parser.parse_args()
    if args.command == "create": create_file(args.folder, args.file)
if __name__ == "__main__": main()