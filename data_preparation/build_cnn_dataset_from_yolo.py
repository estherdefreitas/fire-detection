from __future__ import annotations

from collections import Counter
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "kaggle_raw" / "Fire-Detection"
OUT_DIR = BASE_DIR / "data" / "cnn_dataset"

SPLITS = ["train", "valid", "test"]

CLASS_NAMES = {
    0: "fire",
    1: "smoke",
}


def find_image_for_label(images_dir: Path, stem: str) -> Path | None:
    for ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        candidate = images_dir / f"{stem}{ext}"
        if candidate.exists():
            return candidate
    return None


def main():
    print(f"[INFO] RAW_DIR: {RAW_DIR}")
    print(f"[INFO] OUT_DIR: {OUT_DIR}")

    for split in SPLITS:
        for cls_name in CLASS_NAMES.values():
            dest_dir = OUT_DIR / split / cls_name
            dest_dir.mkdir(parents=True, exist_ok=True)

    total_copied = 0
    copied_per_split_class = {split: Counter() for split in SPLITS}
    class_id_counter = Counter()

    for split in SPLITS:
        print(f"\n[INFO] Processing split: {split}")

        images_dir = RAW_DIR / split / "images"
        labels_dir = RAW_DIR / split / "labels"

        if not labels_dir.exists():
            print(f"[WARNING] Labels directory not found: {labels_dir}")
            continue

        label_files = list(labels_dir.glob("*.txt"))
        print(f"[INFO] Found {len(label_files)} files in {labels_dir}")

        for label_path in label_files:
            stem = label_path.stem  # file name without extension

            img_path = find_image_for_label(images_dir, stem)
            if img_path is None:
                print(f"[WARNING] No image found at {label_path.name}")
                continue

            with open(label_path, "r") as f:
                lines = [ln.strip() for ln in f if ln.strip()]

            if not lines:
                print(f"[WARN] Label empty: {label_path.name}")
                continue

            class_ids = []
            for ln in lines:
                parts = ln.split()
                try:
                    cid = int(float(parts[0]))  # first value is the class ID
                    class_ids.append(cid)
                    class_id_counter[cid] += 1
                except (ValueError, IndexError):
                    print(f"[WARNING] Invalid label: {ln}")
                    continue

            if not class_ids:
                print(f"[WARNING] No valid class on: {label_path.name}")
                continue

            if 0 in class_ids:
                cls_name = CLASS_NAMES[0]
            elif 1 in class_ids:
                cls_name = CLASS_NAMES[1]
            else:
                print(f"[WARNING] Unsupported classes at: {label_path.name}: {sorted(set(class_ids))}")
                continue

            dest_path = OUT_DIR / split / cls_name / img_path.name
            shutil.copy2(img_path, dest_path)

            copied_per_split_class[split][cls_name] += 1
            total_copied += 1

    print("\n[INFO] Distribution of class IDs found in the labels:")
    for cid, count in sorted(class_id_counter.items()):
        print(f"  class_id {cid}: {count} caixas")

    print("\n[OK] Created dataset at:", OUT_DIR)
    print("\n[INFO] Images per split/class copied:")
    for split in SPLITS:
        print(f"  Split {split}:")
        for cls_name in CLASS_NAMES.values():
            print(f"    {cls_name}: {copied_per_split_class[split][cls_name]} imagens")

    print(f"\n[OK] Total of images copied: {total_copied}")
    print(f"[OK] Classification dataset created at: {OUT_DIR}")

if __name__ == "__main__":
    main()
