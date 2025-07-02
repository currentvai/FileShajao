import os
import shutil
import sys
import time
import hashlib
import logging
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# --- কালার কোড এবং অন্যান্য ধ্রুবক ---
C_CYAN, C_BLUE, C_YELLOW, C_RED, C_GREEN, C_PURPLE, C_RESET = '\033[1;36m', '\033[1;34m', '\033[1;33m', '\033[1;31m', '\033[1;32m', '\033[1;35m', '\033[0m'
FOLDER_COLORS = ['\033[38;5;208m', '\033[38;5;220m', '\033[38;5;154m', '\033[38;5;87m', '\033[38;5;45m', '\033[38;5;123m']

# নতুন ধ্রুবক: লগ এবং রিসাইকেল বিনের জন্য
LOG_FILE = 'fileshajao.log'
REARRANGE_LOG_FILE = '.rearrange_log.json'
RECYCLE_BIN_NAME = '.FileShajaoTrash'

# --- লগিং সেটআপ ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def display_banner():
    banner_art = """
███████ ██ ██      ███████ ███████ ██   ██  █████       ██  █████   ██████  
██      ██ ██      ██      ██      ██   ██ ██   ██      ██ ██   ██ ██    ██ 
█████   ██ ██      █████   ███████ ███████ ███████      ██ ███████ ██    ██ 
██      ██ ██      ██           ██ ██   ██ ██   ██ ██   ██ ██   ██ ██    ██ 
██      ██ ███████ ███████ ███████ ██   ██ ██   ██  █████  ██   ██  ██████  
"""
    print(f"{C_CYAN}{banner_art}{C_RESET}")
    print(f"{C_BLUE}Developed By Current Vai ♚ | FileShajao v2.0 (Undo & Recycle Bin Edition){C_RESET}")
    print(f"{C_GREEN}GitHub: https://github.com/currentvai{C_RESET}")
    print(f"{C_GREEN}Telegram: https://t.me/currentvai{C_RESET}\n")

def get_available_storages():
    storages = []
    internal_storage = '/sdcard'
    if os.path.exists(internal_storage):
        storages.append({'name': 'Internal Storage', 'path': internal_storage})
    base_storage_path = '/storage'
    if os.path.exists(base_storage_path):
        all_dirs = os.listdir(base_storage_path)
        sd_cards = [d for d in all_dirs if d != 'emulated' and os.path.isdir(os.path.join(base_storage_path, d))]
        if sd_cards:
            storages.append({'name': 'External SD Card', 'path': os.path.join(base_storage_path, sd_cards[0])})
    return storages

def select_storage(storages):
    if not storages:
        print(f"{C_RED}[!] No storage found! Please grant storage permission.{C_RESET}")
        return None
    print(f"{C_YELLOW}[>] Select a storage to scan:{C_RESET}")
    for i, storage in enumerate(storages):
        print(f"  [{i+1}] {storage['name']} ({storage['path']})")
    while True:
        try:
            choice = int(input(f"{C_GREEN}[+] Enter your choice: {C_RESET}"))
            if 1 <= choice <= len(storages): return storages[choice-1]['path']
            else: print(f"{C_RED}[!] Invalid choice.{C_RESET}")
        except ValueError: print(f"{C_RED}[!] Please enter a number.{C_RESET}")

def select_folder_interactive(base_path):
    current_path = base_path
    while True:
        os.system('clear'); display_banner()
        print(f"{C_YELLOW}[i] Current Directory: {C_GREEN}{current_path}{C_RESET}")
        print(f"{C_PURPLE}{'-'*60}{C_RESET}")
        try:
            items = sorted(os.listdir(current_path))
            directories = [d for d in items if os.path.isdir(os.path.join(current_path, d)) and d != RECYCLE_BIN_NAME]
            print(f"  [{C_GREEN}0{C_RESET}] Select THIS folder for actions ('{os.path.basename(current_path)}')")
            print(f"  [{C_YELLOW}..{C_RESET}] Go to Parent Directory")
            for i, dirname in enumerate(directories):
                color = FOLDER_COLORS[i % len(FOLDER_COLORS)]; print(f"  [{color}{i+1}{C_RESET}] {dirname}")
            choice = input(f"\n{C_GREEN}[+] Select a folder or option: {C_RESET}")
            if choice == '0': return current_path
            elif choice == '..':
                parent_path = os.path.dirname(current_path)
                if current_path != base_path: current_path = parent_path
                else: print(f"{C_RED}[!] Cannot go above the selected storage root.{C_RESET}"); time.sleep(1)
            else:
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(directories): current_path = os.path.join(current_path, directories[choice_num-1])
                    else: print(f"{C_RED}[!] Invalid number.{C_RESET}"); time.sleep(1)
                except ValueError: print(f"{C_RED}[!] Invalid input.{C_RESET}"); time.sleep(1)
        except Exception as e: print(f"{C_RED}[!] Error: {e}{C_RESET}"); return None

