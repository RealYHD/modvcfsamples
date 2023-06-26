from modvcfsamples.sample import filter_sample_datatype, filter_all_sample_datatypes, get_records_from_vcf
import os

def test_get_records_from_vcf_not_none():
    records = get_records_from_vcf(os.path.abspath("tests/resources/test_files_shortened.vcf"))
    assert len(records) > 0

def test_filter_sample_datatype_not_none():
    records = get_records_from_vcf(os.path.abspath("tests/resources/test_files_shortened.vcf"))
    filter_for = ["GT"]
    modified_record = filter_sample_datatype(records[0], *filter_for)
    assert modified_record is not None

def test_filter_sample_datatype_only_filtered():
    records = get_records_from_vcf(os.path.abspath("tests/resources/test_files_shortened.vcf"))
    filter_for = ["GT"]
    modified_record = filter_sample_datatype(records[0], *filter_for)
    for sample in modified_record.samples:
        assert len(sample) <= len(filter_for)
        for key, _ in sample._asdict().items():
            assert key in filter_for

def test_filter_all_sample_datatypes_not_empty():
    records = get_records_from_vcf(os.path.abspath("tests/resources/test_files_shortened.vcf"))
    filter_for = ["GT"]
    modified_records = list(filter_all_sample_datatypes(records, *filter_for))
    assert len(modified_records) == 11

def test_filter_all_sample_datatypes_filtered():
    records = get_records_from_vcf(os.path.abspath("tests/resources/test_files_shortened.vcf"))
    filter_for = ["GT"]
    modified_records = list(filter_all_sample_datatypes(records, *filter_for))
    for modified_record in modified_records:
        for sample in modified_record.samples:
            assert len(sample) <= len(filter_for)
            for key, _ in sample._asdict().items():
                assert key in filter_for

