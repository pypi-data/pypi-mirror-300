"""MQT Core - The Backbone of the Munich Quantum Toolkit."""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_8_2():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_core.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-mqt_core-2.7.0')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-mqt_core-2.7.0')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_8_2()
del _delvewheel_patch_1_8_2
# end delvewheel patch

from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Union

from ._version import version as __version__
from ._version import version_tuple as version_info
from .ir import QuantumComputation

if TYPE_CHECKING:
    from qiskit.circuit import QuantumCircuit

    """The type of input that can be used to load a quantum circuit."""
    CircuitInputType = Union[QuantumComputation, str, PathLike[str], QuantumCircuit]


def load(input_circuit: CircuitInputType) -> QuantumComputation:
    """Load a quantum circuit from any supported format as a :class:`~mqt.core.ir.QuantumComputation`.

    Args:
        input_circuit: The input circuit to translate to a :class:`~mqt.core.ir.QuantumComputation`. This can be a :class:`~mqt.core.ir.QuantumComputation` itself, a file name to any of the supported file formats, an OpenQASM (2.0 or 3.0) string, or a Qiskit :class:`~qiskit.circuit.QuantumCircuit`.

    Returns:
        The :class:`~mqt.core.ir.QuantumComputation`.

    Raises:
        ValueError: If the input circuit is a Qiskit :class:`~qiskit.circuit.QuantumCircuit` but the `qiskit` extra is not installed.
        FileNotFoundError: If the input circuit is a file name and the file does not exist.
    """
    if isinstance(input_circuit, QuantumComputation):
        return input_circuit

    if isinstance(input_circuit, (str, PathLike)):
        if not Path(input_circuit).is_file():
            if isinstance(input_circuit, PathLike) or "OPENQASM" not in input_circuit:
                msg = f"File {input_circuit} does not exist."
                raise FileNotFoundError(msg)
            # otherwise, we assume that this is a QASM string
            return QuantumComputation.from_qasm(str(input_circuit))

        return QuantumComputation(str(input_circuit))

    try:
        from .plugins.qiskit import qiskit_to_mqt
    except ImportError:
        msg = "Qiskit is not installed. Please install `mqt.core[qiskit]` to use Qiskit circuits as input."
        raise ValueError(msg) from None

    return qiskit_to_mqt(input_circuit)


__all__ = [
    "__version__",
    "load",
    "version_info",
]
if TYPE_CHECKING:
    __all__ += ["CircuitInputType"]