def setup_recycle_bin(target_dir):
    recycle_path = os.path.join(target_dir, RECYCLE_BIN_NAME)
    if not os.path.exists(recycle_path): os.makedirs(recycle_path)
    return recycle_path

def move_to_recycle_bin(filepath, recycle_bin_dir):
    if not os.path.exists(filepath): return False
    try:
        filename = os.path.basename(filepath)
        destination = os.path.join(recycle_bin_dir, filename)
        if os.path.exists(destination):
            name, ext = os.path.splitext(filename)
            timestamp = int(time.time())
            destination = os.path.join(recycle_bin_dir, f"{name}_{timestamp}{ext}")
        shutil.move(filepath, destination)
        logging.info(f"Moved to recycle bin: {filepath} -> {destination}")
        return True
    except Exception as e:
        logging.error(f"Failed to move {filepath} to recycle bin: {e}")
        return False

def manage_recycle_bin(recycle_bin_dir):
    while True:
        os.system('clear'); display_banner()
        print(f"{C_YELLOW}--- Recycle Bin Management ---{C_RESET}\nLocation: {recycle_bin_dir}")
        files_in_bin = sorted(os.listdir(recycle_bin_dir))
        if not files_in_bin:
            print(f"\n{C_GREEN}[i] Recycle bin is empty.{C_RESET}"); input("\nPress Enter to return..."); return
        print("\nFiles in Recycle Bin:")
        for i, filename in enumerate(files_in_bin): print(f"  [{i+1}] {filename}")
        print("\nOptions:\n  [e] Empty recycle bin (Permanent Delete!)\n  [b] Back to main menu")
        choice = input(f"\n{C_GREEN}[+] Enter your choice: {C_RESET}").lower()
        if choice == 'b': break
        elif choice == 'e':
            confirm = input(f"{C_RED}[!] Are you sure you want to permanently delete ALL files? (yes/no): {C_RESET}").lower()
            if confirm == 'yes':
                for filename in tqdm(files_in_bin, desc="Emptying Bin"):
                    try: os.remove(os.path.join(recycle_bin_dir, filename))
                    except Exception as e: logging.error(f"Failed to delete from bin: {filename}, {e}")
                print(f"{C_GREEN}[✔] Recycle bin emptied.{C_RESET}"); logging.warning("Recycle bin emptied."); time.sleep(2)
        else: print(f"{C_RED}[!] Invalid option.{C_RESET}"); time.sleep(1)

def calculate_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(65536), b''): sha256.update(block)
        return filepath, sha256.hexdigest()
    except (IOError, OSError): return filepath, None

def find_duplicate_files(target_dir, recycle_bin_dir):
    print(f"\n{C_YELLOW}[*] Collecting files to scan...{C_RESET}")
    filepaths = [os.path.join(p, f) for p, _, fs in os.walk(target_dir) for f in fs if RECYCLE_BIN_NAME not in p]
    if not filepaths: print(f"{C_GREEN}[✔] No files to scan.{C_RESET}"); return
    print(f"{C_GREEN}[i] Found {len(filepaths)} files. Calculating hashes...{C_RESET}")
    hashes, duplicates = {}, []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(calculate_hash, path) for path in filepaths}
        with tqdm(total=len(futures), desc="Hashing Files", unit="file") as pbar:
            for future in as_completed(futures):
                try:
                    path, file_hash = future.result()
                    if file_hash:
                        if file_hash in hashes: duplicates.append({'original': hashes[file_hash], 'duplicate': path})
                        else: hashes[file_hash] = path
                except Exception: pass
                pbar.update(1)
    if not duplicates: print(f"\n{C_GREEN}[✔] No duplicate files found!{C_RESET}"); return
    print(f"\n{C_RED}[!] Found {len(duplicates)} duplicate files.{C_RESET}")
    if input(f"{C_YELLOW}[?] Review and move them to recycle bin? (y/n): {C_RESET}").lower() == 'y':
        for item in duplicates:
            print(f"\n  - Original:  {item['original']}\n  - Duplicate: {C_RED}{item['duplicate']}{C_RESET}")
            choice = input("    Move duplicate to recycle bin? (y/n/skip all): ").lower()
            if choice == 'y':
                if move_to_recycle_bin(item['duplicate'], recycle_bin_dir): print(f"    {C_GREEN}Moved to recycle bin!{C_RESET}")
                else: print(f"    {C_RED}Failed to move.{C_RESET}")
            elif choice == 'skip all': break
    print(f"\n{C_GREEN}[✔] Duplicate scan complete.{C_RESET}")

