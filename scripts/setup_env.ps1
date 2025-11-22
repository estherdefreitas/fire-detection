$VENV = ".venv"

Write-Output ">> Checking Python..."
$PY = (Get-Command python -ErrorAction SilentlyContinue)

if (-not $PY) {
    Write-Error "Python not found. Install Python 3 first."
    exit 1
}

Write-Output ">> Creating venv in $VENV..."
python -m venv $VENV

Write-Output ">> Activating environment..."
& "$VENV\Scripts\Activate.ps1"

if (-not (Test-Path "requirements.txt")) {
    Write-Error "requirements.txt not found!"
    exit 1
}

Write-Output ">> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

Write-Output ">> Environment setup complete."