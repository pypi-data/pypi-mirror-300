import cloudscraper as cc
import httpx as hx
import json as js
import os
import tqdm as td

import constants as cs
import file as fl

cwd = os.getcwd()

def download(link: str, path: str, progress = True, description = None) -> None:
    """Download data from 'link' and store at 'path'."""
    
    if description is not None:
        print(f"Downloading {description}...")
    
    with hx.Client(http2 = True) as client:
        with client.stream("get", link) as response:
            with open(path, "wb") as file:
                total = int(response.headers.get("Content-Length", 0))
                with td.tqdm(total = total, \
                             unit_scale = True, \
                             unit_divisor = 2**10, \
                             unit = "B", \
                             disable = not progress) as progress:
                    num_bytes_downloaded = response.num_bytes_downloaded
                    for chunk in response.iter_bytes():
                        file.write(chunk)
                        progress.update(response.num_bytes_downloaded)
                        num_bytes_downloaded = response.num_bytes_downloaded

def question(string: str) -> bool:
    """Ask the user a Y/N question and return the accompagnied truth value."""
    while True:
        choice = input(f"{string} (Y/N): ").lower()
        
        if choice in cs.answers_true:
            return True
        elif choice in cs.answers_false:
            return False
        else:
            print("This is not an option. Please try again.")

def drive_selection() -> str:
    """Select a drive for a directory."""
    
    # Select drive for Windows only
    if os.name == "nt":
        # Collect available drives
        drives = []
        for letter in [chr(x) for x in range(ord("A"), ord("A") + 26)]:
            if os.path.exists(f"{letter}:"):
                drives.append(letter)
        
        # Print all drives
        for letter in drives:
            print(f"{letter}. Drive {letter}:")
        
        # Select a drive
        while True:
            drive = input("Which drive should be selected? (Enter the corresponding option): ").upper()
            
            if drive in drives:
                return f"{drive}:"
            else:
                print("This is not an option. Please try again.")
    else:
        return os.path.splitdrive(cwd)[0]

def clear_screen() -> None:
    """Clear the screen for Windows and Unix-based systems."""
    
    os.system("cls" if os.name == "nt" else "clear")

def get_translations() -> dict[str, dict]:
    """Collect all translations from the Custom Mario Kart Wiiki."""
    
    scraper = cc.create_scraper(browser = {"custom": "ScraperBot"})
    text = scraper.get("https://wiki.tockdom.com/info-w/translations.json").text
    json = js.loads(text)
    return json["translate"]

def get_prefixes() -> list[str]:
    """Collect all prefixes from Wiimm's CT-Archive."""
    
    file = fl.TXT(os.path.join(os.getcwd(), "prefixes.txt"))
    download("https://ct.wiimm.de/export/prefix", file.path)
    
    info = file.read()
    
    prefixes = set()
    for k in range(len(info)):
        if info[k][0] == "#" or info[k][0] == "@":
            continue
        prefixes.add(info[k][:info[k].find("|")])
    file.delete()
    return prefixes

def rename_riivolution(riivolution: fl.Folder, Wiimm_Intermezzo: fl.File, new_suffix: str) -> tuple[fl.Folder, fl.File]:
    """Rename an Intermezzo build from Wiimm so it has a unique name for Riivolution."""
    
    for file in os.listdir(riivolution.path):
        if file.endswith(".xml"):
            xml = fl.TXT(os.path.join(riivolution.path, file))
            break
    if xml.filename != "Wiimm-Intermezzo.xml":
        current_suffix = xml.filename[len("Wiimm-Intermezzo-"):xml.filename.find(".xml")]
    else:
        current_suffix = ""
    lines = xml.read()
    for x in range(len(lines)):
        lines[x] = lines[x].replace(f"WiimmIntermezzo{current_suffix}", f"WiimmIntermezzo{new_suffix}")
        if current_suffix:
            lines[x] = lines[x].replace(f"Wiimm-Intermezzo-{current_suffix}", f"Wiimm-Intermezzo-{new_suffix}")
        else:
            lines[x] = lines[x].replace("Wiimm-Intermezzo", f"Wiimm-Intermezzo-{new_suffix}")
    xml.write(lines)
    xml.rename(f"Wiimm-Intermezzo-{new_suffix}.xml")
    Wiimm_Intermezzo.rename(f"Wiimm-Intermezzo-{new_suffix}")
    return riivolution, Wiimm_Intermezzo
