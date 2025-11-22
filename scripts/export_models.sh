#!/usr/bin/env bash

EXPORT_DIR="exports"
MODELS_DIR="models"
YOLO_DATA_CONFIG="data/yolo_dataset/data.yaml"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
EXPORT_FILE="${EXPORT_DIR}/fire_detection_models_${TIMESTAMP}.zip"

echo ">> Creating export directory: ${EXPORT_DIR}"
mkdir -p "${EXPORT_DIR}"

if [ ! -d "${MODELS_DIR}" ]; then
  echo "ERROR: Models directory '${MODELS_DIR}' not found."
  echo "Train and save your models before exporting."
  exit 1
fi

echo ">> Preparing list of files to export..."

FILES_TO_EXPORT=()

# CNN model(s)
if ls ${MODELS_DIR}/*.h5 &> /dev/null; then
  FILES_TO_EXPORT+=(${MODELS_DIR}/*.h5)
fi

# YOLO model(s)
if ls ${MODELS_DIR}/*.pt &> /dev/null; then
  FILES_TO_EXPORT+=(${MODELS_DIR}/*.pt)
fi

# YOLO data config (if exists)
if [ -f "${YOLO_DATA_CONFIG}" ]; then
  FILES_TO_EXPORT+=("${YOLO_DATA_CONFIG}")
fi

# requirements and README (context)
if [ -f "requirements.txt" ]; then
  FILES_TO_EXPORT+=("requirements.txt")
fi

if [ -f "README.md" ]; then
  FILES_TO_EXPORT+=("README.md")
fi

if [ ${#FILES_TO_EXPORT[@]} -eq 0 ]; then
  echo "ERROR: No models or config files found to export."
  exit 1
fi

echo ">> Files to be exported:"
for f in "${FILES_TO_EXPORT[@]}"; do
  echo "   - ${f}"
done

echo ">> Creating ZIP: ${EXPORT_FILE}"
zip -r "${EXPORT_FILE}" "${FILES_TO_EXPORT[@]}"

echo ">> Export complete!"
echo "Generated file: ${EXPORT_FILE}"