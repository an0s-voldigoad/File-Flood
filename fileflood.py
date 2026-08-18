#!/usr/bin/env python3

import hashlib
import os
import shutil
import sys
import time
from pathlib import Path


# ============================================================
#                         FileFlood
#        Advanced File Size Generation & Testing Utility
# ============================================================


# ============================================================
#                         TERMINAL COLORS
# ============================================================

RESET = "\033[0m"

BLACK = "\033[30m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"

BOLD = "\033[1m"


# ============================================================
#                           BANNER
# ============================================================

BANNER = r"""
 ________  _____  _____     ________   ________  _____       ___      ___   ______
|_   __  ||_   _||_   _|   |_   __  | |_   __  ||_   _|    .'   `.  .'   `.|_   _ `.
  | |_ \_|  | |    | |       | |_ \_|   | |_ \_|  | |     /  .-.  \/  .-.  \ | | `. \
  |  _|     | |    | |   _   |  _| _    |  _|     | |   _ | |   | || |   | | | |  | |
 _| |_     _| |_  _| |__/ | _| |__/ |  _| |_     _| |__/ |\  `-'  /\  `-'  /_| |_.' /
|_____|   |_____||________||________| |_____|   |________| `.___.'  `.___.'|______.'  

              Advanced File Size Generation & Testing Utility
"""


# ============================================================
#                         CONFIGURATION
# ============================================================

DEFAULT_CHUNK_SIZE = 1024 * 1024       # 1 MB
DEFAULT_BENCHMARK_SIZE = 100 * 1024 * 1024


# ============================================================
#                       TERMINAL HELPERS
# ============================================================

def clear_terminal():
    """Clear the terminal screen."""
    os.system("clear")


def show_banner():
    """Display FileFlood banner."""
    print(CYAN + BOLD + BANNER + RESET)


def header(title):
    """Display a section header."""
    print()
    print(MAGENTA + "                    ┌─────────────────────────────────┐")
    print(f"                    │ {title:^31} │")
    print("                    └─────────────────────────────────┘" + RESET)
    print()


def pause():
    """Wait for Enter."""
    input(
        "\n" +
        YELLOW +
        "                    Press ENTER to continue..." +
        RESET
    )


def clear_and_banner():
    """Clear screen and display banner."""
    clear_terminal()
    show_banner()


def success(message):
    """Print success message."""
    print(GREEN + f"\n                    ✓ {message}" + RESET)


def warning(message):
    """Print warning message."""
    print(YELLOW + f"\n                    ! {message}" + RESET)


def error(message):
    """Print error message."""
    print(RED + f"\n                    ✗ {message}" + RESET)


def info(message):
    """Print informational message."""
    print(CYAN + f"\n                    [*] {message}" + RESET)


# ============================================================
#                         SIZE HELPERS
# ============================================================

UNITS = {
    "B": 1,
    "KB": 1024,
    "MB": 1024 ** 2,
    "GB": 1024 ** 3,
}


def format_size(size_bytes):
    """Convert bytes into a human-readable size."""

    if size_bytes < 1024:
        return f"{size_bytes} B"

    if size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.2f} KB"

    if size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.2f} MB"

    return f"{size_bytes / (1024 ** 3):.2f} GB"


def choose_unit():
    """Ask user to select KB, MB or GB."""

    print(CYAN + "                    Select size unit:" + RESET)
    print()
    print("                    [1] KB")
    print("                    [2] MB")
    print("                    [3] GB")
    print()

    choice = input(
        YELLOW + "                    Select: " + RESET
    ).strip()

    units = {
        "1": ("KB", 1024),
        "2": ("MB", 1024 ** 2),
        "3": ("GB", 1024 ** 3),
    }

    return units.get(choice)


def ask_size():
    """Ask for a numerical size and unit."""

    unit = choose_unit()

    if unit is None:
        error("Invalid unit selection.")
        return None

    unit_name, multiplier = unit

    while True:

        value = input(
            YELLOW +
            f"\n                    Enter size in {unit_name}: " +
            RESET
        ).strip()

        try:
            value = float(value)

            if value <= 0:
                raise ValueError

            total_bytes = int(value * multiplier)

            if total_bytes <= 0:
                raise ValueError

            return total_bytes, value, unit_name

        except ValueError:
            error("Please enter a valid positive number.")


