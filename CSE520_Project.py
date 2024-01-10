############################################# Data Hazard Analyzer #############################################
#
# Objective : To run through a given ASM code, identify possible data hazards and stall locations and return
#             number of clocks taken by the code to run on a MIPS 5-stage pipeline with minor forwarding.
# Authors   : Aravind Hari Nair
#             Chiang Wang
# Due Date  : 19 April, 2022
# Course    : CSE520 - Computer Architecture II
#
################################################################################################################

# Import statements
import os
import logging
logging.basicConfig(filename='std.log', filemode='w', level=logging.WARNING) # Replace level with logging.INFO for all information

# Creating a class to hold register properties
class Register:
  def __init__(self, stage, name, write=False):
    self.stage = stage # if 0 - not-in-use/free  | 1-5: indicates stage
    self.name = name
    self.write = write

# Loading the data into separate arrays for easier processing
def data_load(filepath):
  asm_file = open(filepath, 'r')
  lines = asm_file.readlines()
  logging.info('Reading assembly code line-by-line')
  lines[:] = [x for x in lines if not x.startswith('#')] # Clearing out comments

  instr, reg, instr_reg = [], [], []
  for i in range(len(lines)):
    lines[i] = (((lines[i].strip()).split('   ', 1))[0]).strip()
    logging.info(f'  {i}-> {lines[i]} ')

  for i in range(len(lines)):
    instr.append((lines[i].split(' ', 1))[0])
    reg_current_instr = (lines[i].split(' ', 1))[1].split('$')
    for j in range(len(reg_current_instr)):
      reg_current_instr[j] = reg_current_instr[j].split(',')[0].strip()
      if reg_current_instr[j] not in reg:
        reg.append(reg_current_instr[j])
    reg_current_instr = list(filter(None, reg_current_instr))
    instr_reg.append(reg_current_instr)
    
  reg = list(filter(None, reg)) # Removing empty elements
  reg_copy = reg.copy() # Creating copy for indexing purposes
  for i in range(len(reg)):
    reg[i] = Register(stage=0, name=reg[i]) # Creating register objects
  return instr, reg, reg_copy, instr_reg

# Function to detect if all operations are done and registers are clear
def end_reg(register):
  end = True
  for x in register:
    if x.stage:
      end = False
  return end

# Function to update register object values
def update_reg(register):
  for x in register:
    if x.stage:
      if x.stage == 5:
        x.stage = 0
      else:
        x.stage = x.stage+1
        if x.stage > 3:
          x.write = False   


# MAIN FUNCTION
if __name__ == '__main__':
  file = input("Enter file (default: test.asm): ") or 'test.asm'
  instr, reg, reg_copy, instr_reg = data_load(file)

  # Initializing
  clk, ins, stall_cntr = 0, -1, 0
  run_complete = False
  stall = False
  stall_reg = ''

  while not run_complete:
    clk = clk + 1
    update_reg(reg)
    for x in range(len(reg_copy)):
      logging.info(f'Status of {reg[x].name} stage= {reg[x].stage} | write= {reg[x].write}')

    if stall:
      logging.error(f'Stall at clock {clk} due to {stall_reg}')
      stall = False
      stall_cntr = stall_cntr+1
    else:
      ins = ins+1
      if ins < len(instr):
        for x in instr_reg[ins]:
          index = reg_copy.index(x)
          if instr_reg[ins].index(x) == 0: # If it's an write register, checks if it's currently being written to and is not repeated in the current instruction
            if reg[index].write and (len(set(instr_reg[ins])) != len(instr_reg[ins])):
              stall = True
              stall_reg = reg[index].name
            else: # If there's no Read-After-Write hazard, but it's overwritten in the next cycle, reset parameters to enable rewrite.
              reg[index].stage = 1
              reg[index].write = True
          else: # For read registers, checks if any other instructions are writing to it
            if reg[index].write:
              stall = True
              stall_reg = reg[index].name
      # Checks if the conditions are met to finish running the program
      run_complete = end_reg(reg) and ins != len(instr)

  # OUTPUTS
  print(f'Ideal clock   : {len(instr)+4}')
  print(f'Current clock : {len(instr)+4+stall_cntr}')
  print(f'Stall delay   : {stall_cntr}')

################################################################################################################