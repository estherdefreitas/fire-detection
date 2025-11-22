#!/usr/bin/env bash
VENV_DIR=".venv"

echo ">> Detecting Python executable..."

if command -v python3 &> /dev/null; then
  PYTHON_BIN="python3"
elif command -v python &> /dev/null; then
  PYTHON_BIN="python"
else
  echo "ERROR: Python not found. Install Python 3 first."
  exit 1
fi

echo ">> Using Python: ${PYTHON_BIN}"

if [ ! -d "${VENV_DIR}" ]; then
  echo ">> Creating virtual environment in ${VENV_DIR}"
  ${PYTHON_BIN} -m venv "${VENV_DIR}"
else
  echo ">> Virtual environment ${VENV_DIR} already exists. Skipping creation."
fi

# Aviso: a ativação só vale se você rodar com "source"
echo ">> To activate the virtual environment, run:"
echo "   source ${VENV_DIR}/bin/activate   # Linux/macOS"
echo "   ${VENV_DIR}\\Scripts\\activate    # Windows (PowerShell/CMD)"
echo

# Ativa o venv neste script para instalar as dependências
# (não afeta o shell pai, mas é suficiente para este comando)
if [ -f "${VENV_DIR}/bin/activate" ]; then
  # Linux / macOS
  source "${VENV_DIR}/bin/activate"
elif [ -f "${VENV_DIR}/Scripts/activate" ]; then
  # Windows Git Bash
  source "${VENV_DIR}/Scripts/activate"
else
  echo "ERROR: Could not find activate script in ${VENV_DIR}."
  exit 1
fi

if [ ! -f "requirements.txt" ]; then
  echo "ERROR: requirements.txt not found in project root."
  exit 1
fi

echo ">> Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo ">> Environment setup complete."