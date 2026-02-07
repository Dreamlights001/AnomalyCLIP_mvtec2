import os
import json


class MVTec2Solver(object):
    CLSNAMES = [
        'can', 'fabric', 'fruit_jelly', 'rice', 'sheet_metal', 'vial', 'wallplugs', 'walnuts'
    ]

    def __init__(self, root='data/mvtec2'):
        self.root = root
        self.meta_path = f'{root}/meta.json'

    def extract_metadata(self, filename):
        """Extract metadata from filename, e.g., 'shift_rot45_001.png' -> {'condition': 'shift_rot45', 'index': '001'}"""
        metadata = {}
        if '_' in filename:
            name_parts = filename.split('_')
            # Extract condition information
            condition_parts = []
            for part in name_parts[:-1]:  # Exclude the index part
                if part.isdigit() and len(part) == 3:
                    break
                condition_parts.append(part)
            if condition_parts:
                metadata['condition'] = '_'.join(condition_parts)
            # Extract index
            if name_parts[-1].startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                metadata['index'] = name_parts[-1].split('.')[0]
        return metadata

    def get_mask_path(self, img_name, ground_truth_dir):
        """Find corresponding mask file for an image"""
        # Try to find mask with matching name pattern
        base_name = os.path.splitext(img_name)[0]
        for mask_name in os.listdir(ground_truth_dir):
            if base_name in mask_name or 'mask' in mask_name:
                return mask_name
        # Fallback: return None if no match found
        return None

    def run(self):
        info = dict(train={}, validation={}, test={})
        anomaly_samples = 0
        normal_samples = 0
        for cls_name in self.CLSNAMES:
            cls_dir = f'{self.root}/{cls_name}'
            # Process train data
            train_cls_info = []
            train_good_dir = f'{cls_dir}/train/good'
            if os.path.exists(train_good_dir):
                img_names = os.listdir(train_good_dir)
                img_names.sort()
                for img_name in img_names:
                    metadata = self.extract_metadata(img_name)
                    info_img = dict(
                        img_path=f'{cls_name}/train/good/{img_name}',
                        mask_path='',
                        cls_name=cls_name,
                        specie_name='good',
                        anomaly=0,
                        **metadata
                    )
                    train_cls_info.append(info_img)
            info['train'][cls_name] = train_cls_info
            
            # Process validation data
            validation_cls_info = []
            validation_dir = f'{cls_dir}/validation'
            if os.path.exists(validation_dir):
                # Check if validation directory has subdirectories
                items = os.listdir(validation_dir)
                for item in items:
                    item_path = f'{validation_dir}/{item}'
                    if os.path.isdir(item_path):
                        # This is a subdirectory (e.g., 'good')
                        specie = item
                        is_abnormal = True if specie not in ['good'] else False
                        try:
                            img_names = os.listdir(item_path)
                            img_names.sort()
                            for img_name in img_names:
                                # Skip non-image files
                                if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                                    continue
                                metadata = self.extract_metadata(img_name)
                                info_img = dict(
                                    img_path=f'{cls_name}/validation/{specie}/{img_name}',
                                    mask_path='',
                                    cls_name=cls_name,
                                    specie_name=specie,
                                    anomaly=1 if is_abnormal else 0,
                                    **metadata
                                )
                                validation_cls_info.append(info_img)
                        except Exception as e:
                            print(f"Error processing validation subdirectory {item}: {e}")
                            continue
                    else:
                        # This is a file directly in validation directory
                        # Skip non-image files
                        if not item.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                            continue
                        metadata = self.extract_metadata(item)
                        info_img = dict(
                            img_path=f'{cls_name}/validation/{item}',
                            mask_path='',
                            cls_name=cls_name,
                            specie_name='validation',
                            anomaly=0,
                            **metadata
                        )
                        validation_cls_info.append(info_img)
            info['validation'][cls_name] = validation_cls_info
            
            # Process test data
            test_cls_info = []
            test_public_dir = f'{cls_dir}/test_public'
            if os.path.exists(test_public_dir):
                # Process good samples
                good_dir = f'{test_public_dir}/good'
                if os.path.exists(good_dir):
                    img_names = os.listdir(good_dir)
                    img_names.sort()
                    for img_name in img_names:
                        metadata = self.extract_metadata(img_name)
                        info_img = dict(
                            img_path=f'{cls_name}/test_public/good/{img_name}',
                            mask_path='',
                            cls_name=cls_name,
                            specie_name='good',
                            anomaly=0,
                            **metadata
                        )
                        test_cls_info.append(info_img)
                        normal_samples += 1
                
                # Process bad samples
                bad_dir = f'{test_public_dir}/bad'
                ground_truth_dir = f'{test_public_dir}/ground_truth'
                if os.path.exists(bad_dir) and os.path.exists(ground_truth_dir):
                    img_names = os.listdir(bad_dir)
                    img_names.sort()
                    for img_name in img_names:
                        mask_name = self.get_mask_path(img_name, ground_truth_dir)
                        if mask_name:
                            metadata = self.extract_metadata(img_name)
                            info_img = dict(
                                img_path=f'{cls_name}/test_public/bad/{img_name}',
                                mask_path=f'{cls_name}/test_public/ground_truth/{mask_name}',
                                cls_name=cls_name,
                                specie_name='bad',
                                anomaly=1,
                                **metadata
                            )
                            test_cls_info.append(info_img)
                            anomaly_samples += 1
            info['test'][cls_name] = test_cls_info
        with open(self.meta_path, 'w') as f:
            f.write(json.dumps(info, indent=4) + "\n")
        print('normal_samples', normal_samples, 'anomaly_samples', anomaly_samples)
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate meta.json for MVTec2 dataset')
    parser.add_argument('--root', type=str, default='/root/autodl-tmp/datasets/mvtec2', help='Root directory of the dataset')
    args = parser.parse_args()
    runner = MVTec2Solver(root=args.root)
    runner.run()
