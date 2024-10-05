import io
import pathlib
from contextlib import contextmanager
from typing import Generator


class BinaryManager:
    def get_data_path_by_name(self, name: str) -> pathlib.Path:
        ...

    def register_binary_path(self, name: str, path: str) -> None:
        ...

    def execute_binary(self, name: str, cmd_args: list[str], timeout: int,
                       error_manage: bool = True, separate_output: bool = True, text: bool = True) \
            -> tuple[str | bytes, str | bytes]:
        ...

    def clear_outs_folder(self):
        ...

    def check_binary(self, name: str) -> bool:
        ...

    @contextmanager
    def open_file(self, name: str, file_name: str) -> Generator[io.IOBase, None, None]:
        ...
