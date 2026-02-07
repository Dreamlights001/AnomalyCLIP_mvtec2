import os
import json


class Br35Solver(object):
    CLSNAMES = ['brain']

    def __init__(self, root='data/mvtec'):
        self.root = root
        self.meta_path = f'{root}/meta.json'

    def run(self):
        info = dict(train={}, test={})
        for cls_name in self.CLSNAMES:
            cls_dir = self.root
            for phase in ['test']:
                cls_info = []
                # Get all items in the directory
                items = os.listdir(cls_dir)
                for item in items:
                    # Skip meta.json and other non-directory items
                    item_path = os.path.join(cls_dir, item)
                    if not os.path.isdir(item_path):
                        continue
                    
                    specie = item
                    is_abnormal = True if specie not in ['no'] else False
                    
                    # Get image files in the directory
                    try:
                        img_names = os.listdir(item_path)
                        img_names.sort()
                        for img_name in img_names:
                            # Skip non-image files
                            if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                                continue
                            
                            info_img = dict(
                                img_path=f'{specie}/{img_name}',
                                cls_name=cls_name,
                                mask_path="",
                                specie_name=specie,
                                anomaly=1 if is_abnormal else 0,
                            )
                            cls_info.append(info_img)
                    except Exception as e:
                        print(f"Error processing {item_path}: {e}")
                        continue
                info[phase][cls_name] = cls_info
        with open(self.meta_path, 'w') as f:
            f.write(json.dumps(info, indent=4) + "\n")

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate meta.json for Br35H dataset')
    parser.add_argument('--root', type=str, default='/remote-home/iot_zhouqihang/data/br35', help='Root directory of the dataset')
    args = parser.parse_args()
    runner = Br35Solver(root=args.root)
    runner.run()