def rearrange_files(target_dir):
    log_path = os.path.join(target_dir, REARRANGE_LOG_FILE)
    if os.path.exists(log_path):
        if input(f"{C_YELLOW}[?] An existing undo log found. Overwrite it? (y/n): {C_RESET}").lower() != 'y': return
    print(f"\n{C_YELLOW}[*] Rearranging files...{C_RESET}")
    rearrange_log = {"operations": []}
    files_to_move = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f)) and f not in [os.path.basename(__file__), LOG_FILE, REARRANGE_LOG_FILE]]
    with tqdm(total=len(files_to_move), desc="Rearranging", unit="file") as pbar:
        for filename in files_to_move:
            source_path = os.path.join(target_dir, filename)
            extension = os.path.splitext(filename)[1][1:].lower() or 'Other_Files'
            destination_dir = os.path.join(target_dir, extension)
            log_entry = {"source": source_path, "destination": os.path.join(destination_dir, filename)}
            rearrange_log["operations"].append(log_entry)
            try:
                if not os.path.exists(destination_dir): os.makedirs(destination_dir)
                shutil.move(source_path, os.path.join(destination_dir, filename))
            except Exception as e: logging.error(f"Failed to move {source_path}: {e}")
            pbar.update(1)
    with open(log_path, 'w') as f: json.dump(rearrange_log, f, indent=4)
    print(f"\n{C_GREEN}[✔] Rearrangement complete. An undo log has been created.{C_RESET}")

def undo_last_rearrange(target_dir):
    log_path = os.path.join(target_dir, REARRANGE_LOG_FILE)
    if not os.path.exists(log_path): print(f"{C_RED}[!] No rearrange log found to undo.{C_RESET}"); return
    print(f"{C_YELLOW}[*] Undoing the last rearrangement...{C_RESET}")
    with open(log_path, 'r') as f: log_data = json.load(f)
    operations = log_data.get("operations", [])
    if not operations: print(f"{C_RED}[!] Log file is empty.{C_RESET}"); return
    with tqdm(total=len(operations), desc="Undoing", unit="file") as pbar:
        for op in reversed(operations):
            try:
                source_dir = os.path.dirname(op['source'])
                if not os.path.exists(source_dir): os.makedirs(source_dir)
                shutil.move(op['destination'], op['source'])
            except Exception as e: logging.error(f"Failed to undo move: {op['destination']} -> {op['source']}. Error: {e}")
            pbar.update(1)
    os.remove(log_path)
    print(f"\n{C_GREEN}[✔] Undo complete! Files restored.{C_RESET}")

def main_menu(target_dir):
    recycle_bin_dir = setup_recycle_bin(target_dir)
    while True:
        os.system('clear'); display_banner()
        print(f"{C_YELLOW}Selected Folder: {C_GREEN}{target_dir}{C_RESET}\n")
        print(f"{C_PURPLE}--- Choose an action ---{C_RESET}")
        print("  [1] Rearrange Files (by extension)"); print("  [2] Find & Delete Duplicate Files")
        print(f"  [3] {C_YELLOW}Undo Last Rearrange{C_RESET}"); print(f"  [4] {C_CYAN}Manage Recycle Bin{C_RESET}")
        print("  [5] Choose another folder"); print("  [6] Exit")
        choice = input(f"\n{C_GREEN}[+] Enter your choice: {C_RESET}")
        if choice == '1': rearrange_files(target_dir)
        elif choice == '2': find_duplicate_files(target_dir, recycle_bin_dir)
        elif choice == '3': undo_last_rearrange(target_dir)
        elif choice == '4': manage_recycle_bin(recycle_bin_dir)
        elif choice == '5': return 'reselect'
        elif choice == '6': logging.info("User exited."); sys.exit(0)
        else: print(f"{C_RED}[!] Invalid choice.{C_RESET}")
        if choice in ['1', '2', '3']: input("\nPress Enter to return to menu...")

def main():
    try:
        logging.info("FileShajao v4.0 started.")
        while True:
            os.system('clear'); display_banner()
            storages = get_available_storages()
            base_path = select_storage(storages)
            if base_path:
                target_folder = select_folder_interactive(base_path)
                if target_folder:
                    logging.info(f"User selected folder: {target_folder}")
                    if main_menu(target_folder) == 'reselect': continue
            break
    except KeyboardInterrupt:
        logging.info("Program interrupted by user (Ctrl+C).")
        print(f"\n{C_RED}[!] Process interrupted. Exiting.{C_RESET}")
    except Exception as e:
        logging.critical(f"An unhandled exception occurred: {e}", exc_info=True)
        print(f"{C_RED}[!!!] A critical error occurred. Check '{LOG_FILE}' for details.{C_RESET}")

if __name__ == "__main__":
    main()
