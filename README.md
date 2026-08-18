# 🌊 FILEFLOOD

## ⚡ Advanced File Size Generation & Testing Utility

FileFlood is a lightweight, interactive CLI utility built with Python for generating, expanding, inspecting, hashing, benchmarking, and testing files of custom sizes.

Instead of remembering complicated terminal commands, FileFlood provides an interactive menu that guides you through every operation.

No external Python packages.  
No database.  
No network connection.  
No complicated arguments.

Just run the script and select what you want to do.

---

## 🚀 FEATURES

📁 CREATE NEW FILE  
Generate files using custom sizes in KB, MB, and GB.

📈 PUMP EXISTING FILE  
Increase the size of an already existing file using Add Size or Target Size.

🔍 FILE INFORMATION  
Inspect filename, location, size, bytes, permissions, modified time, and file type.

🔐 HASH / INTEGRITY  
Calculate MD5, SHA-1, SHA-256, and SHA-512 hashes.

🧪 BOUNDARY TESTING  
Generate files around a selected size boundary.

💽 DISK BENCHMARK  
Perform a basic sequential write benchmark.

⚡ SPARSE FILE SUPPORT  
Create large logical files without immediately writing the entire amount of data.

📊 LIVE PROGRESS  
Display percentage, write speed, ETA, and processed data.

💾 DISK SPACE CHECK  
Check available storage before large file-generation operations.

🎨 COLORED TERMINAL  
ANSI colors for a clean hacker-style CLI.

🖥️ INTERACTIVE MENU  
No complicated command-line arguments required.

---

## 🖥️ MAIN MENU

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
```

---

## 📸 Screenshots 

<img src="[https://i.postimg.cc/LXVfDDMq/Screenshot-2026-08-18-06-51-25.png]">

# 📁 CREATE NEW FILE

Choose:

```text
[1] Create New File
```

FileFlood guides you through filename, size, unit, data pattern, and file mode.

Supported units:

```text
KB
MB
GB
```

Example:

```text
Filename : test.bin
Size     : 500
Unit     : MB
```

---

# 📈 PUMP EXISTING FILE

Choose:

```text
[2] Pump Existing File
```

Then select:

```text
[1] Add Size
[2] Set Target Size
```

### ADD SIZE

```text
Current File : 500 MB
Add Size     : 1 GB
Final Size   : ~1.50 GB
```

### TARGET SIZE

```text
Current File : 500 MB
Target Size  : 2 GB
Required     : ~1.50 GB
```

FileFlood calculates the required difference automatically.

---

# 🧱 DATA PATTERNS

### ZERO DATA

```text
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
```

### RANDOM DATA

```text
A7 19 F2 8C 44 91 2D 7A
3B 81 E0 42 9F 11 C4 68
```

### REPEATING DATA

```text
FILEFLOODFILEFLOODFILEFLOOD
FILEFLOODFILEFLOODFILEFLOOD
```

---

# ⚡ SPARSE FILES

FileFlood can create sparse files.

```text
Logical Size : 10 GB
Physical Use : Potentially much smaller
```

Sparse files behave differently from normal files, so always check actual physical disk usage.

---

# 📊 LIVE PROGRESS

Example:

```text
[████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░] 48.23%

Speed : 125.43 MB/s
ETA   : 4.2s
```

---

# 🔍 FILE INFORMATION

Choose:

```text
[3] File Information
```

FileFlood can display:

```text
Name
Location
Size
Size in Bytes
Permissions
Modified Time
File Type
```

Example:

```text
Name       : test.bin
Location   : /home/user/test.bin
Size       : 100.00 MB
Bytes      : 104857600
Permissions: 644
Type       : Regular file
```

---

# 🔐 HASH / INTEGRITY

Choose:

```text
[4] Hash / Integrity
```

Supported:

```text
MD5
SHA-1
SHA-256
SHA-512
```

Example:

```text
SHA-256 : 9f86d081884c7d659a2feaa0c55ad015...
```

Files are processed in chunks rather than loading the entire file into memory.

---

# 🧪 BOUNDARY TESTING

Choose:

```text
[5] Boundary Testing
```

Example:

```text
Base Size : 100 MB
```

Generated boundary sizes:

```text
99 MB
99.5 MB
100 MB
100.5 MB
101 MB
```

Output directory:

```text
fileflood_boundary_tests/
```

Useful for file-size limits, upload limits, application testing, storage testing, and boundary conditions.

---

# 💽 DISK BENCHMARK

Choose:

```text
[6] Disk Benchmark
```

Process:

```text
Create Temporary File
        ↓
Write Test Data
        ↓
Measure Elapsed Time
        ↓
Calculate Write Speed
        ↓
Display Result
        ↓
Remove Temporary File
```

Example:

```text
Write Speed : 180.52 MB/s
```

---

# 💾 DISK SPACE PROTECTION

Example:

```text
Requested : 50 GB
Available : 12 GB

✗ INSUFFICIENT DISK SPACE
```

Always verify the requested size and destination before large operations.

---

# 🎨 TERMINAL COLORS

```text
CYAN      → Branding / Main Interface
GREEN     → Successful Operations
YELLOW    → Warnings / Prompts
RED       → Errors / Exit
MAGENTA   → Menus / Sections
WHITE     → General Information
GRAY      → Secondary Information
```

---

# 🧠 HOW FILEFLOOD WORKS

```text
                         FILEFLOOD
                             │
                             ▼
                       MAIN MENU
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
       CREATE              PUMP               INFO
          │                  │                  │
          ▼                  ▼                  ▼
       Generate            Expand             Inspect
         File              File               File
          │                  │
     ┌────┼────┐             │
     ▼    ▼    ▼             │
    ZERO RANDOM REPEAT       │
     │    │    │             │
     └────┼────┘             │
          │                  │
          └────────┬─────────┘
                   ▼
            FILE OPERATIONS
                   │
                   ▼
            PROGRESS ENGINE
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
        SPEED     ETA    PERCENTAGE
                   │
                   ▼
          HASH / TEST / BENCHMARK
