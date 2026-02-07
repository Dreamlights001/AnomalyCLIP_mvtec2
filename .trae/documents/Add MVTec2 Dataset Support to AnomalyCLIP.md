# Add MVTec2 Dataset Support to AnomalyCLIP

## Overview
This plan outlines the steps to add support for the MVTec2 dataset to the AnomalyCLIP project, including generating the required meta.json file and updating dataset configuration.

## Implementation Steps

### 1. Create MVTec2 Dataset Generator Script
- Create a new file `generate_dataset_json/mvtec2.py`
- Implement a `MVTec2Solver` class similar to `MVTecSolver`
- Define the class names for MVTec2: ['can', 'fabric', 'fruit_jelly', 'rice', 'sheet_metal', 'vial', 'wallplugs', 'walnuts']
- Modify the directory structure handling to account for MVTec2's specific structure:
  - Test data in `test_public` with `bad`, `good`, and `ground_truth` subdirectories
  - Train data in `train/good`
- Generate meta.json file with appropriate paths

### 2. Update Dataset Configuration
- Modify `dataset.py` to add MVTec2 support:
  - Add 'mvtec2' case to the `generate_class_info` function
  - Include the MVTec2 class names in the object list

### 3. Update Path Configuration
- Update the dataset paths in shell scripts to point to `/root/autodl-tmp/datasets`
- Ensure the MVTec2 dataset path is correctly referenced

## Key Considerations
- The MVTec2 dataset has a different directory structure than MVTec, particularly with ground truth located under `test_public/ground_truth`
- Need to ensure the meta.json generation correctly handles this structure
- The class names for MVTec2 are different from MVTec and need to be properly registered

## Expected Output
- A new `mvtec2.py` script in the generate_dataset_json directory
- Updated `dataset.py` with MVTec2 support
- Ability to generate meta.json for MVTec2 dataset
- Ability to run AnomalyCLIP on MVTec2 dataset and output performance metrics