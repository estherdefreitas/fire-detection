$DATA_DIR = "..\data\kaggle_raw"
$DATASET = "metinmekiabullrahman/fire-detection"

Write-Output ">> Creating directory $DATA_DIR"
New-Item -ItemType Directory -Force -Path $DATA_DIR | Out-Null

if (-not (Get-Command kaggle -ErrorAction SilentlyContinue)) {
    Write-Error "ERROR: kaggle CLI not found. Install with 'pip install kaggle'"
    exit 1
}

Write-Output ">> Downloading dataset..."
kaggle datasets download -d $DATASET -p $DATA_DIR --unzip

Write-Output ">> DONE! Files saved in $DATA_DIR"