import platform
import subprocess
import sys
import time
from pathlib import Path


SCRIPTS_DIR = Path(__file__).parent / "scripts"


SCRIPT_MAP = {
    "setup_env": "setup_env",
    "download": "download_kaggle_dataset",
    "export_models": "export_models",
}


def detect_os():
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system in ("Linux", "Darwin"):
        return "unix"
    else:
        return "unknown"


def run_script(action: str):
    os_type = detect_os()
    if os_type == "unknown":
        print(f"[ERROR] Unknown OS: {platform.system()}")
        time.sleep(8.0)
        sys.exit(1)

    if action not in SCRIPT_MAP and action != "all":
        print(f"[ERROR] Unknown action: {action}")
        print("Valid actions: all, ".format(", ".join(SCRIPT_MAP.keys())))
        sys.exit(1)

    actions_to_run = (
        ["download", "setup_env", "export_models"] if action == "all" else [action]
    )

    for act in actions_to_run:
        base_name = SCRIPT_MAP[act]

        if os_type == "windows":
            script_path = SCRIPTS_DIR / f"{base_name}.ps1"
            if not script_path.exists():
                print(f"[ERROR] Script not found: {script_path}")
                sys.exit(1)

            cmd = [
                "powershell",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script_path),
            ]
        else:
            script_path = SCRIPTS_DIR / f"{base_name}.sh"
            if not script_path.exists():
                print(f"[ERROR] Script not found: {script_path}")
                time.sleep(8.0)
                sys.exit(1)

            script_path.chmod(script_path.stat().st_mode | 0o111)
            cmd = ["bash", str(script_path)]

        print(f"\n[INFO] Running '{act}' script: {script_path}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Fail to run '{act}'. error code: {e.returncode}")
            time.sleep(8.0)
            sys.exit(e.returncode)

    print("\n[OK] Succesfully completed the script.")


def print_usage():
    print("Choose an action:")
    print("  download       ")
    print("  setup_env      ")
    print("  export_models  - Exporta modelos treinados para um .zip em exports/")
    print("  all            - Run all scripts\n")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        action_arg = sys.argv[1].strip().lower()
    else:
        while (action_arg := input(f"{print_usage()}").strip().lower()) not in SCRIPT_MAP.keys():
            if action_arg == "all":
                break
            print(f"Invalid input: {action_arg}. Please enter one of {list(SCRIPT_MAP.keys())}.")
    run_script(action_arg)
