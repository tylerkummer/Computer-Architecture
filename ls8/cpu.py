"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
SP = 7


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
        # Set running to True for the while loop we use
        self.running = True
        # Set up branchtable functions
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[MUL] = self.mul
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop

    # Accept address to read
    def ram_read(self, address):
        # Return the value stored in address
        return self.ram[address]

    # Accept a value to write and an address to write to
    def ram_write(self, value, address):
        # Set the address to the value
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) < 2:
            print("Usage: filename.py filename")
            sys.exit()

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    self.ram[address] = int(n, 2)
                    address += 1
        except:
            print("File Not Found")
            sys.exit()

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

    # Functions that take in operand_a and operand_b
    def hlt(self, operand_a, operand_b):
        self.running = False

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def push(self, operand_a, operand_b):
        pass

    def pop(self, operand_a, operand_b):
        pass

    def run(self):
        """Run the CPU."""

        while self.running:
            # Read memory address thats in PC and store in IR
            ir = self.ram[self.pc]
            # Ram_Read the bytes PC + 1 and PC + 2
            # Store them in operand_a and operand_b
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # Set the branch operation and pass operand_a and operand_b
            self.branchtable[ir](operand_a, operand_b)
