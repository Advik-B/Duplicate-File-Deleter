from dataclasses import dataclass
from xxhash import xxh64
from os import path

@dataclass
class QuickHasher:
    path: str
    file_hash: str

    @staticmethod
    def from_file(file_path: str, MAX_BUFFER_SIZE: int) -> 'QuickHasher':
        hasher = xxh64()
        file_size = path.getsize(file_path)
        if file_size <= MAX_BUFFER_SIZE:
            return QuickHasher(
                file_hash=QuickHasher.__perfect_fsize(
                    file_path,
                    hasher,
                ),
                path=path.abspath(file_path)
            )

        return QuickHasher(
            file_hash=QuickHasher.__imperfect_fsize(
                file_path,
                hasher,
            ),
            path=path.abspath(file_path),
            MAX_BUFFER_SIZE=MAX_BUFFER_SIZE,
        )

    @staticmethod
    def __perfect_fsize(file_path: str, hasher: xxh64) -> str:
        with open(file_path, 'rb') as file:
            hasher.update(file.read())
            return hasher.hexdigest()

    @staticmethod
    def __imperfect_fsize(file_path: str, hasher: xxh64, MAX_BUFFER_SIZE) -> str:
        with open(file_path, 'rb') as file:
            hasher.update(file.read(MAX_BUFFER_SIZE))
            # Skip to the last part of the file and update the hasher with the last bit of data
            file.seek(-MAX_BUFFER_SIZE, 2)
            hasher.update(file.read())
            return hasher.hexdigest()

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, QuickHasher):
            return self.file_hash == __value.file_hash
        return False