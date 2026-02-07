import os
import json

# 检查 MVTec2 数据集的 meta.json 文件
dataset_root = '/root/autodl-tmp/datasets/mvtec2'
meta_path = os.path.join(dataset_root, 'meta.json')

print(f"=== Checking MVTec2 dataset structure ===")
print(f"Dataset root: {dataset_root}")
print(f"Meta.json path: {meta_path}")

# 检查 meta.json 文件是否存在
if os.path.exists(meta_path):
    print("✓ meta.json file exists")
    # 加载 meta.json 文件
    with open(meta_path, 'r') as f:
        meta_data = json.load(f)
    
    # 检查测试数据
    if 'test' in meta_data:
        print(f"✓ Test data found with {len(meta_data['test'])} categories")
        
        # 检查每个类别的测试数据
        for category, data in meta_data['test'].items():
            print(f"  - {category}: {len(data)} samples")
            
            # 检查是否有异常样本
            has_anomaly = any(item['anomaly'] == 1 for item in data)
            has_normal = any(item['anomaly'] == 0 for item in data)
            print(f"    Anomaly samples: {has_anomaly}")
            print(f"    Normal samples: {has_normal}")
            
            # 检查样本路径是否存在
            if data:
                first_sample = data[0]
                img_path = os.path.join(dataset_root, first_sample['img_path'])
                if os.path.exists(img_path):
                    print(f"    First sample path exists: {img_path}")
                else:
                    print(f"    First sample path does not exist: {img_path}")
else:
    print("✗ meta.json file not found")
    # 检查数据集目录结构
    if os.path.exists(dataset_root):
        print("Dataset directory structure:")
        for item in os.listdir(dataset_root):
            item_path = os.path.join(dataset_root, item)
            if os.path.isdir(item_path):
                print(f"  - {item}/")
                # 检查每个类别的子目录
                for subitem in os.listdir(item_path):
                    subitem_path = os.path.join(item_path, subitem)
                    if os.path.isdir(subitem_path):
                        print(f"    - {subitem}/")
    else:
        print("✗ Dataset directory not found")
