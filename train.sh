
#!/bin/bash

device=1

# Train on VisA dataset
echo "=== Training on VisA dataset ==="
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale
save_dir=./checkpoints/${base_dir}/
CUDA_VISIBLE_DEVICES=${device} python train.py --dataset visa --train_data_path /root/autodl-tmp/datasets/visa \
--save_path ${save_dir} \
--features_list 24 --image_size 518  --batch_size 8 --print_freq 1 \
--epoch 15 --save_freq 1 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}

# Train on MVTec dataset
echo "=== Training on MVTec dataset ==="
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale_visa
save_dir=./checkpoints/${base_dir}/
CUDA_VISIBLE_DEVICES=${device} python train.py --dataset mvtec --train_data_path /root/autodl-tmp/datasets/mvtec \
--save_path ${save_dir} \
--features_list 24 --image_size 518  --batch_size 8 --print_freq 1 \
--epoch 15 --save_freq 1 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}

# Train on MVTec2 dataset
echo "=== Training on MVTec2 dataset ==="
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale_mvtec2
save_dir=./checkpoints/${base_dir}/
CUDA_VISIBLE_DEVICES=${device} python train.py --dataset mvtec2 --train_data_path /root/autodl-tmp/datasets/mvtec2 \
--save_path ${save_dir} \
--features_list 24 --image_size 518  --batch_size 8 --print_freq 1 \
--epoch 15 --save_freq 1 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}
