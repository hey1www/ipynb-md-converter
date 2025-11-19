import json
import os

def convert_ipynb_to_md(ipynb_path, md_path):
    """转换单个 ipynb 文件为 md 文件"""
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    md_lines = []
    for cell in notebook.get('cells', []):
        ctype = cell.get('cell_type')
        source = ''.join(cell.get('source', []))  # Jupyter 把每行存在列表里

        if not source.strip():
            continue

        if ctype == 'markdown':
            md_lines.append(source.rstrip('\n'))
            md_lines.append('')  # 空行分隔
        elif ctype == 'code':
            md_lines.append('```python')
            md_lines.append(source.rstrip('\n'))
            md_lines.append('```')
            md_lines.append('')
        # 其他类型（raw等）忽略

    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))


def main():
    # 用脚本所在目录作为根目录，而不是 os.getcwd()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. 收集所有 .ipynb 文件
    ipynb_files = []
    for root, dirs, files in os.walk(base_dir):
        # 跳过 Jupyter 的检查点目录
        if '.ipynb_checkpoints' in root:
            continue

        for filename in files:
            if filename.lower().endswith('.ipynb'):
                ipynb_path = os.path.join(root, filename)
                ipynb_files.append(ipynb_path)

    # 2. 如果一个也没有，给出提示并退出
    if not ipynb_files:
        print("没有找到任何 .ipynb 文件。请确认：")
        print("1) 你的 .ipynb 和这个脚本在同一目录（或其子目录）")
        print("2) 你是运行了这个脚本本身，而不是在别的工作目录执行")
        return

    # 3. 打印编号列表
    print("检测到以下 .ipynb 文件：")
    for idx, path in enumerate(ipynb_files, start=1):
        rel_path = os.path.relpath(path, base_dir)
        print(f"{idx}. {rel_path}")

    # 4. 询问用户选择
    print("\n请输入要转换的序号，多个序号请用空格分隔；")
    print("例如：1 3 5")
    print("直接回车表示转换上面列出的全部文件。")
    selection = input("你的选择：").strip()

    # 5. 解析用户输入
    if selection == "":
        # 全选
        selected_indices = list(range(1, len(ipynb_files) + 1))
    else:
        try:
            parts = selection.split()
            selected_indices = sorted(set(int(p) for p in parts))
        except ValueError:
            print("输入格式错误：只能输入数字序号，多个序号之间用空格分隔。")
            return

        # 检查是否有越界序号
        max_index = len(ipynb_files)
        if any(i < 1 or i > max_index for i in selected_indices):
            print(f"输入的序号必须在 1 到 {max_index} 范围内。")
            return

    # 6. 执行转换
    converted = 0
    for i in selected_indices:
        ipynb_path = ipynb_files[i - 1]
        root = os.path.dirname(ipynb_path)
        filename = os.path.basename(ipynb_path)

        md_filename = filename[:-6] + '.md'  # 去掉 .ipynb
        md_path = os.path.join(root, md_filename)

        print(f"转换: {ipynb_path} -> {md_path}")
        try:
            convert_ipynb_to_md(ipynb_path, md_path)
            converted += 1
        except Exception as e:
            print(f"[失败] {ipynb_path}: {e}")

    print(f"转换完成，共生成 {converted} 个 .md。")


if __name__ == "__main__":
    print("="*50)
    print("          .ipynb to .md 转换器 by heyi")
    print("="*50)
    main()