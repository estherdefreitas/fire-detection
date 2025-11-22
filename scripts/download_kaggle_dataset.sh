#!/usr/bin/env bash

DATA_DIR="../data/kaggle_raw"
DATASET="metinmekiabullrahman/fire-detection"

echo ">> Creating data directory: ${DATA_DIR}"
mkdir -p "${DATA_DIR}"

echo ">> Checking Kaggle CLI..."
if ! command -v kaggle &> /dev/null; then
  echo "ERROR: kaggle CLI not found."
  echo "Install with: pip install kaggle"
  echo "And configure API token in ~/.kaggle/kaggle.json"
  exit 1
fi

echo ">> Downloading dataset from Kaggle: ${DATASET}"
kaggle datasets download -d "${DATASET}" -p "${DATA_DIR}" --unzip

echo ">> Download complete."
echo "Files are in: ${DATA_DIR}"