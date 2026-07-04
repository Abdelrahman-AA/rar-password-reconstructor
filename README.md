# RAR Password Permutation Tool (WIP)

A smart, structured brute-force tool written in Python designed to recover lost or forgotten RAR file passwords. Unlike standard brute-force tools that try random characters, this tool relies on pre-defined string components (**Chunks**) and structures them using custom permutation logic to intelligently reconstruct the target password.

> ⚠️ **Status: Work In Progress (WIP)**
> > This project is currently under active development. The core layout logic and permutation architecture are complete, but performance optimizations (such as multi-threading and direct archive handling) are currently planned for future updates.

---

## ✨ Features
- **Structured Permutations:** Dynamically group-combines words, characters, or phrases instead of testing endless random character combinations.
- **Smart Constraints:** Supports pre-calculated constraints to save CPU cycles:
  - **Mandatory Elements:** Ensure specific blocks *must* appear in the password.
  - **Fixed Positions:** Force a specific block to always stay at a designated position in the chain.
  - **Alternative Variations:** Define lists of interchangeable words or symbols for a specific position.
- **WinRAR / UnRAR Integration:** Directly interfaces with the system's `unrar` CLI utility to safely test and validate generated password strings.

---

## 🛠️ Requirements & Setup

### 1. Prerequisites
- **Python 3.x** installed on your system.
- **WinRAR / UnRAR Command Line Tool:**
  - **Windows:** The script looks for UnRAR at `C:\Program Files\WinRAR\UnRAR.exe` by default. If installed elsewhere, make sure `unrar` is added to your system's Environment Variables (PATH).
  - **Linux / macOS:** Ensure `unrar` is installed and accessible via your terminal (e.g., `sudo dnf install unrar` or `sudo apt install unrar`).

### 2. Project Layout
Keep your RAR file and your chunks configuration file in an accessible directory:
```text
├── rar_cracker.py
├── target_file.rar
└── chunks.txt
```

## 📝 Preparing the Chunks File (`chunks.txt`)

The script reads a text file (`chunks.txt`) containing the building blocks of the potential password. You can configure how the script processes these blocks using specific prefixes and bracket rules.

### 🔍 Rules and Syntax Guide

*   **Standard Block:** A simple line without any formatting. The script will use the entire line text as-is.
*   **Alternative Block `(...)`:** Words grouped inside parentheses and separated by commas or hyphens. The script will pick **only one** variation from this group to test per permutation.
*   **Mandatory Block `[M]`:** Placing `[m]` or `[M]` before a block forces the script to **only** test password variations that contain this specific chunk.
*   **Fixed Position Block `[N]`:** Placing a number before a block forces this chunk to strictly sit at that precise index (1-based index) in the generated password sequence.

---

### 📋 Example `chunks.txt` Configuration

```text
# Case 1: Simple blocks that will be mixed together
Admin
2026

# Case 2: Alternative variations (The tool will test either 'Password', 'Pass', or 'P@ss')
(Password, Pass - P@ss)

# Case 3: Mandatory block (This MUST be included in the password sequence)
[M] @#$

# Case 4: Fixed position (This block MUST always be the 1st element in the password)
[1] CompanyName
```

## 🚀 How to Run

1.  Open your terminal or command prompt.
2.  Navigate to the directory containing the script.
3.  Execute the tool using the following command:
    ```bash
    python rar_cracker.py
    ```
4.  Follow the interactive CLI prompts:
    *   **Enter RAR file path:** Provide the path to your target `.rar` archive (you can drag and drop the file into the terminal).
    *   **Enter text file path containing chunks:** Provide the path to your configured `chunks.txt` file.
    *   **Enter MINIMUM elements to combine:** Specify the lower bound of elements to chain together.
    *   **Enter MAXIMUM elements to combine:** Specify the upper bound of elements to chain together.

---

## 🚧 Road Map & Upcoming Improvements

- [ ]  Implement **Multiprocessing / Multi-threading** to distribute password testing workloads across all available CPU cores.
- [ ]  Transition from CLI subprocess spawns to native Python archive libraries or **Hashcat/John the Ripper** integration to drastically increase passwords-per-second capabilities.
- [ ]  Add real-time performance metrics (e.g., attempt speeds, estimated time remaining).
- [ ]  Improve memory management for massive chunk configuration lists.

---

## 🤝 Contributing

Contributions, bug reports, and performance optimization ideas are highly welcome! Since this project is currently a **Work in Progress (WIP)**, feel free to fork this repository, open issues, or submit pull requests with your enhancements.

## ✒️ Author

Developed with 💻 by **Abdelrahman Abodief**.
