from modvcfsamples.sample import (
    keep_specific_call_data,
    get_records_from_vcf,
    normalize_gt_to_length,
)
import os


def test_filter_all_sample_datatypes_not_empty():
    records, header = get_records_from_vcf(
        os.path.abspath("tests/resources/test_files_shortened.vcf")
    )
    filter_for = ["GT"]
    modified_records, header = keep_specific_call_data(records, header, *filter_for)
    assert len(modified_records) == 11


def test_filter_all_sample_datatypes_filtered():
    records, header = get_records_from_vcf(
        os.path.abspath("tests/resources/test_files_shortened.vcf")
    )
    filter_for = ["GT"]
    modified_records, header = keep_specific_call_data(records, header, *filter_for)
    for modified_record in modified_records:
        for call in modified_record.calls:
            assert len(call.data.keys()) <= len(filter_for)
            for key, _ in call.data.items():
                assert key in filter_for


def test_normalize_gt_to_length_not_empty():
    records, header = get_records_from_vcf(
        os.path.abspath("tests/resources/test_files_shortened_haploid.vcf")
    )
    modified_records, _ = normalize_gt_to_length(records, header, 4)
    assert len(modified_records) > 0


def test_normalize_gt_to_length_gt_normalized():
    records, header = get_records_from_vcf(
        os.path.abspath("tests/resources/test_files_shortened_haploid.vcf")
    )
    modified_records, _ = normalize_gt_to_length(records, header, 4)
    for modified_record in modified_records:
        for call in modified_record.calls:
            assert len(call.data["GT"].split("|")) == 4 or "/" in call.data["GT"]
