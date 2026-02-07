import os
import json

def analyze_mvtec2_structure(dataset_root):
    """分析 MVTec2 数据集结构并统计样本数量"""
    print(f"=== Analyzing MVTec2 Dataset Structure ===")
    print(f"Dataset root: {dataset_root}")
    print("")
    
    # 检查数据集根目录是否存在
    if not os.path.exists(dataset_root):
        print(f"Error: Dataset directory not found at {dataset_root}")
        return
    
    # 获取类别列表
    categories = []
    for item in os.listdir(dataset_root):
        item_path = os.path.join(dataset_root, item)
        if os.path.isdir(item_path):
            categories.append(item)
    
    print(f"Found {len(categories)} categories: {categories}")
    print("")
    
    # 统计每个类别的样本
    total_normal = 0
    total_anomaly = 0
    
    for category in categories:
        print(f"--- Category: {category} ---")
        category_path = os.path.join(dataset_root, category)
        
        # 检查 train/good
        train_good_path = os.path.join(category_path, 'train', 'good')
        if os.path.exists(train_good_path):
            train_good_files = [f for f in os.listdir(train_good_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            print(f"Train good samples: {len(train_good_files)}")
        else:
            print("Train good directory not found")
        
        # 检查 test_public/good
        test_good_path = os.path.join(category_path, 'test_public', 'good')
        if os.path.exists(test_good_path):
            test_good_files = [f for f in os.listdir(test_good_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            print(f"Test good samples: {len(test_good_files)}")
            total_normal += len(test_good_files)
        else:
            print("Test good directory not found")
        
        # 检查 test_public/bad
        test_bad_path = os.path.join(category_path, 'test_public', 'bad')
        if os.path.exists(test_bad_path):
            test_bad_files = [f for f in os.listdir(test_bad_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            print(f"Test bad samples: {len(test_bad_files)}")
            total_anomaly += len(test_bad_files)
        else:
            print("Test bad directory not found")
        
        # 检查 test_public/ground_truth
        gt_path = os.path.join(category_path, 'test_public', 'ground_truth')
        if os.path.exists(gt_path):
            gt_files = [f for f in os.listdir(gt_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            print(f"Ground truth files: {len(gt_files)}")
        else:
            print("Ground truth directory not found")
        
        # 检查 validation 目录
        val_path = os.path.join(category_path, 'validation')
        if os.path.exists(val_path):
            # 检查 validation/good
            val_good_path = os.path.join(val_path, 'good')
            if os.path.exists(val_good_path):
                val_good_files = [f for f in os.listdir(val_good_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                print(f"Validation good samples: {len(val_good_files)}")
            else:
                # 检查 validation 目录下直接的文件
                val_files = [f for f in os.listdir(val_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                print(f"Validation samples: {len(val_files)}")
        else:
            print("Validation directory not found")
        
        print("")
    
    print(f"=== Summary ===")
    print(f"Total normal samples: {total_normal}")
    print(f"Total anomaly samples: {total_anomaly}")
    print(f"Total samples: {total_normal + total_anomaly}")
    print("")
    
    if total_anomaly == 0:
        print("Warning: No anomaly samples found! This is unusual.")
        print("Please check if the dataset structure is correct.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Analyze MVTec2 dataset structure')
    parser.add_argument('--root', type=str, default='/root/autodl-tmp/datasets/mvtec2', help='Root directory of the dataset')
    args = parser.parse_args()
    
    analyze_mvtec2_structure(args.root)
