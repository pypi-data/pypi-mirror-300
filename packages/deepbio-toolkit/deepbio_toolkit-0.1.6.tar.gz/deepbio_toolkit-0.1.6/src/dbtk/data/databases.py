from bitarray import bitarray, decodetree
from bitarray.util import deserialize, serialize
import gzip
import mmap
import numpy as np
from pathlib import Path
import re
from tqdm import tqdm
from typing import Iterable, Union

class SequenceDb:
    """
    A compact sequence storage container using huffman encodings to compress
    DNA sequences, and memory-mapping for fast reads.
    """
    huffman_codes = {
        'N': bitarray('000'),
        'C': bitarray('001'),
        'T': bitarray('01'),
        'A': bitarray('10'),
        'G': bitarray('11')
    }
    decode_tree = decodetree(huffman_codes)

    __slots__ = ["data", "length", "block_size"]

    @staticmethod
    def _encode_sequence(sequence: str) -> bytes:
        encoded = bitarray()
        encoded.encode(SequenceDb.huffman_codes, re.sub(r"[^ACTGN]", "N", sequence))
        return serialize(encoded)

    @staticmethod
    def _decode_sequence(sequence: bytes) -> str:
        return "".join(deserialize(sequence).decode(SequenceDb.decode_tree))

    @staticmethod
    def create(path, sequences: Iterable[str], progress: bool = True):
        """
        Write the given sequences to a new SequenceDb at the given path.
        """
        with open(path, "wb") as f:
            encoded_sequences = list(map(SequenceDb._encode_sequence, sequences))
            n = np.uint32(len(encoded_sequences))
            block_size = np.uint32(2 + max(map(len, encoded_sequences)))
            header = n.tobytes() + block_size.tobytes()
            f.write(n.tobytes())
            f.write(block_size.tobytes())
            if progress:
                encoded_sequences = tqdm(encoded_sequences)
            for sequence in encoded_sequences:
                length = len(sequence).to_bytes(2, "big", signed=False)
                entry = length + sequence + b'\x00'*(block_size - 2 - len(sequence))
                f.write(entry)

    def __init__(self, database: Union[str, Path, bytes]):
        """
        Open and interface with an existing SequenceDb file.
        """
        if isinstance(database, (str, Path)):
            database = Path(database)
            if database.name.endswith(".gz"):
                with gzip.open(database, "rb") as f:
                    self.data = f.read()
            else:
                with open(database, "r+b") as f:
                    self.data = mmap.mmap(f.fileno(), 0)
        else:
            self.data = database
        self.length, self.block_size = np.frombuffer(self.data, count=2, dtype=np.uint32)

    def __getitem__(self, index) -> str:
        """
        Get the DNA sequence at the given index.
        """
        index = 8 + self.block_size*index
        length = int.from_bytes(self.data[index:index+2], "big")
        return self._decode_sequence(self.data[index+2:index+2+length])

    def __iter__(self) -> Iterator[str]:
        """
        Return an iterator over all sequences.
        """
        return (self[i] for i in range(len(self)))

    def __len__(self) -> int:
        """

        """
        return self.length

    # def sample(self, n: Optional[int] = None):

