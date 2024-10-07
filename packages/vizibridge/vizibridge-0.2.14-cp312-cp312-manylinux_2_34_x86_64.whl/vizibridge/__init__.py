from vizibridge.DNA import DNA
from vizibridge.kmers import Kmer
from vizibridge.kmer_index import KmerIndex

del kmers


def kmer_from_str(dna: str) -> Kmer:
    return Kmer.from_dna(next(DNA.from_str(dna)))
