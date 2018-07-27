from abc import abstractproperty, abstractmethod

import capstone as cs


class Instruction(object):
    """Capstone-like instruction to be used internally
    """
    @abstractproperty
    def address(self):
        pass

    @abstractproperty
    def mnemonic(self):
        pass

    @abstractproperty
    def op_str(self):
        pass

    @abstractproperty
    def size(self):
        pass

    @abstractproperty
    def operands(self):
        pass

    # FIXME (theo) eliminate one of the two of insn_name, name
    @abstractproperty
    def insn_name(self):
        pass

    @abstractproperty
    def name(self):
        pass


class Disasm(object):
    """Abstract class for different disassembler interfaces"""

    def __init__(self, disasm):
        self.disasm = disasm

    @abstractmethod
    def disassemble_instruction(self, code, pc):
        """Get next instruction based on the disassembler in use

        :param str code: binary blob to be disassembled
        :param long pc: program counter
        """


class CapstoneDisasm(Disasm):
    def __init__(self, arch, mode):
        try:
            cap = cs.Cs(arch, mode)
        except Exception as e:
            raise e
        cap.detail = True
        cap.syntax = 0
        super().__init__(cap)

    def disassemble_instruction(self, code, pc):
        """Get next instruction using the Capstone disassembler

        :param str code: binary blob to be disassembled
        :param long pc: program counter
        """
        return next(self.disasm.disasm(code, pc))


def init_disassembler(disassembler, arch, mode, view=None):
    if disassembler == "capstone":
        return CapstoneDisasm(arch, mode)
    else:
        raise NotImplementedError("Disassembler not implemented")
