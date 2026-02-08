import os
import argparse

def check_directory_structure(root):
    """检查MVTec2数据集的目录结构"""
    print(f"Checking MVTec2 dataset structure at: {root}")
    print("=" * 80)
    
    # 检查每个类别
    classes = ['can', 'fabric', 'fruit_jelly', 'rice', 'sheet_metal', 'vial', 'wallplugs', 'walnuts']
    
    for cls_name in classes:
        cls_dir = os.path.join(root, cls_name)
        if not os.path.exists(cls_dir):
            print(f"Class directory not found: {cls_dir}")
            continue
        
        print(f"\nClass: {cls_name}")
        print("-" * 40)
        
        # 检查test_public目录
        test_public_dir = os.path.join(cls_dir, 'test_public')
        if os.path.exists(test_public_dir):
            print(f"test_public directory found: {test_public_dir}")
            
            # 检查good子目录
            good_dir = os.path.join(test_public_dir, 'good')
            if os.path.exists(good_dir):
                good_files = os.listdir(good_dir)
                print(f"  good directory: {len(good_files)} files")
                if good_files:
                    print(f"  Example good file: {good_files[0]}")
            
            # 检查bad子目录
            bad_dir = os.path.join(test_public_dir, 'bad')
            if os.path.exists(bad_dir):
                bad_files = os.listdir(bad_dir)
                print(f"  bad directory: {len(bad_files)} files")
                if bad_files:
                    print(f"  Example bad file: {bad_files[0]}")
            
            # 检查ground_truth目录
            ground_truth_dir = os.path.join(test_public_dir, 'ground_truth')
            if os.path.exists(ground_truth_dir):
                mask_files = os.listdir(ground_truth_dir)
                print(f"  ground_truth directory: {len(mask_files)} files")
                if mask_files:
                    print(f"  Example mask file: {mask_files[0]}")
            else:
                print("  ground_truth directory not found")
        else:
            print(f"test_public directory not found for class: {cls_name}")
    
    print("\n" + "=" * 80)
    print("Directory structure check completed.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check MVTec2 dataset directory structure')
    parser.add_argument('--root', type=str, default='/root/autodl-tmp/datasets/mvtec2', help='Root directory of the dataset')
    args = parser.parse_args()
    check_directory_structure(args.root)