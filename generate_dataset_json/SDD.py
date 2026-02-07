

import os
import json


class SDDSolver(object):
    CLSNAMES = [
        'electrical commutators',
    ]

    def __init__(self, root='data/mvtec'):
        self.root = root
        self.meta_path = f'{root}/meta.json'

    def run(self):
        info = dict(train={}, test={})
        anomaly_samples = 0
        normal_samples = 0
        for cls_name in self.CLSNAMES:
            cls_dir = f'{self.root}/{cls_name}'
            for phase in ['train', 'test']:
                cls_info = []
                phase_dir = f'{cls_dir}/{phase}'
                if not os.path.exists(phase_dir):
                    info[phase][cls_name] = cls_info
                    continue
                try:
                    species = os.listdir(phase_dir)
                    for specie in species:
                        is_abnormal = True if specie not in ['good'] else False
                        img_dir = f'{phase_dir}/{specie}'
                        if not os.path.isdir(img_dir):
                            continue
                        img_names = os.listdir(img_dir)
                        mask_names = None
                        if is_abnormal:
                            mask_dir = f'{cls_dir}/ground_truth/{specie}'
                            if os.path.exists(mask_dir):
                                mask_names = os.listdir(mask_dir)
                                mask_names.sort()
                        img_names.sort()
                        for idx, img_name in enumerate(img_names):
                            mask_path = ''
                            if is_abnormal and mask_names and idx < len(mask_names):
                                mask_path = f'{cls_name}/ground_truth/{specie}/{mask_names[idx]}'
                            info_img = dict(
                                img_path=f'{cls_name}/{phase}/{specie}/{img_name}',
                                mask_path=mask_path,
                                cls_name=cls_name,
                                specie_name=specie,
                                anomaly=1 if is_abnormal else 0,
                            )
                            cls_info.append(info_img)
                            if phase == 'test':
                                if is_abnormal:
                                    anomaly_samples = anomaly_samples + 1
                                else:
                                    normal_samples = normal_samples + 1
                except Exception as e:
                    print(f"Error processing {phase_dir}: {e}")
                info[phase][cls_name] = cls_info
        with open(self.meta_path, 'w') as f:
            f.write(json.dumps(info, indent=4) + "\n")
        print('normal_samples', normal_samples, 'anomaly_samples', anomaly_samples)


import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate meta.json for SDD dataset')
    parser.add_argument('--root', type=str, default='/remote-home/iot_zhouqihang/data/SDD', help='Root directory of the dataset')
    args = parser.parse_args()
    runner = SDDSolver(root=args.root)
    runner.run()
