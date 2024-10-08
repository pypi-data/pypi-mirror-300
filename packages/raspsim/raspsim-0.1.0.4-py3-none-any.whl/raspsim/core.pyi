"""
python binding for raspsim, a cycle-accurate x86 simulator based on PTLsim
"""
from __future__ import annotations
import typing
__all__ = ['Address', 'BoundsException', 'BreakpointException', 'CoprocOverrunException', 'Core', 'DebugException', 'DivideException', 'DoubleFaultException', 'FPUException', 'FPUNotAvailException', 'GPFaultException', 'InvalidOpcodeException', 'InvalidTSSException', 'MachineCheckException', 'NMIException', 'OverflowException', 'PageFaultException', 'Prot', 'RaspsimException', 'RegisterFile', 'SSEException', 'SegNotPresentException', 'SpuriousIntException', 'StackFaultException', 'UnalignedException', 'getProtFromELFSegment']
class Address:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, offset: int) -> Address:
        ...
    @typing.overload
    def __setitem__(self, offset: int, value: bytes) -> None:
        ...
    @typing.overload
    def __setitem__(self, offset: int, value: int) -> None:
        ...
    def read(self, size: int = 1) -> bytes:
        """
        Read data from the address
        """
    def write(self, value: bytes) -> None:
        """
        Write data to the address
        """
class BoundsException(Exception):
    pass
class BreakpointException(Exception):
    pass
class CoprocOverrunException(Exception):
    pass
class Core:
    """
    A class to interact with the simulator
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, logfile: str = '/dev/null') -> None:
        """
        Create a new Raspsim instance
        """
    def __str__(self) -> str:
        """
        Get the string representation of the current state of the simulator
        """
    def disableSSE(self) -> None:
        """
        Disable SSE
        """
    def disableX87(self) -> None:
        """
        Disable X87
        """
    def enablePerfectCache(self) -> None:
        """
        Enable perfect cache
        """
    def enableStaticBranchPrediction(self) -> None:
        """
        Enable static branch prediction
        """
    def getMappedPage(self, arg0: int) -> Address:
        """
        Get the mapped page
        """
    def mapPage(self, start: int, prot: Prot) -> Address:
        """
        Map a page to the virtual address space of the simulator
        """
    def memmap(self, start: int, prot: Prot, length: int = 0, data: bytes = b'') -> Address:
        """
        Map a range of memory to the virtual address space of the simulator.
        
        Maps data from `data` into memory and fills the rest with zeros if `length` is greater than the size of `data`. If `length` is 0, the size of `data` will be used as length.
        """
    def run(self) -> None:
        """
        Run the simulator
        """
    @property
    def cycles(self) -> int:
        """
        Get the number of cycles
        """
    @property
    def instructions(self) -> int:
        """
        Get the number of instructions
        """
    @property
    def registers(self) -> RegisterFile:
        """
        Get the register file
        """
class DebugException(Exception):
    pass
class DivideException(Exception):
    pass
class DoubleFaultException(Exception):
    pass
class FPUException(Exception):
    pass
class FPUNotAvailException(Exception):
    pass
class GPFaultException(Exception):
    pass
class InvalidOpcodeException(Exception):
    pass
class InvalidTSSException(Exception):
    pass
class MachineCheckException(Exception):
    pass
class NMIException(Exception):
    pass
class OverflowException(Exception):
    pass
class PageFaultException(Exception):
    pass
class Prot:
    """
    Members:
    
      READ
    
      WRITE
    
      EXEC
    
      NONE
    
      RW
    
      RX
    
      RWX
    """
    EXEC: typing.ClassVar[Prot]  # value = <Prot.EXEC: 4>
    NONE: typing.ClassVar[Prot]  # value = <Prot.NONE: 0>
    READ: typing.ClassVar[Prot]  # value = <Prot.READ: 1>
    RW: typing.ClassVar[Prot]  # value = <Prot.RW: 3>
    RWX: typing.ClassVar[Prot]  # value = <Prot.RWX: 7>
    RX: typing.ClassVar[Prot]  # value = <Prot.RX: 5>
    WRITE: typing.ClassVar[Prot]  # value = <Prot.WRITE: 2>
    __members__: typing.ClassVar[dict[str, Prot]]  # value = {'READ': <Prot.READ: 1>, 'WRITE': <Prot.WRITE: 2>, 'EXEC': <Prot.EXEC: 4>, 'NONE': <Prot.NONE: 0>, 'RW': <Prot.RW: 3>, 'RX': <Prot.RX: 5>, 'RWX': <Prot.RWX: 7>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __and__(self, arg0: Prot) -> bool:
        """
        Check if a protection flag is set
        """
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, arg0: Prot) -> Prot:
        """
        Combine two protection flags
        """
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class RaspsimException(Exception):
    pass
class RegisterFile:
    """
    A class to access the registers of the virtual CPU
    """
    r10: int
    r11: int
    r12: int
    r13: int
    r14: int
    r15: int
    r8: int
    r9: int
    rax: int
    rbp: int
    rbx: int
    rcx: int
    rdi: int
    rdx: int
    rip: int
    rsi: int
    rsp: int
    xmm0: int
    xmm0h: int
    xmm1: int
    xmm10: int
    xmm10h: int
    xmm11: int
    xmm11h: int
    xmm12: int
    xmm12h: int
    xmm13: int
    xmm13h: int
    xmm1h: int
    xmm2: int
    xmm2h: int
    xmm3: int
    xmm3h: int
    xmm4: int
    xmm4h: int
    xmm5: int
    xmm5h: int
    xmm6: int
    xmm6h: int
    xmm7: int
    xmm7h: int
    xmm8: int
    xmm8h: int
    xmm9: int
    xmm9h: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, regname: str) -> int:
        """
        Get the value of a register
        """
    def __setitem__(self, regname: str, value: int) -> None:
        """
        Set the value of a register
        """
class SSEException(Exception):
    pass
class SegNotPresentException(Exception):
    pass
class SpuriousIntException(Exception):
    pass
class StackFaultException(Exception):
    pass
class UnalignedException(Exception):
    pass
def getProtFromELFSegment(flags: int) -> Prot:
    """
    Get the protection as Raspsim Prot from ELF segment flags
    """
