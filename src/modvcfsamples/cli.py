import argparse
import os
from modvcfsamples import sample

def run(vcfs: list[str], only: list[str], output_dir: str):
    for vcf in vcfs:
        vcf_records, header = sample.get_records_from_vcf(vcf)
        processed_vcfs, modified_header = sample.keep_specific_call_data(vcf_records, header, *only)
        sample.write_records_to_vcf(processed_vcfs, modified_header, os.path.join(output_dir, os.path.basename(vcf)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "vcfs",
        help="The VCFs to run filtering on",
        nargs="+",
        metavar="I",
        type=str
    )
    parser.add_argument(
        "output_dir",
        help="The output directory",
        metavar="O",
        type=str
    )
    parser.add_argument(
        "--only",
        "-n",
        help="Remove everything but the sample datatype",
        action="append",
        type=str
    )

    args = parser.parse_args()
    run(args.vcfs, args.only, args.output_dir)


if __name__ == "__main__":
    main()
