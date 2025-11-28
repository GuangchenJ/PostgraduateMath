import os
import re
from collections import Counter

import pandas as pd


def export_tex_stats_to_excel(input_path, output_path=None):
    """
    读取 tex 文件，统计考点，并输出为 Excel 文件
    """

    # 1. 检查输入文件是否存在
    if not os.path.exists(input_path):
        print(f"❌ 错误：找不到文件 '{input_path}'")
        return

    # 2. 自动生成输出文件名（如果未指定）
    if output_path is None:
        # 例如输入 'test.tex'，输出变成 'test_统计结果.xlsx'
        base_name = os.path.splitext(input_path)[0]
        output_path = "1128错题_统计结果.xlsx"

    print(f"📖 正在读取文件: {input_path} ...")

    # 3. 读取文件内容 (处理编码)
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        print("⚠️ UTF-8 读取失败，尝试 GBK 编码...")
        with open(input_path, "r", encoding="gb18030") as f:
            content = f.read()

    # 4. 正则提取考点
    # 逻辑：匹配 \ansat{ ... 考点(任意内容)：(捕获目标) (遇到 ' - ' 或 '}' 结束)
    pattern = re.compile(r"\\ansat\{.*?(?:考点.*?：)\s*(.*?)\s*(?: - |\})")
    matches = pattern.findall(content)

    if not matches:
        print("⚠️ 未在文件中提取到任何考点，请检查文件格式。")
        return

    # 去除首尾空格
    cleaned_points = [m.strip() for m in matches]

    # 5. 统计频次
    # Counter 返回字典形式: {'考点A': 5, '考点B': 2}
    counts = Counter(cleaned_points)

    # 转换为 Pandas DataFrame (表格数据)
    # most_common() 会自动按数量降序排列
    df = pd.DataFrame(counts.most_common(), columns=["考点名称", "出现次数"])

    # 6. (可选) 增加一个百分比列
    total_count = df["出现次数"].sum()
    df["占比"] = df["出现次数"].apply(lambda x: f"{(x / total_count):.1%}")

    # 7. 保存为 Excel
    try:
        df.to_excel(output_path, index=False, sheet_name="考点统计")
        print("=" * 40)
        print("✅ 成功！")
        print(f"📊 共统计到 {total_count} 个题目，涵盖 {len(df)} 个不同考点。")
        print(f"📂 统计文件已保存至: {output_path}")
        print("=" * 40)
    except Exception as e:
        print(f"❌ 保存 Excel 失败: {e}")
        print("请检查文件是否被其他程序（如 Excel）占用。")


# ---在此处修改文件路径---

# 输入的 tex 文件路径
input_tex_file = "./zonghecuoti/1128/all_shuffled_problems.tex"

# 运行函数
export_tex_stats_to_excel(input_tex_file)
