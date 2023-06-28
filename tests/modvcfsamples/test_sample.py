from modvcfsamples.sample import (
    keep_specific_call_data,
    get_records_from_vcf,
    normalize_gt_to_length,
    replace_sample_names,
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
    modified_records = normalize_gt_to_length(records, 4)
    assert len(modified_records) > 0


def test_normalize_gt_to_length_gt_normalized():
    records, header = get_records_from_vcf(
        os.path.abspath("tests/resources/test_files_shortened_haploid.vcf")
    )
    modified_records = normalize_gt_to_length(records, 4)
    for modified_record in modified_records:
        for call in modified_record.calls:
            assert len(call.data["GT"].split("|")) == 4 or "/" in call.data["GT"]

def test_replace_sample_names_record_modified_correctly():
    records, header = get_records_from_vcf(
        os.path.abspath("tests/resources/test_files_shortened_haploid.vcf")
    )
    modified_records, modified_headers = replace_sample_names(records, header, "Gambian", "different")
    for modified_record in modified_records:
        call_name_replaced = False
        for call in modified_record.calls:
            assert call.sample != "Gambian"
            if call.sample == "different":
                call_name_replaced = True
        assert call_name_replaced


def test_replace_sample_names_header_modified_correctly():
    records, header = get_records_from_vcf(
        os.path.abspath("tests/resources/test_files_shortened_haploid.vcf")
    )
    modified_records, modified_headers = replace_sample_names(records, header, "Gambian", "different")
    replaced_found = False
    original_found = False
    for name in modified_headers.samples.names:
        if name == "Gambian":
            original_found = True

        if name == "different":
            replaced_found = True
    assert replaced_found
    assert not original_found