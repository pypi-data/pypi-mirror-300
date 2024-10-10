from bitarray import bitarray, decodetree
from bitarray.util import deserialize, serialize
from dataclasses import dataclass
import gzip
import mmap
import numpy as np
from pathlib import Path
import re
from tqdm import tqdm
from typing import Iterable, Iterator, Union

class Fasta:
    """
    An indexable memory-mapped interface for FASTA files.
    """
    @dataclass
    class Entry:
        _fasta_file: "Fasta"
        _id_start: int
        _id_end: int
        _sequence_start: int
        _sequence_end: int

        @property
        def id(self):
            return self._fasta_file.data[self._id_start:self._id_end]

        @property
        def metadata(self):
            return self._fasta_file.data[self._id_end+1:self._sequence_start-1]

        @property
        def sequence(self):
            return self._fasta_file.data[self._sequence_start:self._sequence_end]

        def __len__(self):
            return len(self.sequence)

        def __str__(self):
            return ">" + (self.id.decode() + " " + self.metadata.decode()).strip() \
                + '\n' + self.sequence.decode()

        def __repr__(self):
            return "Entry:\n" + str(self)

    @classmethod
    def open(cls, path: Union[Path, str]):
        with open(path, "r+", encoding="utf8") as f:
            return cls(mmap.mmap(f.fileno(), 0))

    def __init__(self, data):
        self.data = data
        self.entries = []
        self.id_map = {}
        # Lazy reading
        self._length = None
        self._reader = re.finditer(b'>[^>]+', self.data)
        self._eof = False

    def __iter__(self):
        yield from self.entries
        while self._read_next_entry():
            yield self.entries[-1]

    def __getitem__(self, key):
        if not isinstance(key, int):
            while key not in self.id_map and self._read_next_entry():
                continue
            key = self.id_map[key]
        else:
            while len(self.entries) <= key and self._read_next_entry():
                continue
        return self.entries[key]

    def __len__(self):
        if self._length is None:
            self._length = len(re.findall(b'>', self.data))
            if self._length == len(self.entries):
                self._clean_lazy_loading()
        return self._length

    def _read_next_entry(self):
        try:
            match = next(self._reader)
            group = match.group()
            header_end = group.index(b'\n')
            sequence_id_start = match.start() + 1
            sequence_id_end = match.start() + ((group.find(b' ') + 1) or (header_end + 1)) - 1
            sequence_start = match.start() + header_end + 1
            sequence_end = match.end() - 1
            self.entries.append(self.Entry(self, sequence_id_start, sequence_id_end, sequence_start, sequence_end))
            self.id_map[group[1:header_end]] = len(self.id_map)
        except StopIteration:
            self._length = len(self.entries)
        if not self._eof and self._length == len(self.entries):
            self._eof = True
            self._clean_lazy_loading()
        return not self._eof

    def _clean_lazy_loading(self):
        self.__getitem__ = lambda k: self.entries[self.id_map[k] if isinstance(k, str) else k]


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
        encoded.encode(SequenceDb.huffman_codes, sequence)
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
            f.write(n.tobytes())
            f.write(block_size.tobytes())
            if progress:
                encoded_sequences = tqdm(encoded_sequences)
            for sequence in encoded_sequences:
                length = len(sequence).to_bytes(2, "big", signed=False)
                entry = length + sequence + b'\x00'*(block_size - 2 - len(sequence))
                f.write(entry)

    def __init__(self, database: Union[Path, str, bytes]):
        """
        Open and interface with an existing SequenceDb file.
        """
        if isinstance(database, (Path, str)):
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
        Iterate over all sequences within this container instance.
        """
        return (self[i] for i in range(len(self)))

    def __len__(self) -> int:
        """
        The number of sequences within this container instance.
        """
        return self.length
