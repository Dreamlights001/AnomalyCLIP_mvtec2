import os
import json
import pandas as pd


class VisASolver(object):
    CLSNAMES = [
        'candle', 'capsules', 'cashew', 'chewinggum', 'fryum',
        'macaroni1', 'macaroni2', 'pcb1', 'pcb2', 'pcb3',
        'pcb4', 'pipe_fryum',
    ]

    def __init__(self, root='data/visa'):
        self.root = root
        self.meta_path = f'{root}/meta.json'
        self.phases = ['train', 'test']
        self.csv_data = pd.read_csv(f'{root}/split_csv/1cls.csv', header=0)

    def run(self):
        info = {phase: {} for phase in self.phases}
        anomaly_samples = 0
        normal_samples = 0
        
        # Get column names
        columns = self.csv_data.columns.tolist()
        print(f"CSV columns: {columns}")
        
        # Try different column name variations
        object_col = None
        split_col = None
        label_col = None
        image_col = None
        mask_col = None
        
        # Map possible column names
        for col in columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['object', 'class', 'category']):
                object_col = col
            elif any(keyword in col_lower for keyword in ['split', 'phase']):
                split_col = col
            elif any(keyword in col_lower for keyword in ['label', 'status']):
                label_col = col
            elif any(keyword in col_lower for keyword in ['image', 'img', 'path']):
                image_col = col
            elif any(keyword in col_lower for keyword in ['mask', 'gt', 'groundtruth']):
                mask_col = col
        
        print(f"Mapped columns: object={object_col}, split={split_col}, label={label_col}, image={image_col}, mask={mask_col}")
        
        # Fallback to indices if column names not found
        if not all([object_col, split_col, label_col, image_col]):
            print("Warning: Using column indices as fallback")
            object_col = 0 if len(columns) > 0 else None
            split_col = 1 if len(columns) > 1 else None
            label_col = 2 if len(columns) > 2 else None
            image_col = 3 if len(columns) > 3 else None
            mask_col = 4 if len(columns) > 4 else None
        
        for cls_name in self.CLSNAMES:
            # Filter data for current class
            try:
                if isinstance(object_col, str):
                    cls_data = self.csv_data[self.csv_data[object_col] == cls_name]
                else:
                    cls_data = self.csv_data[self.csv_data.iloc[:, object_col] == cls_name]
            except Exception as e:
                print(f"Error filtering class {cls_name}: {e}")
                # Skip this class if filtering fails
                for phase in self.phases:
                    info[phase][cls_name] = []
                continue
            
            for phase in self.phases:
                cls_info = []
                # Filter data for current phase
                try:
                    if isinstance(split_col, str):
                        cls_data_phase = cls_data[cls_data[split_col] == phase]
                    else:
                        cls_data_phase = cls_data[cls_data.iloc[:, split_col] == phase]
                except Exception as e:
                    print(f"Error filtering phase {phase}: {e}")
                    info[phase][cls_name] = []
                    continue
                
                cls_data_phase.index = list(range(len(cls_data_phase)))
                for idx in range(cls_data_phase.shape[0]):
                    try:
                        data = cls_data_phase.loc[idx]
                        
                        # Determine if abnormal
                        try:
                            if isinstance(label_col, str):
                                label_value = data[label_col]
                            else:
                                label_value = data.iloc[label_col]
                            is_abnormal = str(label_value).lower() == 'anomaly'
                        except Exception as e:
                            print(f"Error getting label: {e}")
                            is_abnormal = False
                        
                        # Get image path
                        try:
                            if isinstance(image_col, str):
                                img_path = data[image_col]
                            else:
                                img_path = data.iloc[image_col]
                        except Exception as e:
                            print(f"Error getting image path: {e}")
                            continue
                        
                        # Get mask path
                        mask_path = ''
                        if is_abnormal and mask_col is not None:
                            try:
                                if isinstance(mask_col, str):
                                    mask_path = data[mask_col]
                                else:
                                    mask_path = data.iloc[mask_col]
                            except Exception as e:
                                print(f"Error getting mask path: {e}")
                        
                        info_img = dict(
                            img_path=img_path,
                            mask_path=mask_path,
                            cls_name=cls_name,
                            specie_name='',
                            anomaly=1 if is_abnormal else 0,
                        )
                        cls_info.append(info_img)
                        
                        if phase == 'test':
                            if is_abnormal:
                                anomaly_samples += 1
                            else:
                                normal_samples += 1
                    except Exception as e:
                        print(f"Error processing row {idx}: {e}")
                        continue
                
                info[phase][cls_name] = cls_info
        
        with open(self.meta_path, 'w') as f:
            f.write(json.dumps(info, indent=4) + "\n")
        print('normal_samples', normal_samples, 'anomaly_samples', anomaly_samples)


import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate meta.json for VisA dataset')
    parser.add_argument('--root', type=str, default='/remote-home/iot_zhouqihang/data/Visa', help='Root directory of the dataset')
    args = parser.parse_args()
    runner = VisASolver(root=args.root)
    runner.run()
