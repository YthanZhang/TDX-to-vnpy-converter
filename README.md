# 使用说明

## 依赖

程序依赖 `pandas` 输出 csv 文件, 使用 `pip install pandas` 安装 pandas

## 运行

将从通达信导出的 `*.txt` 文件放置到 `tdx_files` 文件夹中

打开命令行运行 `python main.py [m/d]`, 使用 `m` 转换分钟线, `d` 转换日线


输出会被放置到 `csv_files` 文件夹中

## 其他指令

`-i [path]` 设置输入文件夹

`-o [path]` 设置输出文件夹

`--no-adjust-time` 禁用分钟线转换时间矫正
