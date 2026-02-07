#!/bin/bash

# 专门测试 MVTec2 数据集的脚本
echo "=== Testing only MVTec2 dataset ==="

# 配置参数
device=0
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale
save_dir=./checkpoints/${base_dir}/
checkpoint_path="${save_dir}epoch_15.pth"

# 检查 checkpoint 文件是否存在
if [ ! -f "$checkpoint_path" ]; then
    echo "Error: Checkpoint file not found at $checkpoint_path"
    echo "Please train the model first using train.sh"
    exit 1
fi

echo "Using checkpoint: $checkpoint_path"
echo "Testing MVTec2 dataset..."

# 运行测试命令
CUDA_VISIBLE_DEVICES=${device} python test.py --dataset mvtec2 \
--data_path /root/autodl-tmp/datasets/mvtec2 \
--save_path ./results/${base_dir}/zero_shot_mvtec2 \
--checkpoint_path "$checkpoint_path" \
--features_list 6 12 18 24 \
--image_size 518 \
--depth ${depth} \
--n_ctx ${n_ctx} \
--t_n_ctx ${t_n_ctx} \
--metrics image-pixel-level

echo "MVTec2 dataset testing completed!"
