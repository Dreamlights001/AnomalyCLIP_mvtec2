
#!/bin/bash

# 检查是否有可用的 CUDA GPU
if command -v nvidia-smi &> /dev/null && nvidia-smi | grep -q "CUDA Version";
 then
    echo "CUDA GPU detected, using GPU for training"
    device=0
    echo "Using CUDA device ${device}"
else
    echo "No CUDA GPU detected, using CPU for training"
    device=-1
fi

# Train on MVTec2 dataset (focus on MVTec2 first)
echo "=== Training on MVTec2 dataset ==="
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale_mvtec2
save_dir=./checkpoints/${base_dir}/

# 创建保存目录
mkdir -p ${save_dir}

# 运行训练
if [ ${device} -ge 0 ]; then
    # 使用默认 CUDA 设备
    python train.py --dataset mvtec2 --train_data_path /root/autodl-tmp/datasets/mvtec2 \
    --save_path ${save_dir} \
    --features_list 24 --image_size 518  --batch_size 4 --print_freq 1 \
    --epoch 15 --save_freq 1 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}
else
    # 使用 CPU
    python train.py --dataset mvtec2 --train_data_path /root/autodl-tmp/datasets/mvtec2 \
    --save_path ${save_dir} \
    --features_list 24 --image_size 518  --batch_size 4 --print_freq 1 \
    --epoch 15 --save_freq 1 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}
fi

echo "Training completed!"
