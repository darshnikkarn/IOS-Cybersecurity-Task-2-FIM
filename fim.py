import os
import json
import hashlib
import argparse
import time
import logging
from concurrent.futures import ThreadPoolExecutor


DEFAULT_BASELINE = "baseline.json"
DEFAULT_LOG = "fim.log"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                sha256.update(chunk)

        return file_path, sha256.hexdigest()

    except (PermissionError, OSError) as error:
        print(f"[ERROR] {file_path}: {error}")
        return file_path, None


def scan_directory(directory):
    file_paths = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)

            # Do not monitor the baseline/log files themselves
            if os.path.abspath(file_path) in {
                os.path.abspath(BASELINE_FILE),
                os.path.abspath(LOG_FILE)
            }:
                continue

            file_paths.append(file_path)

    files = {}

    # Multiple files are hashed simultaneously
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(calculate_hash, file_paths)

        for file_path, file_hash in results:
            if file_hash:
                files[file_path] = file_hash

    return files


def save_baseline(files):
    with open(BASELINE_FILE, "w") as file:
        json.dump(files, file, indent=4)

    print("[+] Baseline created successfully.")
    logging.info("Baseline created.")


def load_baseline():
    with open(BASELINE_FILE, "r") as file:
        return json.load(file)


def check_integrity(directory):
    try:
        old_files = load_baseline()
    except (FileNotFoundError, json.JSONDecodeError):
        print("[ERROR] Baseline does not exist or is invalid.")
        print("[INFO] Run --init first.")
        return

    new_files = scan_directory(directory)

    changes = False

    old_set = set(old_files)
    new_set = set(new_files)

    for file in sorted(new_set - old_set):
        print(f"[ADDED] {file}")
        logging.warning(f"ADDED: {file}")
        changes = True

    for file in sorted(old_set - new_set):
        print(f"[DELETED] {file}")
        logging.warning(f"DELETED: {file}")
        changes = True

    for file in sorted(old_set & new_set):
        if old_files[file] != new_files[file]:
            print(f"[MODIFIED] {file}")
            logging.warning(f"MODIFIED: {file}")
            changes = True

    if not changes:
        print("[OK] No changes detected.")


def watch_directory(directory, interval):
    print(f"[+] Monitoring: {directory}")
    print(f"[+] Checking every {interval} seconds.")
    print("[+] Press Ctrl+C to stop.\n")

    try:
        while True:
            check_integrity(directory)
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[+] Monitoring stopped.")


def main():
    global BASELINE_FILE, LOG_FILE

    parser = argparse.ArgumentParser(
        description="FIM - File Integrity Monitor"
    )

    parser.add_argument(
        "--directory",
        required=True,
        help="Directory to monitor"
    )

    parser.add_argument(
        "--init",
        action="store_true",
        help="Create a SHA-256 baseline"
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Check directory integrity"
    )

    parser.add_argument(
        "--watch",
        action="store_true",
        help="Continuously monitor the directory"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Watch interval in seconds (default: 5)"
    )

    parser.add_argument(
        "--baseline",
        default="baseline.json",
        help="Baseline file (default: baseline.json)"
    )

    parser.add_argument(
        "--log",
        default="fim.log",
        help="Log file (default: fim.log)"
    )

    args = parser.parse_args()

    BASELINE_FILE = args.baseline
    LOG_FILE = args.log

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    if not os.path.isdir(args.directory):
        print("[ERROR] Directory does not exist.")
        return

    selected_modes = sum([
        args.init,
        args.check,
        args.watch
    ])

    if selected_modes != 1:
        print("[ERROR] Choose exactly one of --init, --check, or --watch.")
        return

    if args.init:
        files = scan_directory(args.directory)
        save_baseline(files)

    elif args.check:
        check_integrity(args.directory)

    elif args.watch:
        if not os.path.exists(BASELINE_FILE):
            print("[ERROR] Baseline does not exist.")
            print("[INFO] Run --init first.")
            return

        watch_directory(args.directory, args.interval)


if __name__ == "__main__":
    main()