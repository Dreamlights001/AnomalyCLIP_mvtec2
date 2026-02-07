#!/bin/bash

# 数据集根目录
DATASET_ROOT="/root/autodl-tmp/datasets/mvtec2"

echo "=== MVTec2 Dataset Structure ==="
echo "Dataset root: $DATASET_ROOT"
echo ""

# 检查数据集根目录是否存在
if [ ! -d "$DATASET_ROOT" ]; then
    echo "Error: MVTec2 dataset directory not found at $DATASET_ROOT"
    exit 1
fi

# 列出顶层类别目录
echo "=== Top-level categories ==="
ls -la "$DATASET_ROOT"
echo ""

# 对于每个类别，检查其目录结构
echo "=== Category structures ==="
for category in "$DATASET_ROOT"/*; do
    if [ -d "$category" ]; then
        category_name=$(basename "$category")
        echo ""
        echo "--- Category: $category_name ---"
        
        # 列出类别下的子目录
        ls -la "$category"
        
        # 检查 test_public 目录
        test_public_dir="$category/test_public"
        if [ -d "$test_public_dir" ]; then
            echo ""
            echo "Test public directory structure:"
            ls -la "$test_public_dir"
            
            # 检查 bad 目录
            bad_dir="$test_public_dir/bad"
            if [ -d "$bad_dir" ]; then
                echo ""
                echo "Bad samples count: $(ls -la "$bad_dir" | wc -l)"
                echo "First 10 bad samples:"
                ls -la "$bad_dir" | head -10
            fi
            
            # 检查 ground_truth 目录
            gt_dir="$test_public_dir/ground_truth"
            if [ -d "$gt_dir" ]; then
                echo ""
                echo "Ground truth count: $(ls -la "$gt_dir" | wc -l)"
                echo "First 10 ground truth files:"
                ls -la "$gt_dir" | head -10
            fi
        fi
    fi
done

echo ""
echo "=== Structure check completed ==="
