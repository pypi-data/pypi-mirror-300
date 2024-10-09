from dataclasses import dataclass
from typing import Any, Dict

from pystratum_common.wrapper.helper.PythonCodeStore import PythonCodeStore


@dataclass
class WrapperContext:
    """
    The build context for generating wrapper methods for invoking stored routines.
    """
    # ------------------------------------------------------------------------------------------------------------------
    code_store: PythonCodeStore
    """
    The Python code store for, well, storing the generated Python code.
    """

    pystratum_metadata: Dict[str, Any]
    """
    The metadata of the stored routine.
    """

# ----------------------------------------------------------------------------------------------------------------------