```

---

# 🛠️ TECHNOLOGY

```text
Language        : Python 3
Interface       : Interactive CLI
Platform        : Linux
Dependencies    : Python Standard Library
External APIs   : None
Database        : None
Network         : None
Main Program    : fileflood.py
Architecture    : Single Python Script
```

---

# 📦 REQUIREMENTS

```text
Python 3.x
Linux
ANSI-compatible terminal
```

No external Python packages are required.

---

# ⚙️ INSTALLATION

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FileFlood
chmod +x fileflood.py
./fileflood.py
```

Or:

```bash
python3 fileflood.py
```

---

# ⚡ QUICK START

Launch:

```bash
python3 fileflood.py
```

Then select:

```text
[1] Create New File
```

or:

```text
[2] Pump Existing File
```

and follow the prompts.

---

# 📂 PROJECT STRUCTURE

```text
FileFlood/
│
├── fileflood.py
├── README.md
├── LICENSE
├── .gitignore
│
└── screenshots/
    └── fileflood-main.png
```

Recommended `.gitignore`:

```text
__pycache__/
*.pyc
*.pyo
*.tmp
*.bin
fileflood_boundary_tests/
```

---

# 🎯 USE CASES

```text
🧪 Application Testing
💾 Storage Testing
📁 File Handling Testing
📏 File-Size Boundary Testing
🔐 Hash Verification
💽 Disk Benchmarking
🐍 Python Learning
🐧 Linux Learning
🛡️ Cybersecurity Labs
🔬 Development Testing
```

---

# 🧪 EXAMPLE WORKFLOW

```text
START FILEFLOOD
       │
       ▼
CREATE 10 MB FILE
       │
       ▼
FILE INFORMATION
       │
       ▼
CALCULATE SHA-256
       │
       ▼
PUMP +10 MB
       │
       ▼
VERIFY NEW SIZE
       │
       ▼
CALCULATE HASH AGAIN
       │
       ▼
RUN DISK BENCHMARK
       │
       ▼
DONE
```

---

# 🛣️ ROADMAP

### COMPLETED

```text
[✓] Interactive CLI
[✓] KB / MB / GB support
[✓] New file generation
[✓] Existing file pumping
[✓] Target-size pumping
[✓] Multiple data patterns
[✓] Sparse file support
[✓] File information
[✓] Hashing
[✓] Boundary testing
[✓] Disk benchmarking
[✓] Progress display
[✓] Disk-space checking
[✓] Colored terminal interface
```

### PLANNED

```text
[ ] Configurable chunk size
[ ] Custom output directories
[ ] Multiple-file generation
[ ] Custom repeating patterns
[ ] Read benchmark
[ ] Read / Write comparison
[ ] Benchmark reports
[ ] Exportable results
[ ] Operation history
[ ] Configuration persistence
[ ] Improved terminal animations
[ ] Standalone executable release
```

---

# 🔥 PROJECT PHILOSOPHY

```text
             SIMPLE
                │
                ▼
           INTERACTIVE
                │
                ▼
            AUTOMATED
                │
                ▼
             POWERFUL
                │
                ▼
             TESTABLE
```

FileFlood is designed to make file-generation and file-testing operations easier while keeping the interface beginner-friendly.

---

# ⚠️ DISCLAIMER

FileFlood is intended for:

```text
Educational purposes
Development
Authorized testing
Storage testing
Application testing
Benchmarking
Cybersecurity laboratories
```

Do not use FileFlood to intentionally exhaust storage resources on systems you do not own or have authorization to test.

Large file operations can consume significant disk space.

Always verify:

```text
✓ Target Path
✓ Requested Size
✓ Available Disk Space
✓ Authorization
```

The author is not responsible for data loss, storage exhaustion, service disruption, system damage, or misuse resulting from this software.

Use responsibly.

---

# 🤝 CONTRIBUTING

Contributions are welcome.

You can contribute through:

```text
🐛 Bug Reports
💡 Feature Requests
🔧 Code Improvements
📖 Documentation Improvements
🎨 Interface Improvements
⚡ Performance Improvements
```

For bugs, include:

```text
1. Description
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Python version
6. Linux distribution
```

---

# ⭐ SUPPORT THE PROJECT

```text
⭐ Star the repository
🍴 Fork the project
🐛 Report bugs
💡 Suggest features
📢 Share the project
```

---

<div align="center">

# 🌊 FILEFLOOD

### `GENERATE • PUMP • INSPECT • HASH • TEST • BENCHMARK`

```text
╔══════════════════════════════════════════════════════╗
║                                                      ║
║                    FILEFLOOD                         ║
║                                                      ║
║          GENERATE • PUMP • TEST • BENCHMARK          ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

**🐍 Built with Python**

**🐧 Built for Linux**

**⚡ Built from Scratch**

<br>

<img src="https://img.shields.io/badge/PYTHON-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/LINUX-SUPPORTED-FCC624?style=for-the-badge&logo=linux&logoColor=black">
<img src="https://img.shields.io/badge/CLI-TOOL-00d9ff?style=for-the-badge">
<img src="https://img.shields.io/badge/OPEN%20SOURCE-YES-00ff9d?style=for-the-badge">

</div>
