"""
Code: Provides translation of Hack assembly mnemonics into binary codes for A- and C-instructions.
"""
class Code:
    COMPUTATION = {
        "0":   "0101010",
        "1":   "0111111",
        "-1":  "0111010",
        "D":   "0001100",
        "A":   "0110000",
        "M":   "1110000",
        "!D":  "0001101",
        "!A":  "0110001",
        "!M":  "1110001",
        "-D":  "0001111",
        "-A":  "0110011",
        "-M":  "1110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "M+1": "1110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "M-1": "1110010",
        "D+A": "0000010",
        "D+M": "1000010",
        "D-A": "0010011",
        "D-M": "1010011",
        "A-D": "0000111",
        "M-D": "1000111",
        "D&A": "0000000",
        "D&M": "1000000",
        "D|A": "0010101",
        "D|M": "1010101",
    }

    DESTINATION = {
        "":  "000",  # null
        "M":   "001",
        "D":   "010",
        "MD":  "011",
        "A":   "100",
        "AM":  "101",
        "AD":  "110",
        "AMD": "111",
    }

    JUMP = {
        "":  "000",  # null
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }
    @staticmethod
    def translate_A(address: str|int) -> str:
        """
        Translate an A-instruction address into a 16-bit binary string.
        Accepts either an integer or string representation of a number.
        """
        return format(int(address), "016b")

    @classmethod
    def translate_C(cls, clean_line: str) -> str:
        """
        Translate a C-instruction into its 16-bit binary representation.
        Splits the instruction into dest, comp, and jump fields and encodes them.
        """
        if "=" in clean_line:
            dest, rest = clean_line.split("=", 1)
        else:
            dest, rest = "", clean_line
        if ";" in rest:
            comp, jump = rest.split(";", 1)
        else:
            comp, jump = rest, ""

        comp_bits = cls.COMPUTATION.get(comp)
        dest_bits = cls.DESTINATION.get(dest)
        jump_bits = cls.JUMP.get(jump)

        if comp_bits is None:
            raise ValueError(f"Invalid comp field: '{comp}'")
        if dest_bits is None:
            raise ValueError(f"Invalid dest field: '{dest}'")
        if jump_bits is None:
            raise ValueError(f"Invalid jump field: '{jump}'")
        return "111" + comp_bits + dest_bits + jump_bits
    

 