def parse_size_string(value):
    """
    Parse strings such as:
        500MB
        1.5GB
        100KB
    """

    value = value.strip().upper().replace(" ", "")

    for unit in ("GB", "MB", "KB", "B"):

        if value.endswith(unit):

            number = value[:-len(unit)]

            try:
                number = float(number)

                if number <= 0:
                    return None

                return int(number * UNITS[unit])

            except ValueError:
                return None

    return None


# ============================================================
#                       DISK INFORMATION
# ============================================================

def get_disk_space(path="."):
    """Return total, used and free disk space."""

    usage = shutil.disk_usage(path)

    return usage.total, usage.used, usage.free


def show_disk_space(path="."):
    """Display disk space information."""

    total, used, free = get_disk_space(path)

    print(WHITE + f"                    Total : {format_size(total)}")
    print(WHITE + f"                    Used  : {format_size(used)}")
    print(WHITE + f"                    Free  : {format_size(free)}" + RESET)


def enough_disk_space(required_bytes, path="."):
    """Check whether enough disk space is available."""

    _, _, free = get_disk_space(path)

    return free >= required_bytes


# ============================================================
#                     PROGRESS DISPLAY
# ============================================================

def progress_bar(current, total, start_time, width=45):
    """Display progress bar, speed and ETA."""

    if total <= 0:
        percent = 100
    else:
        percent = min(current / total, 1.0) * 100

    filled = int(width * percent / 100)

    bar = "█" * filled + "░" * (width - filled)

    elapsed = max(time.time() - start_time, 0.0001)

    speed = current / elapsed

    if speed > 0:
        remaining = max(total - current, 0) / speed
    else:
        remaining = 0

    speed_text = format_size(int(speed)) + "/s"

    print(
        f"\r                    "
        f"[{bar}] "
        f"{percent:6.2f}% "
        f"{speed_text:>12} "
        f"ETA {remaining:6.1f}s",
        end="",
        flush=True
    )


# ============================================================
#                     DATA PATTERN ENGINE
# ============================================================

