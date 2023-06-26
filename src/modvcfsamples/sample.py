import vcf
from collections import namedtuple
from copy import deepcopy

def get_records_from_vcf(path: str):
    vcf_records = []
    with open(path, "r") as vcf_stream:
        reader = vcf.Reader(vcf_stream)
        for record in reader:
            vcf_records.append(record)

    return vcf_records

def filter_sample_datatype(record, *datatypes: str):
    call_data = namedtuple("Data", *datatypes)
    filtered_calls = []
    modified_record = deepcopy(record)
    for call in record.samples:
        kept_data = {}
        for datatype in datatypes:
            kept_data[datatype] = call[datatype]
        filtered_calls.append(call_data(**kept_data))
    modified_record.samples = filtered_calls
    return modified_record

def filter_all_sample_datatypes(records: list, *datatypes: str):
    for record in records:
        yield filter_sample_datatype(record, *datatypes)

def write_records_to_vcf(records: list, path: str):
    with open(path, "w") as vcf_stream:
        writer = vcf.Writer(vcf_stream, records[0])
        for record in records:
            writer.write_record(record)