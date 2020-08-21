"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


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
        # Create an sp set to 7
        self.sp = 7
        # Create a reg of that sp set to 0xF4
        self.reg[self.sp] = 0xF4
        # Set flag for CMP
        self.fl = 0b00000000
        # Set up branchtable functions
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[ADD] = self.add
        self.branchtable[MUL] = self.mul
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        self.branchtable[CMP] = self.cmp_
        self.branchtable[JMP] = self.jmp
        self.branchtable[JEQ] = self.jeq
        self.branchtable[JNE] = self.jne

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
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            # Check if reg a and b are equal
            if self.reg[reg_a] == self.reg[reg_b]:
                # If they are then set E flag to 1
                self.fl = 0b00000001
            # Check if reg a is greater than reg b
            elif self.reg[reg_a] > self.reg[reg_b]:
                # If so then set G flag to 1
                self.fl = 0b00000010
            # Check if reg a is less than reg b
            elif self.reg[reg_a] < self.reg[reg_b]:
                # If so then set L flag to 1
                self.fl = 0b00000100
            # If none of them work then just set to 0
            else:
                self.fl = 0b00000000
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

    def add(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

    def mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def cmp_(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3

    def push(self, operand_a, operand_b):
        # Subtract sp by one since we are popping it off
        self.sp -= 1
        # Reassign the ram sp to our reg operand_a
        self.ram[self.sp] = self.reg[operand_a]
        # Add pc by 2 for the next iteration
        self.pc += 2

    def pop(self, operand_a, operand_b):
        # In reverse this time set our reg operand a to our ram sp
        self.reg[operand_a] = self.ram[self.sp]
        # Add pc by 1 since we are adding it on
        self.sp += 1
        # Add pc by 2 for the next iteration
        self.pc += 2

    def call(self, operand_a, operand_b):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        value = self.ram[self.pc + 1]
        self.pc = self.reg[value]

    def ret(self, operand_a, operand_b):
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def jmp(self, operand_a, operand_b):
        # Set pc to the value of the given register (operand_a)
        self.pc = self.reg[operand_a]

    def jeq(self, operand_a, operand_b):
        # Use the and operator to check if self.fl is set to True
        equal = self.fl & 0b00000001
        # Check if equal is set to 1 or True
        if equal:
            # If it is jump to the address in the stored register (operand_a)
            self.pc = self.reg[operand_a]
        else:
            # If not then just cycle through pc
            self.pc += 2

    def jne(self, operand_a, operand_b):
       # Use the and operator to check if self.fl is set to False
        equal = self.fl & 0b00000001
        # Check if equal is set to 0 or False
        if not equal:
            # If it is jump to the address in the stored register (operand_a)
            self.pc = self.reg[operand_a]
        else:
            # If not then just cycle through pc
            self.pc += 2

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
