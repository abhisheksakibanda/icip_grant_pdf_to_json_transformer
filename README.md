# ICIP Grant PDF to JSON Transformer

A tool to extract data from an ICIP Grant/Contribution Payment Form and convert to a JSON file

## Pre-requisites:
This tool requires you to install the GhostScript package on your system.
You can download it from <a href="https://www.ghostscript.com/download/gsdnld.html" target="_blank" title="GhostScript Download Page">here</a>

Download and install the package based on your system configuration and add the path to the GhostScript executable to your system's PATH environment variable.
(Default Windows Location: `C:\Program Files\gs\gsx.x.x\bin`)

## Installation:
1. Clone the repository
2. Run `pip install -r requirements.txt` to install the required packages
3. Run the `main.py` file to start the application
4. Enter the path to the ICIP Grant PDF file when prompted
5. The program will ask for the location to save the JSON file after processing

## Program Flags:
- `--pdf` / `-p` : Path to the ICIP Grant PDF file
- `--json` / `-j` : Path to save the JSON file after processing


