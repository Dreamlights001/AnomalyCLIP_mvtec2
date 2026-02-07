
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

# Train on VisA dataset (primary training dataset)
echo "=== Training on VisA dataset ==="
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale
save_dir=./checkpoints/${base_dir}/

# 创建保存目录
mkdir -p ${save_dir}

# 运行训练 - 进一步增加 batch size 以充分利用 24G 显存
echo "Starting VisA dataset training with maximum batch size..."
python train.py --dataset visa --train_data_path /root/autodl-tmp/datasets/visa \
--save_path ${save_dir} \
--features_list 24 --image_size 518  --batch_size 32 --print_freq 1 \
--epoch 15 --save_freq 1 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}

echo "VisA dataset training completed!"

# Train on MVTec dataset
echo "=== Training on MVTec dataset ==="
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale_visa
save_dir=./checkpoints/${base_dir}/

# 创建保存目录
mkdir -p ${save_dir}

# 运行训练 - 进一步增加 batch size 以充分利用 24G 显存
echo "Starting MVTec dataset training with maximum batch size..."
python train.py --dataset mvtec --train_data_path /root/autodl-tmp/datasets/mvtec \
--save_path ${save_dir} \
--features_list 24 --image_size 518  --batch_size 32 --print_freq 1 \
--epoch 15 --save_freq 1 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}

echo "MVTec dataset training completed!"

echo "=== All training completed! ==="
echo "MVTec2 dataset is only used for testing, not training."
echo "Use test.sh to evaluate on MVTec2 dataset."
