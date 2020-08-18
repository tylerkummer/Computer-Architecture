"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # RAM holds 256 bytes of memory
        self.ram = [0] * 256
        # Create 8 general purpose registers registers
        self.reg = [0] * 8
        # Set PC to 0 as a counter
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) < 2:
            print("Usage: filename.py filename\n")
            sys.exit()

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue
        except:
            print("File Not Found")
            sys.exit()

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            # Read memory address thats in PC and store in IR
            IR = self.ram_read(self.pc)
            # Ram_Read the bytes PC + 1 and PC + 2
            # Store them in operand_a and operand_b
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # Use an if statement to check for the binary of HLT, LDI and PRN
            # Then call the functions with the appropriate parameters
            if IR == 0b00000001:
                self.hlt()
            elif IR == 0b10000010:
                self.ldi(operand_a, operand_b)
            elif IR == 0b01000111:
                self.prn(operand_a)

    # Accept address to read
    def ram_read(self, address):
        # Return the value stored in address
        return self.ram[address]

    # Accept a value to write and an address to write to
    def ram_write(self, value, address):
        # Set the address to the value
        self.ram[address] = value

    # Create an hlt function that will exit the program.
    def hlt(self):
        sys.exit()

    # Create an ldi function that assigns the register of operand_a to operand_b
    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        # Update the PC to go to the next instruction in the loop
        self.pc += 3

    # Create a prn that will print the reg place of operand_a
    def prn(self, operand_a):
        print(self.reg[operand_a])
        # Update the PC to go to the next instruction in the loop
        self.pc += 2
