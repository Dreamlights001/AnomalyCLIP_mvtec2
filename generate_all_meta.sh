#!/bin/bash

# 数据集根目录
DATASET_ROOT="/root/autodl-tmp/datasets"

# 进入 generate_dataset_json 目录
cd "$(dirname "$0")/generate_dataset_json"

# 生成 MVTec 数据集的 meta.json
echo "Generating meta.json for MVTec dataset..."
python mvtec.py --root "$DATASET_ROOT/mvtec"

# 生成 MVTec2 数据集的 meta.json
echo "Generating meta.json for MVTec2 dataset..."
python mvtec2.py --root "$DATASET_ROOT/mvtec2"

# 生成 VisA 数据集的 meta.json
echo "Generating meta.json for VisA dataset..."
python visa.py --root "$DATASET_ROOT/visa"

# 生成 SDD 数据集的 meta.json
echo "Generating meta.json for SDD dataset..."
python SDD.py --root "$DATASET_ROOT/sdd"

# 生成 DTD 数据集的 meta.json
echo "Generating meta.json for DTD dataset..."
python DTD.py --root "$DATASET_ROOT/DTD"

# 生成 BrainMRI 数据集的 meta.json
echo "Generating meta.json for BrainMRI dataset..."
python brainmri.py --root "$DATASET_ROOT/brainmri"

# 生成 Br35H 数据集的 meta.json
echo "Generating meta.json for Br35H dataset..."
python br35.py --root "$DATASET_ROOT/Br35H"

# 生成 BTAD 数据集的 meta.json
echo "Generating meta.json for BTAD dataset..."
python btad.py --root "$DATASET_ROOT/btad"

# 生成 DAGM 数据集的 meta.json
echo "Generating meta.json for DAGM dataset..."
python DAGM.py --root "$DATASET_ROOT/dagm"

# 生成 MPDD 数据集的 meta.json
echo "Generating meta.json for MPDD dataset..."
python mpdd.py --root "$DATASET_ROOT/mpdd"

# 生成 CVC-ClinicDB 数据集的 meta.json
echo "Generating meta.json for CVC-ClinicDB dataset..."
python clinicDB.py --root "$DATASET_ROOT/CVC-ClinicDB"

# 生成 CVC-ColonDB 数据集的 meta.json
echo "Generating meta.json for CVC-ColonDB dataset..."
python colonDB.py --root "$DATASET_ROOT/CVC-ColonDB"

# 生成 Kvasir 数据集的 meta.json
echo "Generating meta.json for Kvasir dataset..."
python kvasir.py --root "$DATASET_ROOT/Kvasir"

# 生成 ISIC2016 数据集的 meta.json
echo "Generating meta.json for ISIC2016 dataset..."
python isbi.py --root "$DATASET_ROOT/ISIC2016"

echo "All meta.json files generated successfully!"
