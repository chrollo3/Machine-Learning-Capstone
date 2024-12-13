import os
import shutil
import random

def split_existing_dataset(base_dir, output_dir, split_ratios=(0.8, 0.2), seed=42):
    """
    Membagi ulang dataset yang sudah ada dalam struktur train/test ke dalam train/val/test.

    Args:
        base_dir (str): Path ke folder dataset (yang memiliki train/ dan test/ di dalamnya).
        output_dir (str): Path output untuk dataset yang sudah dipisah ulang.
        split_ratios (tuple): Proporsi pembagian untuk train dan validation dari `train/`.
        seed (int): Seed untuk random shuffling agar hasil konsisten.
    """
    random.seed(seed)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for split in ['train', 'test']:
        split_dir = os.path.join(base_dir, split)
        
        for class_name in os.listdir(split_dir):
            class_dir = os.path.join(split_dir, class_name)
            
            if not os.path.isdir(class_dir):
                continue
            
            images = os.listdir(class_dir)
            random.shuffle(images)
            
            if split == 'train':
                train_split = int(split_ratios[0] * len(images))
                train_images = images[:train_split]
                val_images = images[train_split:]
                
                for subset, subset_images in [('train', train_images), ('val', val_images)]:
                    subset_dir = os.path.join(output_dir, subset, class_name)
                    os.makedirs(subset_dir, exist_ok=True)
                    for image in subset_images:
                        shutil.copy2(os.path.join(class_dir, image), os.path.join(subset_dir, image))
            elif split == 'test':
                test_dir = os.path.join(output_dir, 'test', class_name)
                os.makedirs(test_dir, exist_ok=True)
                for image in images:
                    shutil.copy2(os.path.join(class_dir, image), os.path.join(test_dir, image))
    
    print(f"Dataset berhasil diproses dan dibagi ke folder: {output_dir}")

base_dataset_dir = 'dataset'
output_dataset_dir = 'dataset/split'

split_existing_dataset(base_dataset_dir, output_dataset_dir)
