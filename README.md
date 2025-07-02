<div align="center">

# FileShajao v4.0

**An Intelligent File Manager & Cleaner for Your Android Device**

*Developed By: Current Vai ♚*

---
<div align="center">

```
███████ ██ ██      ███████ ███████ ██   ██  █████       ██  █████   ██████  
██      ██ ██      ██      ██      ██   ██ ██   ██      ██ ██   ██ ██    ██ 
█████   ██ ██      █████   ███████ ███████ ███████      ██ ███████ ██    ██ 
██      ██ ██      ██           ██ ██   ██ ██   ██ ██   ██ ██   ██ ██    ██ 
██      ██ ███████ ███████ ███████ ██   ██ ██   ██  █████  ██   ██  ██████  
```

---

<!-- Add a link to your logo here -->
<img src="assets/image/logo.png" alt="FileShajao Logo" width="300"/>

# FileShajao v4.0

**An Intelligent File Manager & Cleaner for Your Android Device**

*Developed By: Current Vai ♚*

<p>
  <img src="https://img.shields.io/badge/Version-2.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/License-All_Rights_Reserved-red.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Termux_on_Android-green.svg" alt="Platform">
</p>
<p>
  <a href="https://github.com/currentvai" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-currentvai-blue?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="https://t.me/currentvai" target="_blank">
    <img src="https://img.shields.io/badge/Telegram-currentvai-blue?style=for-the-badge&logo=telegram" alt="Telegram">
  </a>
</p>

</div>

---

**`FileShajao`** is a powerful command-line utility designed to bring order to the chaos of your Android's storage. It simplifies file organization, detects and removes duplicate files, and helps you reclaim precious space, all while ensuring your data remains safe with robust features like **Undo** and a **Recycle Bin**.

### ✨ Core Features

| Feature | Description | Icon |
| :--- | :--- | :---: |
| **File Organizer** | Automatically sorts files in any directory into sub-folders based on their extension. | 📂 |
| **Duplicate Cleaner**| Uses multi-threading to rapidly find duplicate files and offers to move them to the recycle bin. | 🧬 |
| **Undo/Revert** | Accidentally rearranged a folder? Revert the entire operation with a single command. | ↩️ |
| **Safe Recycle Bin** | Deleted files are not lost forever. They are moved to a secure trash folder (`.FileShajaoTrash`) for easy recovery. | 🗑️ |
| **Interactive Navigation**| A colorful and intuitive interface for browsing your directories with ease. | 🗺️ |
| **Logging System** | Every action is recorded in a detailed log file (`fileshajao.log`), perfect for tracking and debugging. | 📝 |
| **Progress Bars** | Beautiful progress bars keep you informed during time-consuming tasks like hashing or moving files. | ⏳ |

---

### 📲 Installation

**Prerequisite:** You must have the **Termux** app installed on your Android device (preferably from F-Droid).

---

#### Method 1: Step-by-Step Installation (Recommended for New Users)

**Step 1: Prepare Termux**

# Update and upgrade all packages
```bash
pkg update && pkg upgrade -y
```

# Install required tools (Python and Git)
```bash
pkg install python git -y
```

# Install the 'tqdm' library for progress bars
```bash
pip install tqdm
```

# Grant storage permission (CRITICAL STEP)
```bash
termux-setup-storage
```

# A pop-up will appear on your phone. You MUST tap "Allow".

**Step 2: Download FileShajao**
# Clone the repository from GitHub
```bash
git clone https://github.com/currentvai/FileShajao.git
```

**Step 3: Run the Tool**
# Navigate into the project directory
```bash
cd FileShajao
```

# Run the script
```bash
python shajao.py
```
And you're all set! The tool will now start.

---

#### Method 2: One-Liner Installation (For Advanced Users)

This single command will perform all setup, download, and execution steps at once. Just copy, paste, and run.

```bash
pkg update -y && pkg upgrade -y && pkg install python git -y && pip install tqdm && termux-setup-storage && git clone https://github.com/currentvai/FileShajao.git && cd FileShajao && python shajao.py
```
*(Note: You will still need to manually tap "Allow" when the storage permission pop-up appears.)*

---

### ⚙️ How to Use

After launching the tool, you will be greeted with a user-friendly menu:

1.  **Rearrange Files:** Organizes files in the selected folder into sub-directories based on their file extensions.
2.  **Find & Delete Duplicate Files:** Scans the folder for duplicate files and gives you the option to move them to the Recycle Bin.
3.  **Undo Last Rearrange:** If you accidentally rearrange a folder, this option will restore all files to their original locations.
4.  **Manage Recycle Bin:** View, restore, or permanently delete files from the `.FileShajaoTrash` folder.

### 🛡️ Safety First!

A single wrong command can create a mess. That's why `FileShajao` is built with two powerful safety nets:

*   **Undo Last Rearrange:** Your file organization tasks are risk-free. A detailed log file allows you to revert any rearrangement instantly.
*   **Recycle Bin:** Your deleted files are not gone for good. They are safely stored in a hidden trash folder for later recovery.

### 🤝 Contributing

Contributions are welcome! If you have ideas for new features, bug reports, or code improvements, please feel free to open an issue or submit a pull request.

### 📜 License

Copyright (c) 2025 Current Vai.

**All Rights Reserved.**

Unauthorized copying of this file, via any medium, is strictly prohibited. This software is proprietary and confidential.

---
<div align="center">
"I am completely destroyed. Error 304 Not Modified."
</div>
