import argparse
import os
from typing import Union
from modvcfsamples import sample

def run(vcfs: list[str], only: list[str], gt: Union[int, None], output_dir: str):
    for vcf in vcfs:
        vcf_records, header = sample.get_records_from_vcf(vcf)
        modified_vcfs = vcf_records
        modified_header = header
        if len(only) > 0:
            modified_vcfs, modified_header = sample.keep_specific_call_data(modified_vcfs, modified_header, *only)
        if gt is not None:
            modified_vcfs, modified_header = sample.normalize_gt_to_length(modified_vcfs, modified_header, gt)
        sample.write_records_to_vcf(modified_vcfs, modified_header, os.path.join(output_dir, os.path.basename(vcf)))

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
        "--gt-norm",
        "-g",
        help="Resizes haploid genotypes to n-ploid by repeating it.",
        type=int,
        required=False
    )
    parser.add_argument(
        "--only",
        "-n",
        help="Remove everything but the sample datatype",
        action="append",
        type=str,
        required=False
    )

    args = parser.parse_args()
    run(args.vcfs, args.only, args.gt_norm, args.output_dir)


if __name__ == "__main__":
    main()
