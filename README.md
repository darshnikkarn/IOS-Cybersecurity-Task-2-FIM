# File Integrity Monitor (FIM)

## Overview

This project is a File Integrity Monitor (FIM) developed in Python as part of the IOS Club Cybersecurity Technical Team Task 2.

The tool monitors files in a specified directory using SHA-256 cryptographic hashing. It creates a trusted baseline and detects file additions, modifications, and deletions.

The tool also provides a continuous watch mode for monitoring changes at regular intervals.

---

## Features

- SHA-256 cryptographic hashing
- Baseline creation and storage
- Detection of modified files
- Detection of newly added files
- Detection of deleted files
- Continuous monitoring using watch mode
- Multithreaded file hashing using `ThreadPoolExecutor`
- Command-line interface
- Configurable monitoring interval
- Error handling for missing or inaccessible files
- Logging of detected events

---

## Technologies Used

- Python 3.12+
- hashlib
- os
- json
- argparse
- logging
- time
- concurrent.futures

No external Python packages are required.

---

## Requirements

- Python 3.12 or later
- Windows / Linux / macOS
- No additional libraries are required

---

## Project Structure

```text
IOS-Cybersecurity-Task-2/
│
├── fim.py
├── baseline.json
├── fim.log
├── test_folder/
│   ├── test.txt
│   └── new_file.txt
│
└── screenshots/
    ├── 01-clean-baseline.png
    ├── 02-modified-file.png
    ├── 03-added-file.png
    ├── 04-deleted-file.png
    └── 05-watch-mode.png

## Demo Video

A short demonstration of the File Integrity Monitor showing baseline creation, integrity checking, file modification detection, and watch mode.

[Watch the FIM Demo Video](https://drive.google.com/file/d/1VnDx0jKZwbA6zduUQEEyLga1uxpv9uAM/view?usp=sharing)
