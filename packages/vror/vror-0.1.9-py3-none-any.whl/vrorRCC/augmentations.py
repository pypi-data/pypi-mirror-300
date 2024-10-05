import os
import random
from PIL import Image, ImageEnhance
import numpy as np

# Augmentation functions
def rotate(image, angle):
    return image.rotate(angle)

def flip_horizontal(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def flip_vertical(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def add_noise(image, noise_level=25):
    img_array = np.array(image)
    noise = np.random.normal(0, noise_level, img_array.shape)
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img)

# Apply augmentations to a single image
def apply_augmentations(image_path, num_augmentations=3):
    original_image = Image.open(image_path).convert('RGB')
    augmentation_functions = [rotate, flip_horizontal, flip_vertical, adjust_brightness, add_noise]
    
    augmented_images = []
    for _ in range(num_augmentations):
        augmented_image = original_image.copy()
        num_operations = random.randint(1, 3)
        
        for _ in range(num_operations):
            aug_func = random.choice(augmentation_functions)
            if aug_func == rotate:
                augmented_image = aug_func(augmented_image, random.uniform(-30, 30))
            elif aug_func == adjust_brightness:
                augmented_image = aug_func(augmented_image, random.uniform(0.5, 1.5))
            elif aug_func == add_noise:
                augmented_image = aug_func(augmented_image)
            else:
                augmented_image = aug_func(augmented_image)
        
        augmented_images.append(augmented_image)
    return augmented_images

# Process all images in the dataset
def process_dataset(input_dir, output_dir="Augmented_DataSet", num_augmentations=3):
    os.makedirs(output_dir, exist_ok=True)
    
    for dirpath, dirnames, filenames in os.walk(input_dir):
        relative_path = os.path.relpath(dirpath, input_dir)
        output_subdir = os.path.join(output_dir, relative_path)
        os.makedirs(output_subdir, exist_ok=True)
        
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            img = Image.open(file_path)
            if not filename.endswith('.png'):
                filename = os.path.splitext(filename)[0] + '.png'
                file_path = os.path.join(output_subdir, filename)
                img = img.convert("RGB")
                img.save(file_path)
            else:
                img.save(os.path.join(output_subdir, filename))
            
            augmented_images = apply_augmentations(file_path, num_augmentations)
            
            for idx, augmented_image in enumerate(augmented_images):
                output_image_path = os.path.join(
                    output_subdir, f"augmented_{idx+1}_{filename}"
                )
                augmented_image.save(output_image_path)

