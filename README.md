# Data Hazard Detection Unit (using Python)

## About
This was a project done for my CSE520 - Computer Architecture II course at ASU.
The objective was to run through a given Assembly code, identify possible data hazards and stall locations and return number of clocks taken by the code to run on a MIPS 5-stage pipeline with minor forwarding

## How to Run
- Open terminal in this folder and run `python CSE520_Project.py`
- The program will ask if you want to enter a custom assembly file. You can provide the path.
  - By default it will run the `test.asm` file present in the same folder.
- The program will display the number of ideal clock cycles in which it can be completed as well as the current delay and cycles caused due to slack.

#### NOTE:

- No other dependencies are required ideally, but in case any are missing, you can install `pipreqs` using `pip install pipreqs` and run the command `pipreqs` in the project folder to generate a `requirements.txt` file. This can be installed using `pip install -r requirements.txt` command.

## Authors
Aravind Hari Nair
Chiang Wang