# ipynb-md converter v3

一个用于批量将 Jupyter Notebook（`.ipynb`）转换为 Markdown（`.md`）的小工具脚本。适合把实验记录、课堂作业或项目笔记从 Notebook 导出为纯文本/Markdown 文件进行版本管理或发布。

## 功能简介

- 自动递归扫描脚本所在目录及其子目录中的所有 `.ipynb` 文件（跳过 `.ipynb_checkpoints` 目录）。
- 以编号列表的形式展示发现的所有 Notebook 文件。
- 支持键盘交互选择要转换的文件：
  - 回车：转换全部
  - 输入一个或多个编号：只转换指定文件
- 将 Notebook 中的单元格转换为 Markdown：
  - Markdown 单元格：按原内容输出，并用空行分隔
  - 代码单元格：使用 ```python 代码块包裹
  - 其他类型单元格（如 raw）：忽略
- 生成的 `.md` 文件与原 `.ipynb` 文件位于同一目录，文件名相同，仅扩展名不同。

## 环境要求

- Python 3.x
- 无需额外第三方依赖，仅使用标准库 `json` 与 `os`。:contentReference[oaicite:0]{index=0}

## 使用方法

1. 将 `ipynb-md converter v3.py` 放到包含 Notebook 的根目录（或任意上层目录）。
2. 在该脚本所在目录打开终端/命令行，运行：

   ```bash
   python "ipynb-md converter v3.py"
````

3. 终端中会显示类似输出：

   ```text
   ==================================================
             .ipynb to .md 转换器 by heyi
   ==================================================
   检测到以下 .ipynb 文件：
   1. notebook1.ipynb
   2. subdir/notebook2.ipynb
   3. ...

   请输入要转换的序号，多个序号请用空格分隔；
   例如：1 3 5
   直接回车表示转换上面列出的全部文件。
   ```

4. 交互选择：

   * 转换全部：直接按回车
   * 只转换第 1 和第 3 个文件：输入 `1 3` 然后回车

5. 转换完成后，会在对应目录生成同名 `.md` 文件，例如：

   * `notebook1.ipynb` → `notebook1.md`

## 实现方式概述

* `convert_ipynb_to_md(ipynb_path, md_path)`

  * 读取 `.ipynb` 文件（实际为 JSON），遍历 `cells` 列表。
  * 对每个单元格：

    * 拼接 `cell["source"]` 列表为完整字符串。
    * 去除空白单元格。
    * 按 `cell_type` 区分：

      * `markdown`：原样写入，并加入一个空行。
      * `code`：包裹在 ```python 代码块中，并加空行。
* `main()`

  * 使用 `os.path.abspath(__file__)` 得到脚本所在目录作为扫描根目录，而非当前工作目录，避免因在其他路径运行脚本导致扫描不到文件的问题。
  * 用 `os.walk` 递归遍历目录，过滤 `.ipynb_checkpoints`。
  * 收集所有 `.ipynb` 路径并编号打印。
  * 解析用户输入（空字符串=全选；否则按空格分割为多个数字）。
  * 做输入合法性及范围检查。
  * 根据用户选择调用 `convert_ipynb_to_md` 执行转换并统计成功数量。

## 注意事项

* 若目录中没有任何 `.ipynb` 文件，脚本会给出提示并直接退出。
* 若某个 Notebook 文件损坏或格式异常，转换该文件时会打印错误信息，但不会影响其他文件的转换。
* Markdown 输出默认以 UTF-8 编码保存。
