# HA_RMSD_Analysis

基于 PyMOL 的 H1N1 HA 蛋白抗原位点 RMSD 批量比对脚本

---

## 功能简介
本项目用于批量比较一组 HA 蛋白 PDB 文件与一个参考结构的 RMSD（Root Mean Square Deviation），针对五个经典抗原位点（Sa、Sb、Ca1、Ca2、Cb）。  
自动筛选出任一抗原位点 RMSD 超过设定阈值的样本，并导出结果至 Excel 文件。

---

## 依赖环境
- Python >= 3.8
- [PyMOL](https://pymol.org/2/) （支持 `import pymol`）
- pandas
- openpyxl

安装依赖：
```bash
pip install -r requirements.txt

#运行示例
python HA_script.py <pdb_dir> <ref_pdb> --threshold 0.1 --output HA_RMSD_results.xlsx

<pdb_dir>：包含所有待分析 PDB 文件的文件夹路径。

<ref_pdb>：参考标准 PDB 文件的完整路径（如 cluster_HA_stand_model_001.pdb）。

--threshold：可选参数，指定 RMSD 阈值（默认 0.1）。

--output：可选参数，指定输出的 Excel 文件名（默认 RMSD_analysis_results.xlsx）。
