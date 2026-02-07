
#!/bin/bash

device=0

# Test on MVTec dataset
echo "=== Testing on MVTec dataset ==="
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale
save_dir=./checkpoints/${base_dir}/
CUDA_VISIBLE_DEVICES=${device} python test.py --dataset mvtec \
--data_path /root/autodl-tmp/datasets/mvtec --save_path ./results/${base_dir}/zero_shot \
--checkpoint_path ${save_dir}epoch_15.pth \
--features_list 24 --image_size 518 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}

# Test on VisA dataset
echo "=== Testing on VisA dataset ==="
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale_visa
save_dir=./checkpoints/${base_dir}/
CUDA_VISIBLE_DEVICES=${device} python test.py --dataset visa \
--data_path /root/autodl-tmp/datasets/visa --save_path ./results/${base_dir}/zero_shot \
--checkpoint_path ${save_dir}epoch_15.pth \
--features_list 24 --image_size 518 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}

# Test on MVTec2 dataset
echo "=== Testing on MVTec2 dataset ==="
depth=9
n_ctx=12
t_n_ctx=4
base_dir=${depth}_${n_ctx}_${t_n_ctx}_multiscale
save_dir=./checkpoints/${base_dir}/
CUDA_VISIBLE_DEVICES=${device} python test.py --dataset mvtec2 \
--data_path /root/autodl-tmp/datasets/mvtec2 --save_path ./results/${base_dir}/zero_shot_mvtec2 \
--checkpoint_path ${save_dir}epoch_15.pth \
--features_list 24 --image_size 518 --depth ${depth} --n_ctx ${n_ctx} --t_n_ctx ${t_n_ctx}
