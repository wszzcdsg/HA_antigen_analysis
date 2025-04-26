#!/usr/bin/env python
"""
HA_script.py

依赖：
  pandas
  openpyxl
  pymol（确保你的 Python 环境中已安装 PyMOL 的 Python 包）

示例用法：
  python HA_script.py /path/to/pdb_dir /path/to/cluster_HA_stand_model_001.pdb \
      --threshold 0.1 --output results.xlsx
"""

import os
import argparse
import pandas as pd
from pymol import cmd

# 定义五个经典抗原位点及其残基
ANTIGEN_SITES = {
    'Sa':  [128,129,156,157,158,159,160,162,163,164,165,166,167],
    'Sb':  [187,188,189,190,191,192,193,194,195,196,197,198],
    'Ca1': [169,170,171,172,173,206,207,208],
    'Ca2': [140,141,142,143,144,145],
    'Cb':  [79,80,81,82,83,84]
}

def parse_args():
    parser = argparse.ArgumentParser(
        description="批量计算多个 HA PDB 文件在经典抗原位点上的 RMSD，并将超过阈值的结果导出 Excel。"
    )
    parser.add_argument(
        "pdb_dir",
        help="包含所有待分析 PDB 文件的文件夹路径"
    )
    parser.add_argument(
        "ref_pdb",
        help="参考 PDB 文件的完整路径（cluster_HA_stand_model_001.pdb）"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.1,
        help="RMSD 阈值，默认为 0.1"
    )
    parser.add_argument(
        "--output",
        default="RMSD_analysis_results.xlsx",
        help="输出的 Excel 文件名，默认为 RMSD_analysis_results.xlsx"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    pdb_dir    = args.pdb_dir
    ref_pdb    = args.ref_pdb
    threshold  = args.threshold
    output_xlsx= args.output

    # 检查输入
    if not os.path.isdir(pdb_dir):
        raise SystemExit(f"Error: '{pdb_dir}' 不是有效的目录。")
    if not os.path.isfile(ref_pdb):
        raise SystemExit(f"Error: 参考 PDB 文件 '{ref_pdb}' 不存在。")

    # 加载参考结构
    cmd.reinitialize()  # 清空任何已有对象
    cmd.load(ref_pdb, "ref")

    # 收集所有样本 PDB 文件（排除参考文件本身）
    pdb_files = sorted([
        os.path.join(pdb_dir, f)
        for f in os.listdir(pdb_dir)
        if f.lower().endswith(".pdb") and os.path.abspath(os.path.join(pdb_dir, f)) != os.path.abspath(ref_pdb)
    ])

    results = []

    # 遍历每个样本
    for pdb_file in pdb_files:
        base_name = os.path.basename(pdb_file)
        print(f"Processing {base_name} ...")
        cmd.load(pdb_file, "sample")
        cmd.align("sample", "ref")

        # 对每个抗原位点计算 RMSD
        for site, residues in ANTIGEN_SITES.items():
            sel_ref =   f"ref   and resi {'+'.join(map(str, residues))}"
            sel_sam =  f"sample and resi {'+'.join(map(str, residues))}"
            cmd.select(f"{site}_ref",   sel_ref)
            cmd.select(f"{site}_sam", sel_sam)

            rmsd_val = cmd.rms_cur(f"{site}_sam", f"{site}_ref")
            if rmsd_val > threshold:
                results.append({
                    'PDB文件': base_name,
                    '抗原位点': site,
                    'RMSD值': round(rmsd_val, 3)
                })

        # 清除 sample，进入下一个循环
        cmd.delete("sample")

    # 导出 Excel
    if results:
        df = pd.DataFrame(results)
        df.to_excel(output_xlsx, index=False)
        print(f"分析完成，共 {len(results)} 条记录，已写入 '{output_xlsx}'.")
    else:
        print("分析完成，无任意抗原位点的 RMSD 超过阈值。")

if __name__ == "__main__":
    main()
