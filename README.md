<div align="center">

```
███████ ██ ██      ███████ ███████ ██   ██  █████       ██  █████   ██████  
██      ██ ██      ██      ██      ██   ██ ██   ██      ██ ██   ██ ██    ██ 
█████   ██ ██      █████   ███████ ███████ ███████      ██ ███████ ██    ██ 
██      ██ ██      ██           ██ ██   ██ ██   ██ ██   ██ ██   ██ ██    ██ 
██      ██ ███████ ███████ ███████ ██   ██ ██   ██  █████  ██   ██  ██████  
```
### FileShajao v1.0

**Developed By: Current Vai ♚**

[![GitHub](https://img.shields.io/badge/GitHub-YourUsername-blue?style=for-the-badge&logo=github)](https://github.com/currentvai)
[![Telegram](https://img.shields.io/badge/Telegram-Channel-blue?style=for-the-badge&logo=telegram)](https://t.me/currentvai)

</div>

---

A powerful and interactive script for Android (via Termux) to automatically organize files in any folder based on their extensions.

## 🌟 Features

-   Interactive command-line interface.
-   Choose between Internal Storage and External SD Card.
-   Automatically lists all folders for you to choose from.
-   Organizes files into new folders named after their extensions (e.g., `.jpg` files go to a `jpg` folder).
-   Colorful and user-friendly output.

## 📲 Installation & Usage (for Android/Termux)

1.  **Install Termux:**
    Download and install Termux from **[F-Droid](https://f-droid.org/en/packages/com.termux/)**. The Google Play Store version is outdated and will not work.

2.  **Update & Install Packages:**
    Open Termux and run the following commands to install `git` and `python`:
    ```bash
    pkg update && pkg upgrade -y
    pkg install python git -y
    ```

3.  **Grant Storage Permission:**
    This is a **critical step**. You must give Termux permission to access your files.
    ```bash
    termux-setup-storage
    ```
    A pop-up will appear on your phone. Tap **"Allow"**.

4.  **Clone This Repository:**
    ```bash
    git clone https://github.com/currentvai/FileShajao.git
    ```

5.  **Run the Script:**
    Navigate into the cloned directory and run the Python script:
    ```bash
    cd FileShajao
    python shajao.py
    ```

Now just follow the on-screen instructions to select your storage and folder!

---

> Copyright (c) 2024 Current Vai
>
> **All Rights Reserved.**
>
> Unauthorized copying of this file, via any medium is strictly prohibited.
>
> "I am completely destroyed. Error 304 Not Modified."
