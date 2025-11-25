import os
import shutil
import random
from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).resolve().parents[2]  # volta 2 níveis até a raiz
RAW_DIR = BASE_DIR / "data" / "kaggle_raw"
OUT_DIR = BASE_DIR / "data" / "cnn_dataset"

CLASSES = ["fire", "no_fire"]
SPLITS = {
    "train": 0.7,
    "val": 0.15,
    "test": 0.15,
}


def create_dirs():
    for split in SPLITS.keys():
        for cls in CLASSES:
            dir_path = OUT_DIR / split / cls
            dir_path.mkdir(parents=True, exist_ok=True)


def split_and_copy():
    random.seed(42)

    for cls in CLASSES:
        src_dir = RAW_DIR / cls
        all_files = [f for f in src_dir.iterdir() if f.is_file()]
        random.shuffle(all_files)

        n_total = len(all_files)
        n_train = int(n_total * SPLITS["train"])
        n_val = int(n_total * SPLITS["val"])
        # resto vai para test
        n_test = n_total - n_train - n_val

        splits_files = {
            "train": all_files[:n_train],
            "val": all_files[n_train:n_train + n_val],
            "test": all_files[n_train + n_val:],
        }

        for split_name, files in splits_files.items():
            dest_dir = OUT_DIR / split_name / cls
            for f in files:
                shutil.copy2(f, dest_dir)


if __name__ == "__main__":
    create_dirs()
    split_and_copy()
    print("Dataset splited in train/val/test at:", OUT_DIR)
