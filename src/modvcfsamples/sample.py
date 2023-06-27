from typing import Iterable, OrderedDict
import vcfpy
from collections import namedtuple
from copy import deepcopy
import os

from vcfpy.record import Call


def get_records_from_vcf(path: str):
    vcf_records = []
    with open(path, "r") as vcf_stream:
        reader = vcfpy.Reader.from_stream(vcf_stream)
        for record in reader:
            vcf_records.append(record)

    return vcf_records, reader.header


def keep_specific_call_data(records: list[vcfpy.Record], header: vcfpy.Header, *datatypes: str):
    lines_kept = [line for line in header.lines if line.key != "FORMAT"]
    lines_kept.extend([line for line in header.get_lines("FORMAT") if line.id in datatypes])
    modified_header = vcfpy.Header(lines_kept, header.samples)
    modified_records = []

    for record in records:
        modified_calls = []
        for call in record.calls:
            kept_data = OrderedDict()
            for datatype in datatypes:
                kept_data[datatype] = call.data[datatype]
            modified_calls.append(Call(call.sample, kept_data, record))
        modified_record = vcfpy.Record(
            record.CHROM,
            record.POS,
            record.ID,
            record.REF,
            record.ALT,
            record.QUAL,
            record.FILTER,
            record.INFO,
            datatypes,
            modified_calls,
        )
        modified_records.append(modified_record)
    return modified_records, modified_header

def normalize_gt_to_length(records: list[vcfpy.Record], header: vcfpy.Header, num: int):
    modified_records = []
    for record in records:
        modified_calls = []
        for call in record.calls:
            gt_parts = call.data['GT'].replace("/", "|").split("|")
            modified_call = deepcopy(call)
            if len(gt_parts) > 1:
                # TODO Add logging and output if gt_parts is longer.
                pass
            else:
                modified_call.data['GT'] = "|".join([gt_parts[0]]  * num)
            modified_calls.append(modified_call)
        modified_record = vcfpy.Record(
            record.CHROM,
            record.POS,
            record.ID,
            record.REF,
            record.ALT,
            record.QUAL,
            record.FILTER,
            record.INFO,
            record.FORMAT,
            modified_calls,
        )
        modified_records.append(modified_record)
    return modified_records, header

def write_records_to_vcf(records: Iterable[vcfpy.Record], header: vcfpy.Header, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as vcf_stream:
        writer = vcfpy.Writer.from_stream(vcf_stream, header)
        for record in records:
            writer.write_record(record)
