from Bio import Entrez
from Bio import SeqIO
import time

Entrez.email = "laspamlaspam@gmail.com"

# Search for the valid ID using esearch
search_handle = Entrez.esearch(db="nucleotide", term="NC_000001.11", retmode="xml")
search_record = Entrez.read(search_handle)
search_handle.close()

if search_record["IdList"]:
    valid_id = search_record["IdList"][0]
    print(f"Valid ID: {valid_id}")
else:
    print("No valid ID found.")


id_number = valid_id
with Entrez.efetch(db="nucleotide", id=id_number, rettype="fasta", retmode="text") as handle:
    record = SeqIO.read(handle, "fasta")
    print(f"Gene ID: {record.id}")
    print(f"Description: {record.description}")
    print(f"Sequence:\n{record.seq[16:68722497]}...")

    185,428,566 - 185,428,623