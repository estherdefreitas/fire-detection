$EXPORT_DIR = "exports"
$MODELS_DIR = "models"
$YOLO_CONFIG = "data\yolo_dataset\data.yaml"

$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$ZIP_FILE = "$EXPORT_DIR\fire_detection_$TIMESTAMP.zip"

New-Item -ItemType Directory -Force -Path $EXPORT_DIR | Out-Null

if (-not (Test-Path $MODELS_DIR)) {
    Write-Error "Models folder not found!"
    exit 1
}

$files = @()

$files += Get-ChildItem "$MODELS_DIR\*.h5" -ErrorAction SilentlyContinue
$files += Get-ChildItem "$MODELS_DIR\*.pt" -ErrorAction SilentlyContinue
if (Test-Path $YOLO_CONFIG) { $files += $YOLO_CONFIG }
if (Test-Path "README.md") { $files += "README.md" }
if (Test-Path "requirements.txt") { $files += "requirements.txt" }

if ($files.Count -eq 0) {
    Write-Error "No model files found to export."
    exit 1
}

Write-Output ">> Creating ZIP file: $ZIP_FILE"
Compress-Archive -Path $files -DestinationPath $ZIP_FILE -Force

Write-Output ">> Export complete!"
Write-Output "Saved as: $ZIP_FILE"