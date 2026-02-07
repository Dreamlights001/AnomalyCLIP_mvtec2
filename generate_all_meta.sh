#!/bin/bash

# 数据集根目录
DATASET_ROOT="/root/autodl-tmp/datasets"

# 进入 generate_dataset_json 目录
cd "$(dirname "$0")/generate_dataset_json" || {
    echo "Error: Could not enter generate_dataset_json directory"
    exit 1
}

echo "Starting to generate meta.json files for all datasets..."
echo ""

# 函数：生成单个数据集的 meta.json
generate_meta() {
    local dataset_name="$1"
    local script_name="$2"
    local dataset_path="$3"
    
    echo "=== Generating meta.json for $dataset_name dataset ==="
    echo "Dataset path: $dataset_path"
    
    # 检查数据集目录是否存在
    if [ ! -d "$dataset_path" ]; then
        echo "Warning: $dataset_name dataset directory not found at $dataset_path"
        echo "Skipping $dataset_name dataset..."
        echo ""
        return
    fi
    
    # 运行生成脚本
    if python "$script_name" --root "$dataset_path"; then
        echo "✓ Successfully generated meta.json for $dataset_name dataset"
    else
        echo "✗ Failed to generate meta.json for $dataset_name dataset"
        echo "Continuing with other datasets..."
    fi
    
    echo ""
}

# 生成各个数据集的 meta.json
generate_meta "MVTec" "mvtec.py" "$DATASET_ROOT/mvtec"
generate_meta "MVTec2" "mvtec2.py" "$DATASET_ROOT/mvtec2"
generate_meta "VisA" "visa.py" "$DATASET_ROOT/visa"
generate_meta "SDD" "SDD.py" "$DATASET_ROOT/sdd"
generate_meta "DTD" "DTD.py" "$DATASET_ROOT/DTD"
generate_meta "BrainMRI" "brainmri.py" "$DATASET_ROOT/brainmri"
generate_meta "Br35H" "br35.py" "$DATASET_ROOT/Br35H"
generate_meta "BTAD" "btad.py" "$DATASET_ROOT/btad"
generate_meta "DAGM" "DAGM.py" "$DATASET_ROOT/dagm"
generate_meta "MPDD" "mpdd.py" "$DATASET_ROOT/mpdd"
generate_meta "CVC-ClinicDB" "clinicDB.py" "$DATASET_ROOT/CVC-ClinicDB"
generate_meta "CVC-ColonDB" "colonDB.py" "$DATASET_ROOT/CVC-ColonDB"
generate_meta "Kvasir" "kvasir.py" "$DATASET_ROOT/Kvasir"
generate_meta "ISIC2016" "isbi.py" "$DATASET_ROOT/ISIC2016"

echo "=== Generation process completed! ==="
echo "Some datasets may have failed, but the process has completed."
echo "Check the output above for details on which datasets were successful."