def generate_chunk(pattern, size):
    """Generate a chunk of data."""

    if pattern == "zero":
        return b"\x00" * size

    if pattern == "random":
        return os.urandom(size)

    if pattern == "repeat":
        data = b"FILEFLOOD"
        repeats = (size // len(data)) + 1
        return (data * repeats)[:size]

    return b"\x00" * size


def choose_pattern():
    """Choose file data pattern."""

    print(CYAN + "                    Select data pattern:" + RESET)
    print()
    print("                    [1] Zero")
    print("                    [2] Random")
    print("                    [3] Repeating FileFlood pattern")
    print()

    choice = input(
        YELLOW + "                    Select: " + RESET
    ).strip()

    patterns = {
        "1": "zero",
        "2": "random",
        "3": "repeat",
    }

    return patterns.get(choice)


# ============================================================
#                       FILE WRITER
# ============================================================

def write_file(path, total_bytes, pattern="zero"):
    """Write actual data to a file with progress."""

    written = 0
    start_time = time.time()

    try:

        with open(path, "wb") as file:

            while written < total_bytes:

                remaining = total_bytes - written

                chunk_size = min(DEFAULT_CHUNK_SIZE, remaining)

                data = generate_chunk(pattern, chunk_size)

                file.write(data)

                written += chunk_size

                progress_bar(
                    written,
                    total_bytes,
                    start_time
                )

        print()

        elapsed = max(time.time() - start_time, 0.0001)

        speed = written / elapsed

        print(
            WHITE +
            f"\n                    Written : {format_size(written)}"
        )

        print(
            WHITE +
            f"                    Time    : {elapsed:.2f} seconds"
        )

        print(
            WHITE +
            f"                    Speed   : {format_size(int(speed))}/s" +
            RESET
        )

        return True

    except OSError as exc:

        print()

        error(f"Write operation failed: {exc}")

        return False


# ============================================================
#                    SPARSE FILE CREATION
# ============================================================

def create_sparse_file(path, total_bytes):
    """Create a sparse file."""

    try:

        with open(path, "wb") as file:
            file.seek(total_bytes - 1)
            file.write(b"\x00")

        return True

    except OSError as exc:

        error(f"Sparse file creation failed: {exc}")

        return False


# ============================================================
#                    CREATE NEW FILE
# ============================================================

def create_file():
    """Interactive new-file creation."""

    clear_and_banner()

    header("CREATE NEW FILE")

    filename = input(
        YELLOW +
        "                    Enter filename/path: " +
        RESET
    ).strip()

    if not filename:

        error("Filename cannot be empty.")

        pause()

        return

    path = Path(filename).expanduser()

    if path.exists():

        error("File already exists.")

        print()

        overwrite = input(
            YELLOW +
            "                    Overwrite it? [y/N]: " +
            RESET
        ).strip().lower()

        if overwrite not in ("y", "yes"):

            warning("Operation cancelled.")

            pause()

            return

    size_result = ask_size()

    if size_result is None:
        pause()
        return

    total_bytes, value, unit = size_result

    print()

    pattern = choose_pattern()

    if pattern is None:

        error("Invalid pattern selection.")

        pause()

        return

    print()

    print(CYAN + "                    Creation mode:" + RESET)
    print()
    print("                    [1] Normal file")
    print("                    [2] Sparse file")
    print()

    mode = input(
        YELLOW +
        "                    Select: " +
        RESET
    ).strip()

    if mode not in ("1", "2"):

        error("Invalid creation mode.")

        pause()

        return

    print()

    print(MAGENTA + "                    ┌─────────────────────────────────┐")
    print("                    │           FILE SUMMARY            │")
    print("                    └─────────────────────────────────┘" + RESET)

    print()

    print(WHITE + f"                    File    : {path}")
    print(WHITE + f"                    Size    : {value:g} {unit}")
    print(WHITE + f"                    Bytes   : {total_bytes:,}")
    print(WHITE + f"                    Pattern : {pattern}")
    print(
        WHITE +
        f"                    Mode    : "
        f"{'Normal' if mode == '1' else 'Sparse'}"
    )

    print()

    if mode == "1":

        if not enough_disk_space(total_bytes, path.parent or "."):

            error("Insufficient disk space.")

            show_disk_space(path.parent or ".")

            pause()

            return

    else:

        warning(
            "Sparse files consume little physical space initially, "
            "but applications will see the requested logical size."
        )

    print()

    confirmation = input(
        YELLOW +
        "                    Continue? [Y/n]: " +
        RESET
    ).strip().lower()

    if confirmation not in ("", "y", "yes"):

        warning("Operation cancelled.")

        pause()

        return

    clear_and_banner()

    header("CREATING FILE")

    print(
        WHITE +
        f"                    File    : {path}"
    )

    print(
        WHITE +
        f"                    Size    : {format_size(total_bytes)}"
    )

    print()

    if mode == "2":

        if create_sparse_file(path, total_bytes):

            success("Sparse file created successfully.")

    else:

        if write_file(path, total_bytes, pattern):

            success("File created successfully.")

    if path.exists():

        print(
            WHITE +
            f"                    Final size: "
            f"{format_size(path.stat().st_size)}" +
            RESET
        )

    pause()


# ============================================================
#                       PUMP EXISTING FILE
# ============================================================

def pump_file():
    """Pump an existing file."""

    clear_and_banner()

    header("PUMP EXISTING FILE")

    filename = input(
        YELLOW +
        "                    Enter file path: " +
        RESET
    ).strip()

    path = Path(filename).expanduser()

    if not path.is_file():

        error("File does not exist.")

        pause()

        return

    current_size = path.stat().st_size

    print(
        WHITE +
        f"\n                    Current size: "
        f"{format_size(current_size)}" +
        RESET
    )

    print()

    print(CYAN + "                    Pump mode:" + RESET)
    print()
    print("                    [1] Add size")
    print("                    [2] Set target size")
    print()

    mode = input(
        YELLOW +
        "                    Select: " +
        RESET
    ).strip()

    if mode not in ("1", "2"):

        error("Invalid selection.")

        pause()

        return

    size_result = ask_size()

    if size_result is None:

        pause()

        return

    amount, value, unit = size_result

    if mode == "1":

        bytes_to_add = amount

        final_size = current_size + bytes_to_add

    else:

        target_size = amount

        if target_size <= current_size:

            error(
                "Target size must be larger than the current file size."
            )

            pause()

            return

        bytes_to_add = target_size - current_size

        final_size = target_size

    print()

    pattern = choose_pattern()

    if pattern is None:

        error("Invalid pattern selection.")

        pause()

        return

    print()

    print(MAGENTA + "                    ┌─────────────────────────────────┐")
    print("                    │            PUMP SUMMARY            │")
    print("                    └─────────────────────────────────┘" + RESET)

    print()

    print(WHITE + f"                    File     : {path}")
    print(WHITE + f"                    Current  : {format_size(current_size)}")
    print(WHITE + f"                    Adding   : {format_size(bytes_to_add)}")
    print(WHITE + f"                    Final    : {format_size(final_size)}")
    print(WHITE + f"                    Pattern  : {pattern}" + RESET)

    print()

    if not enough_disk_space(bytes_to_add, path.parent or "."):

        error("Insufficient disk space.")

        show_disk_space(path.parent or ".")

        pause()

        return

    confirmation = input(
        YELLOW +
        "\n                    Continue? [Y/n]: " +
        RESET
    ).strip().lower()

    if confirmation not in ("", "y", "yes"):

        warning("Operation cancelled.")

        pause()

        return

    clear_and_banner()

    header("PUMPING FILE")

    print(
        WHITE +
        f"                    File    : {path}"
    )

    print(
        WHITE +
        f"                    Current : {format_size(current_size)}"
    )

    print(
        WHITE +
        f"                    Adding  : {format_size(bytes_to_add)}"
    )

    print(
        WHITE +
        f"                    Target  : {format_size(final_size)}" +
        RESET
    )

    print()

    start_time = time.time()

    try:

        with open(path, "ab") as file:

            written = 0

            while written < bytes_to_add:

                remaining = bytes_to_add - written

                chunk_size = min(
                    DEFAULT_CHUNK_SIZE,
                    remaining
                )

                data = generate_chunk(
                    pattern,
                    chunk_size
                )

                file.write(data)

                written += chunk_size

                progress_bar(
                    written,
                    bytes_to_add,
                    start_time
                )

        print()

        elapsed = max(time.time() - start_time, 0.0001)

        speed = bytes_to_add / elapsed

        print(
            WHITE +
            f"\n                    Added   : "
            f"{format_size(bytes_to_add)}"
        )

        print(
            WHITE +
            f"                    Speed   : "
            f"{format_size(int(speed))}/s"
        )

        print(
            WHITE +
            f"                    Final   : "
            f"{format_size(path.stat().st_size)}" +
            RESET
        )

        success("File pumped successfully.")

    except OSError as exc:

        print()

        error(f"Pump operation failed: {exc}")

    pause()


# ============================================================
#                     FILE INFORMATION
# ============================================================

def file_information():
    """Display information about a file."""

    clear_and_banner()

    header("FILE INFORMATION")

    filename = input(
        YELLOW +
        "                    Enter file path: " +
        RESET
    ).strip()

    path = Path(filename).expanduser()

    if not path.exists():

        error("File does not exist.")

        pause()

        return

    try:

        stat = path.stat()

        print(MAGENTA + "                    ┌─────────────────────────────────┐")
        print("                    │             INFORMATION            │")
        print("                    └─────────────────────────────────┘" + RESET)

        print()

        print(WHITE + f"                    Name       : {path.name}")
        print(WHITE + f"                    Location   : {path.resolve()}")
        print(WHITE + f"                    Size       : {format_size(stat.st_size)}")
        print(WHITE + f"                    Bytes      : {stat.st_size:,}")
        print(WHITE + f"                    Permissions: {oct(stat.st_mode)[-3:]}")
        print(
            WHITE +
            f"                    Modified   : "
            f"{time.ctime(stat.st_mtime)}"
        )

        if path.is_file():

            print(WHITE + "                    Type       : Regular file")

        elif path.is_dir():

            print(WHITE + "                    Type       : Directory")

        else:

            print(WHITE + "                    Type       : Other")

        print(RESET)

    except OSError as exc:

        error(f"Unable to read file information: {exc}")

    pause()


# ============================================================
#                         HASH ENGINE
# ============================================================

def calculate_hash(path, algorithm):
    """Calculate a file hash."""

    hasher = hashlib.new(algorithm)

    try:

        with open(path, "rb") as file:

            while True:

                chunk = file.read(DEFAULT_CHUNK_SIZE)

                if not chunk:
                    break

                hasher.update(chunk)

        return hasher.hexdigest()

    except OSError:

        return None


def hash_file():
    """Calculate file hashes."""

    clear_and_banner()

    header("HASH / INTEGRITY")

    filename = input(
        YELLOW +
        "                    Enter file path: " +
        RESET
    ).strip()

    path = Path(filename).expanduser()

    if not path.is_file():

        error("File does not exist.")

        pause()

        return

    algorithms = [
        "md5",
        "sha1",
        "sha256",
        "sha512",
    ]

    print()

    for algorithm in algorithms:

        info(f"Calculating {algorithm.upper()}...")

        digest = calculate_hash(
            path,
            algorithm
        )

        if digest:

            print(
                WHITE +
                f"\n                    "
                f"{algorithm.upper():<7}: {digest}" +
                RESET
            )

        else:

            error(
                f"Unable to calculate {algorithm.upper()}."
            )

    pause()


# ============================================================
#                     BOUNDARY TESTING
# ============================================================

def boundary_testing():
    """Generate files around a selected size boundary."""

    clear_and_banner()

    header("BOUNDARY TESTING")

    print(
        WHITE +
        "                    Example:"
    )

    print(
        GRAY +
        "                    Enter 100MB to generate:"
    )

    print(
        GRAY +
        "                    99MB, 99.5MB, 100MB, 100.5MB, 101MB" +
        RESET
    )

    print()

    raw = input(
        YELLOW +
        "                    Base size: " +
        RESET
    ).strip()

    base = parse_size_string(raw)

    if base is None:

        error(
            "Invalid size. Example: 100MB"
        )

        pause()

        return

    variations = [
        int(base * 0.99),
        int(base * 0.995),
        base,
        int(base * 1.005),
        int(base * 1.01),
    ]

    print()

    print(CYAN + "                    Generated boundary sizes:" + RESET)

    for index, size in enumerate(variations, 1):

        print(
            WHITE +
            f"                    [{index}] "
            f"{format_size(size)}"
        )

    print()

    create = input(
        YELLOW +
        "                    Create these files? [y/N]: " +
        RESET
    ).strip().lower()

    if create not in ("y", "yes"):

        warning("Operation cancelled.")

        pause()

        return

    output_dir = Path("fileflood_boundary_tests")

    try:

        output_dir.mkdir(
            exist_ok=True
        )

        for index, size in enumerate(variations, 1):

            filename = (
                output_dir /
                f"boundary_{index}_{format_size(size).replace(' ', '')}.bin"
            )

            print(
                CYAN +
                f"\n                    Creating {filename}" +
                RESET
            )

            if not enough_disk_space(
                size,
                output_dir
            ):

                error("Insufficient disk space.")

                break

            write_file(
                filename,
                size,
                "zero"
            )

        success(
            f"Boundary files created in {output_dir}"
        )

    except OSError as exc:

        error(f"Boundary test failed: {exc}")

    pause()


# ============================================================
#                      DISK BENCHMARK
# ============================================================

def disk_benchmark():
    """Perform a simple sequential write benchmark."""

    clear_and_banner()

    header("DISK BENCHMARK")

    print(
        WHITE +
        "                    Benchmark size:" +
        RESET
    )

    size_result = ask_size()

    if size_result is None:

        pause()

        return

    total_bytes, value, unit = size_result

    benchmark_file = Path(
        ".fileflood_benchmark.tmp"
    )

    print()

    print(
        WHITE +
        f"                    Test size: "
        f"{value:g} {unit}" +
        RESET
    )

    if not enough_disk_space(
        total_bytes,
        "."
    ):

        error("Not enough disk space for benchmark.")

        pause()

        return

    confirmation = input(
        YELLOW +
        "\n                    Start benchmark? [Y/n]: " +
        RESET
    ).strip().lower()

    if confirmation not in ("", "y", "yes"):

        warning("Benchmark cancelled.")

        pause()

        return

    clear_and_banner()

    header("DISK BENCHMARK")

    print()

    start = time.time()

    success_write = write_file(
        benchmark_file,
        total_bytes,
        "zero"
    )

    elapsed = max(
        time.time() - start,
        0.0001
    )

    if success_write:

        write_speed = total_bytes / elapsed

        print()

        print(
            GREEN +
            f"                    Write speed: "
            f"{format_size(int(write_speed))}/s" +
            RESET
        )

    try:

        benchmark_file.unlink()

    except OSError:
        pass

    pause()


# ============================================================
#                          SETTINGS
# ============================================================

def settings():
    """Display FileFlood settings."""

    clear_and_banner()

    header("SETTINGS")

    print(
        WHITE +
        f"                    Chunk size: "
        f"{format_size(DEFAULT_CHUNK_SIZE)}"
    )

    print(
        WHITE +
        "                    Color mode: Enabled"
    )

    print(
        WHITE +
        "                    Interface : Interactive"
    )

    print(
        WHITE +
        "                    Version   : 1.0.0" +
        RESET
    )

    print()

    print(
        GRAY +
        "                    Settings customization will be "
        "expanded in a future version." +
        RESET
    )

    pause()


# ============================================================
#                           ABOUT
# ============================================================

def about():
    """Display FileFlood information."""

    clear_and_banner()

    header("ABOUT FILEFLOOD")

    print(
        WHITE +
        "                    FileFlood"
    )

    print(
        WHITE +
        "                    Version  : 1.0.0"
    )

    print(
        WHITE +
        "                    Platform : Linux / Kali Linux"
    )

    print(
        WHITE +
        "                    Language : Python 3"
    )

    print()

    print(
        CYAN +
        "                    Generate. Pump. Test." +
        RESET
    )

    print()

    print(
        GRAY +
        "                    FileFlood is a local file-generation"
    )

    print(
        GRAY +
        "                    and storage-testing utility." +
        RESET
    )

    pause()


# ============================================================
#                        MAIN MENU
# ============================================================

def show_menu():
    """Display main menu."""

    print(
        MAGENTA +
        "                    ┌─────────────────────────────┐"
    )

    print(
        "                    │        FILEFLOOD MENU       │"
    )

    print(
        "                    └─────────────────────────────┘" +
        RESET
    )

    print()

    options = [
        ("1", "Create New File", CYAN),
        ("2", "Pump Existing File", CYAN),
        ("3", "File Information", CYAN),
        ("4", "Hash / Integrity", CYAN),
        ("5", "Boundary Testing", CYAN),
        ("6", "Disk Benchmark", CYAN),
        ("7", "Settings", CYAN),
        ("8", "About", CYAN),
        ("9", "Exit", RED),
    ]

    for number, text, color in options:

        print(
            WHITE +
            f"                    [{number}] " +
            color +
            text +
            RESET
        )

    print()


# ============================================================
#                        MAIN APPLICATION
# ============================================================

def main():
    """Main FileFlood application loop."""

    while True:

        clear_and_banner()

        show_menu()

        choice = input(
            YELLOW +
            "                    Select an option: " +
            RESET
        ).strip()

        if choice == "1":

            create_file()

        elif choice == "2":

            pump_file()

        elif choice == "3":

            file_information()

        elif choice == "4":

            hash_file()

        elif choice == "5":

            boundary_testing()

        elif choice == "6":

            disk_benchmark()

        elif choice == "7":

            settings()

        elif choice == "8":

            about()

        elif choice == "9":

            clear_terminal()

            print()
            print(
                GREEN +
                "                    FileFlood closed." +
                RESET
            )

            print()

            break

        else:

            error("Invalid menu option.")

            pause()


# ============================================================
#                      PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        clear_terminal()

        print()

        print(
            YELLOW +
            "                    FileFlood interrupted." +
            RESET
        )

        print()

        sys.exit(0)

    except Exception as exc:

        clear_terminal()

        print()

        print(
            RED +
            f"                    Unexpected error: {exc}" +
            RESET
        )

        print()

        sys.exit(1)
