<div align="center">

# 🌊 FILEFLOOD

### Advanced File Size Generation & Testing Utility

![Platform](https://img.shields.io/badge/Platform-Linux-111111?style=for-the-badge&logo=linux&logoColor=white)
![Language](https://img.shields.io/badge/Language-Python-111111?style=for-the-badge&logo=python&logoColor=white)
![Interface](https://img.shields.io/badge/Interface-CLI-111111?style=for-the-badge&logo=gnubash&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-None-111111?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0.0-111111?style=for-the-badge)

<br>

<img src="screenshots/fileflood-main.png" width="900">

<br>

**Generate • Pump • Inspect • Hash • Test • Benchmark**

</div>

---

# 🌊 FileFlood

**FileFlood** is a lightweight, interactive CLI utility for Linux designed to generate, expand, inspect, and test files of custom sizes.

It provides an easy-to-use terminal interface for working with files in **KB, MB, and GB**, without requiring complicated command-line arguments.

Built entirely with Python's standard library, FileFlood runs as a **single Python script with zero external Python dependencies**.

---

# 🚀 Features

| Feature | Description |
|---|---|
| 📁 Create New File | Generate files with custom sizes |
| 📈 Pump Existing File | Increase the size of an existing file |
| 🎯 Target Size | Automatically expand a file to a desired final size |
| 📏 KB / MB / GB | Work with multiple file-size units |
| 🧱 Data Patterns | Zero, Random and Repeating data |
| ⚡ Sparse Files | Create large logical files efficiently |
| 📊 Progress Display | Live percentage, speed and ETA |
| 💾 Disk Protection | Check available storage before large writes |
| 🔍 File Information | Inspect file metadata and properties |
| 🔐 Hash / Integrity | MD5, SHA-1, SHA-256 and SHA-512 |
| 🧪 Boundary Testing | Generate files around size boundaries |
| 💽 Disk Benchmark | Measure sequential write performance |
| 🎨 Hacker-Style CLI | Colored terminal interface and ASCII branding |
| 🖥️ Interactive Menu | No complicated commands required |
| 🐍 Single Python File | Core application contained in one `.py` file |
| 📦 Zero Dependencies | Uses Python standard library |

---

# 🖥️ Interface

FileFlood uses an interactive terminal menu instead of requiring users to remember multiple commands.

```text
┌─────────────────────────────┐
│        FILEFLOOD MENU       │
└─────────────────────────────┘

[1] Create New File
[2] Pump Existing File
[3] File Information
[4] Hash / Integrity
[5] Boundary Testing
[6] Disk Benchmark
[7] Settings
[8] About
[9] Exit

Select an option:
