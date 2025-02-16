import os
import shutil
import json

# Define source and destination paths
source_dir = "dogs and cats"  # Change this to your dataset folder
dest_dir = "yolo_dataset"

# YOLO dataset structure
yolo_dirs = [
    "images/train",
    "images/val",
    "labels/train",
    "labels/val"
]

# Create YOLO structure
for yolo_dir in yolo_dirs:
    os.makedirs(os.path.join(dest_dir, yolo_dir), exist_ok=True)

# Define category mapping
categories = {"cat": 0, "dog": 1}  # Fix category names to match JSON labels

# Function to convert JSON annotations to YOLO format
def convert_json_to_yolo(json_path, img_width, img_height):
    with open(json_path, "r") as f:
        data = json.load(f)

    yolo_annotations = []

    # Ensure correct JSON format
    if not isinstance(data, list):
        print(f"⚠ Skipping {json_path} due to incorrect format")
        return []

    for entry in data:
        if "annotations" not in entry or "image" not in entry:
            continue  # Skip invalid entries

        for obj in entry["annotations"]:
            if not isinstance(obj, dict) or "label" not in obj or "coordinates" not in obj:
                continue  # Skip invalid annotations

            class_name = obj["label"].lower()  # Convert to lowercase for consistency
            if class_name not in categories:
                print(f"⚠ Unknown category '{class_name}' in {json_path}")
                continue  # Skip unknown categories

            class_id = categories[class_name]
            coords = obj["coordinates"]

            # Extract x, y, width, and height
            x, y, width, height = coords["x"], coords["y"], coords["width"], coords["height"]

            # Normalize for YOLO format (center_x, center_y, width, height)
            x_center = (x + width / 2) / img_width
            y_center = (y + height / 2) / img_height
            norm_width = width / img_width
            norm_height = height / img_height

            yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}")

    return yolo_annotations

# Function to process images and labels
def process_data(split):
    for category in ["cats", "dogs"]:
        img_src = os.path.join(source_dir, split, category)
        label_src = os.path.join(source_dir, split, category)

        img_dest = os.path.join(dest_dir, "images", split)
        label_dest = os.path.join(dest_dir, "labels", split)

        os.makedirs(img_dest, exist_ok=True)
        os.makedirs(label_dest, exist_ok=True)

        if not os.path.exists(img_src):
            print(f"⚠ Skipping {img_src}, directory not found!")
            continue

        for file in os.listdir(img_src):
            if file.endswith(".jpg") or file.endswith(".png"):
                # Copy image
                img_path = os.path.join(img_src, file)
                img_dest_path = os.path.join(img_dest, file)
                shutil.copy(img_path, img_dest_path)

                # Process annotation
                json_file = file.replace(".jpg", ".json").replace(".png", ".json")
                json_path = os.path.join(label_src, json_file)

                if os.path.exists(json_path):
                    # Assume image size (Replace with actual image size retrieval if needed)
                    image_width, image_height = 640, 640

                    yolo_annotations = convert_json_to_yolo(json_path, image_width, image_height)

                    if yolo_annotations:
                        # Write annotations to .txt file
                        label_file = os.path.join(label_dest, file.replace(".jpg", ".txt").replace(".png", ".txt"))
                        with open(label_file, "w") as f:
                            f.write("\n".join(yolo_annotations))
                    else:
                        print(f"⚠ No valid annotations found in {json_path}")

# Process train and val (test) data
process_data("train")
process_data("val")

# Create YOLO data.yaml file
data_yaml = f"""train: {os.path.abspath(dest_dir)}/images/train
val: {os.path.abspath(dest_dir)}/images/val

nc: 2
names: ['cat', 'dog']
"""

with open(os.path.join(dest_dir, "data.yaml"), "w") as f:
    f.write(data_yaml)

print(f"✅ YOLO dataset structure created at: {os.path.abspath(dest_dir)}")





'''
import os
import json
import cv2

# Define categories correctly
categories = {"cat": 0, "dog": 1}  # Ensure singular names

def convert_json_to_yolo(json_path, img_width, img_height):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        yolo_annotations = []

        # Check if JSON is a list or dict and extract annotations
        if isinstance(data, list):
            annotations = data[0].get("annotations", [])
        elif isinstance(data, dict) and "annotations" in data:
            annotations = data["annotations"]
        else:
            print(f"⚠ Skipping {json_path} due to unexpected format")
            return []

        for obj in annotations:
            if not isinstance(obj, dict) or "label" not in obj or "coordinates" not in obj:
                continue  # Skip invalid entries

            class_name = obj["label"].lower()  # Normalize label names
            if class_name not in categories:
                print(f"⚠ Unknown category '{class_name}' in {json_path}")
                continue  # Skip unknown categories

            class_id = categories[class_name]
            coords = obj["coordinates"]

            # Extract x, y, width, and height
            x, y, width, height = coords["x"], coords["y"], coords["width"], coords["height"]

            # Normalize for YOLO format
            x_center = (x + width / 2) / img_width
            y_center = (y + height / 2) / img_height
            norm_width = width / img_width
            norm_height = height / img_height

            yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}")

        if not yolo_annotations:
            print(f"⚠ No valid annotations found in {json_path}")

        return yolo_annotations

    except json.JSONDecodeError:
        print(f"❌ Error reading {json_path}: Invalid JSON format")
        return []
    except Exception as e:
        print(f"❌ Unexpected error processing {json_path}: {e}")
        return []

def process_data(img_dir, json_dir, label_dest):
    os.makedirs(label_dest, exist_ok=True)
    
    for file in os.listdir(img_dir):
        if file.endswith(".jpg") or file.endswith(".png"):
            image_path = os.path.join(img_dir, file)
            json_path = os.path.join(json_dir, file.replace(".jpg", ".json").replace(".png", ".json"))
            
            if not os.path.exists(json_path):
                print(f"⚠ Annotation file missing for {file}")
                continue

            # Get image dimensions
            img = cv2.imread(image_path)
            if img is None:
                print(f"❌ Error loading image {image_path}")
                continue
            img_height, img_width, _ = img.shape

            # Convert JSON annotations to YOLO format
            yolo_annotations = convert_json_to_yolo(json_path, img_width, img_height)

            if yolo_annotations:
                label_file = os.path.join(label_dest, file.replace(".jpg", ".txt").replace(".png", ".txt"))
                with open(label_file, "w") as f:
                    f.write("\n".join(yolo_annotations))
                print(f"✅ Processed {file} successfully")
            else:
                print(f"⚠ No valid annotations found in {json_path}")

# Example usage
image_directory = "dogs and cats/test/dogs"
json_directory = "dogs and cats/test/dogs"
label_output_directory = "D:/machine_learning/yolo_dataset"

process_data(image_directory, json_directory, label_output_directory)
'''