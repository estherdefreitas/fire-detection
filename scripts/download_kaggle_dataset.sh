#!/usr/bin/env bash

$FIRE_DATASET  = "metinmekiabullrahman/fire-detection"
$FIRE_DIR      = "..\data\kaggle_raw\Fire-Detection"

$SMOKE_DATASET = "deepcontractor/smoke-detection-dataset"
$SMOKE_DIR     = "..\data\kaggle_raw\Smoke-Detection"

Write-Output ">> Checking kaggle CLI..."
if (-not (Get-Command kaggle -ErrorAction SilentlyContinue)) {
    Write-Error "ERROR: kaggle CLI not found. Install with 'pip install kaggle' and configure kaggle.json."
    exit 1
}

# --- FIRE DATASET ---
Write-Output "======================================="
Write-Output ">> Downloading FIRE dataset"
Write-Output "   Kaggle: $FIRE_DATASET"
Write-Output "   Target: $FIRE_DIR"
Write-Output "======================================="

New-Item -ItemType Directory -Force -Path $FIRE_DIR | Out-Null

kaggle datasets download -d $FIRE_DATASET -p $FIRE_DIR --unzip

# --- SMOKE DATASET ---
Write-Output ""
Write-Output "======================================="
Write-Output ">> Downloading SMOKE dataset"
Write-Output "   Kaggle: $SMOKE_DATASET"
Write-Output "   Target: $SMOKE_DIR"
Write-Output "======================================="

New-Item -ItemType Directory -Force -Path $SMOKE_DIR | Out-Null

kaggle datasets download -d $SMOKE_DATASET -p $SMOKE_DIR --unzip

Write-Output ""
Write-Output ">> Download complete."
Write-Output "   Fire dataset saved in:  $FIRE_DIR"
Write-Output "   Smoke dataset saved in: $SMOKE_DIR"