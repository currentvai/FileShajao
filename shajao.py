import os
import shutil
import sys
import time

# ANSI escape codes for colors
C_CYAN = '\033[1;36m'
C_BLUE = '\033[1;34m'
C_YELLOW = '\033[1;33m'
C_RED = '\033[1;31m'
C_GREEN = '\033[1;32m'
C_RESET = '\033[0m'

def display_banner():
    """Displays the project banner and information."""
    # আপনার দেওয়া নতুন ব্যানার
    banner_art = """
███████ ██ ██      ███████ ███████ ██   ██  █████       ██  █████   ██████  
██      ██ ██      ██      ██      ██   ██ ██   ██      ██ ██   ██ ██    ██ 
█████   ██ ██      █████   ███████ ███████ ███████      ██ ███████ ██    ██ 
██      ██ ██      ██           ██ ██   ██ ██   ██ ██   ██ ██   ██ ██    ██ 
██      ██ ███████ ███████ ███████ ██   ██ ██   ██  █████  ██   ██  ██████  
"""
    current_year = time.strftime("%Y")
    
    print(f"{C_CYAN}{banner_art}{C_RESET}")
    print(f"{C_BLUE}Developed By Current Vai ♚ | FileShajao v1.0{C_RESET}")
    print(f"{C_YELLOW}© Copyright {current_year} — All Rights Reserved.{C_RESET}")
    print(f"{C_RED}\"I am completely destroyed. Error 304 Not Modified.\"{C_RESET}\n")
    print(f"{C_GREEN}GitHub: https://github.com/currentvai{C_RESET}") # আপনার GitHub ইউজারনেম দিন
    print(f"{C_GREEN}Telegram: https://t.me/currentvai{C_RESET}\n") # আপনার Telegram ইউজারনেম দিন

def get_storage_path():
    """Asks user to select storage and returns the path."""
    print(f"{C_YELLOW}[>] Choose a storage option:{C_RESET}")
    print("  [1] Internal Storage (Phone Memory)")
    print("  [2] External Storage (SD Card)")
    
    while True:
        choice = input(f"{C_GREEN}[+] Enter your choice (1/2): {C_RESET}")
        if choice == '1':
            return '/sdcard'
        elif choice == '2':
            storage_path = '/storage'
            try:
                all_storages = os.listdir(storage_path)
                sd_cards = [d for d in all_storages if d != 'emulated' and os.path.isdir(os.path.join(storage_path, d))]
                if not sd_cards:
                    print(f"{C_RED}[!] No external SD Card found! Make sure it is mounted.{C_RESET}")
                    return None
                return os.path.join(storage_path, sd_cards[0])
            except FileNotFoundError:
                print(f"{C_RED}[!] Could not access /storage. Is your SD Card properly inserted?{C_RESET}")
                return None
        else:
            print(f"{C_RED}[!] Invalid choice. Please enter 1 or 2.{C_RESET}")

def select_folder(base_path):
    """Lists folders and lets the user select one."""
    print(f"\n{C_YELLOW}[>] Listing directories in: {base_path}{C_RESET}")
    try:
        directories = sorted([d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))])
        if not directories:
            print(f"{C_RED}[!] No directories found in this location.{C_RESET}")
            return None

        for i, dirname in enumerate(directories):
            print(f"  [{i+1}] {dirname}")
        
        while True:
            try:
                choice = int(input(f"\n{C_GREEN}[+] Select a folder number to rearrange: {C_RESET}"))
                if 1 <= choice <= len(directories):
                    return os.path.join(base_path, directories[choice-1])
                else:
                    print(f"{C_RED}[!] Invalid number. Please try again.{C_RESET}")
            except ValueError:
                print(f"{C_RED}[!] Please enter a valid number.{C_RESET}")
    except FileNotFoundError:
        print(f"{C_RED}[!] Error: The path '{base_path}' does not exist.{C_RESET}")
        return None
    except Exception as e:
        print(f"{C_RED}[!] An error occurred: {e}{C_RESET}")
        return None

def rearrange_files(target_dir):
    """Rearranges files in the target directory based on extension."""
    print(f"\n{C_YELLOW}[*] Starting rearrangement in: {target_dir}{C_RESET}")
    
    try:
        file_count = 0
        for filename in os.listdir(target_dir):
            source_path = os.path.join(target_dir, filename)

            if os.path.isfile(source_path):
                extension = os.path.splitext(filename)[1][1:].lower()
                if not extension:
                    extension = 'Other_Files' # এক্সটেনশন ছাড়া ফাইলের জন্য ফোল্ডার
                
                destination_dir = os.path.join(target_dir, extension)
                
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                    print(f"{C_GREEN}[+] Created directory: {destination_dir}{C_RESET}")
                
                destination_path = os.path.join(destination_dir, filename)
                shutil.move(source_path, destination_path)
                print(f"  -> Moved '{filename}' to '{extension}' folder.")
                file_count += 1
        
        if file_count == 0:
            print(f"\n{C_YELLOW}[i] No files found to rearrange in the selected folder.{C_RESET}")
        else:
            print(f"\n{C_GREEN}[✔] Successfully rearranged {file_count} files!{C_RESET}")

    except Exception as e:
        print(f"{C_RED}[!] An error occurred during rearrangement: {e}{C_RESET}")

def main():
    """Main function to run the script."""
    try:
        os.system('clear')
        display_banner()
        
        base_path = get_storage_path()
        if base_path:
            target_folder = select_folder(base_path)
            if target_folder:
                rearrange_files(target_folder)

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Process interrupted by user. Exiting.{C_RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
