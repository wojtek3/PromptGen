import os

def generate_tree(root_dir, prefix="", is_last=True):

    tree_str = ""
    base_name = os.path.basename(root_dir)
    if prefix == "":
        tree_str += f"{base_name}\n"
    else:
        connector = "└─ " if is_last else "├─ "
        tree_str += f"{prefix}{connector}{base_name}\n"

    items = sorted(os.listdir(root_dir))
    items = [item for item in items if not item.startswith('.')]

    new_prefix = prefix + ("   " if is_last else "│  ")
    for i, item in enumerate(items):
        path = os.path.join(root_dir, item)
        is_last_item = (i == len(items) - 1)
        if os.path.isdir(path):
            tree_str += generate_tree(path, prefix=new_prefix, is_last=is_last_item)
        else:
            connector = "└─ " if is_last_item else "├─ "
            tree_str += f"{new_prefix}{connector}{item}\n"

    return tree_str


def list_files_with_contents(root_dir):
    files_data = []

    for subdir, dirs, files in os.walk(root_dir):
        dirs.sort()
        files.sort()

        for file_name in files:
            if file_name.startswith('.'):
                continue

            file_path = os.path.join(subdir, file_name)
            rel_path = os.path.relpath(file_path, root_dir)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                content = "Can't open file"

            files_data.append((rel_path, content))

    return files_data


def main():
    folder_path = input("Project path: ").strip()

    if not os.path.isdir(folder_path):
        print("path doesn't exists.")
        return

    tree_representation = generate_tree(folder_path)

    files_data = list_files_with_contents(folder_path)

    result = []
    result.append(tree_representation)
    result.append("\n")

    for rel_path, content in files_data:
        result.append(f"// {rel_path}:\n")
        result.append(content)
        result.append("\n\n")

    final_text = "".join(result)

    with open("prompt.txt", "w", encoding="utf-8") as out_file:
        out_file.write(final_text)

    print("Prompt saved in prompt.txt")


if __name__ == "__main__":
    main()
