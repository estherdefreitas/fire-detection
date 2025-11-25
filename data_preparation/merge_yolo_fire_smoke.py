from pathlib import Path
import shutil


BASE_DIR = Path(__file__).resolve().parents[1]

FIRE_ROOT = BASE_DIR / "data" / "kaggle_raw" / "Fire-Detection"
SMOKE_ROOT = BASE_DIR / "data" / "kaggle_raw" / "Fire-and-Smoke"

OUT_ROOT = BASE_DIR / "data" / "yolo_dataset"
IMG_OUT_TRAIN = OUT_ROOT / "images" / "train"
IMG_OUT_VAL = OUT_ROOT / "images" / "val"
LBL_OUT_TRAIN = OUT_ROOT / "labels" / "train"
LBL_OUT_VAL = OUT_ROOT / "labels" / "val"


def ensure_dirs():
    for p in [IMG_OUT_TRAIN, IMG_OUT_VAL, LBL_OUT_TRAIN, LBL_OUT_VAL]:
        p.mkdir(parents=True, exist_ok=True)


def copy_yolo_split(src_root: Path, split_name_src: str, split_name_dst: str):

    images_dir = src_root / split_name_src / "images"
    labels_dir = src_root / split_name_src / "labels"

    if not images_dir.exists() or not labels_dir.exists():
        print(f"[WARN] Did not find images/labels in {images_dir} / {labels_dir}")
        return

    if split_name_dst == "train":
        img_out = IMG_OUT_TRAIN
        lbl_out = LBL_OUT_TRAIN
    else:
        img_out = IMG_OUT_VAL
        lbl_out = LBL_OUT_VAL

    img_files = [f for f in images_dir.iterdir() if f.is_file()]
    print(f"[INFO] Copying {len(img_files)} images from {images_dir} para {img_out}")

    for img_path in img_files:
        stem = img_path.stem
        lbl_src = labels_dir / f"{stem}.txt"

        if not lbl_src.exists():
            print(f"[WARN] No label for {img_path.name}, skipping.")
            continue

        shutil.copy2(img_path, img_out / img_path.name)
        shutil.copy2(lbl_src, lbl_out / lbl_src.name)


def main():
    ensure_dirs()

    print("=== Copying Fire-Detection dataset (fire only) ===")
    # Fire-Detection usa 'train', 'valid' (pelo seu log anterior)
    copy_yolo_split(FIRE_ROOT, "train", "train")
    copy_yolo_split(FIRE_ROOT, "valid", "val")

    print("\n=== Copying FireSmoke-YOLOv9 dataset (fire + smoke) ===")
    # No dataset novo pode ser 'train' e 'val' (ou 'valid'), ajuste se necessário
    copy_yolo_split(SMOKE_ROOT, "train", "train")
    # Tenta val e valid
    if (SMOKE_ROOT / "val").exists():
        copy_yolo_split(SMOKE_ROOT, "val", "val")
    elif (SMOKE_ROOT / "valid").exists():
        copy_yolo_split(SMOKE_ROOT, "valid", "val")

    print("\n[OK] Merge completed. Combined dataset at:", OUT_ROOT)


if __name__ == "__main__":
    main()