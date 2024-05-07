import os
import shutil
import random
import json
import yaml

# Set the seed for reproducibility

random.seed(42)

# Function to copy files


def copy_files(files, set_type, images_path, labels_path, base_path):
    for file in files:  # Copy image
        shutil.copy(os.path.join(images_path, file), os.path.join(
            base_path, set_type, 'images'))  # Copy corresponding label
        label_file = file.rsplit('.', 1)[0] + '.txt'
        shutil.copy(os.path.join(labels_path, label_file),
                    os.path.join(base_path, set_type, 'labels'))


def generate_data_yml(base_path):
    with open(base_path+'/notes.json', 'r', encoding='utf-8') as f:
        notes = json.load(f)

    yml_data = {
        "train": "../train/images",
        "val": "../val/images",
        "test": "../test/images",
        "nc": len(notes["categories"]),
        "names": [category["name"] for category in notes["categories"]]
    }

    os.remove(base_path+'/notes.json')
    with open(base_path+'/data.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(yml_data, f, default_flow_style=False)


if __name__ == '__main__':
    # Paths
    base_path = 'datasets/dataset_1'

    images_path = os.path.join(base_path, 'images')
    labels_path = os.path.join(base_path, 'labels')

    # Split Ratios

    train_ratio = 0.70
    val_ratio = 0.15
    test_ratio = 0.15

    # Create directories for train, val, and test sets
    for set_type in ['train', 'val', 'test']:
        for content_type in ['images', 'labels']:
            os.makedirs(os.path.join(base_path, set_type,
                        content_type), exist_ok=True)

    # Get all image filenames
    all_files = [f for f in os.listdir(
        images_path) if os.path.isfile(os.path.join(images_path, f))]
    random.shuffle(all_files)

    # Calculate split indices
    total_files = len(all_files)
    train_end = int(train_ratio * total_files)
    val_end = train_end + int(val_ratio * total_files)

    # Split files
    train_files = all_files[:train_end]
    val_files = all_files[train_end:val_end]
    test_files = all_files[val_end:]

    copy_files(train_files, 'train', images_path, labels_path, base_path)
    copy_files(val_files, 'val', images_path, labels_path, base_path)
    copy_files(test_files, 'test', images_path, labels_path, base_path)

    generate_data_yml(base_path)
    print("Dataset successfully split into train, val, and test sets.")

    # Remove the original images and labels folder
    shutil.rmtree(f'{base_path}/images')
    shutil.rmtree(f'{base_path}/labels')
