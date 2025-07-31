#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from typing import Union


def read_vcf_as_df(vcf_path: Union[str, Path]) -> pd.DataFrame:
    vcf_path = Path(vcf_path)
    vcf_df = pd.read_csv(vcf_path, comment='#', sep='\t', header=None)
    
    with vcf_path.open() as f:
        for line in f:
            if line.startswith('#CHROM'):
                header = line.strip().lstrip('#').split('\t')
                vcf_df.columns = header
                break

    return vcf_df


def read_vcf_as_df_4_alphagenome(vcf_path: Union[str, Path], genome_build = 'b38') -> pd.DataFrame:
    vcf_df = read_vcf_as_df(vcf_path)
    vcf_df["variant_id"] = vcf_df.apply(
        lambda row: f"{row['CHROM']}_{row['POS']}_{row['REF']}_{row['ALT']}_{genome_build}", axis=1
    )
    return vcf_df[["variant_id", "CHROM", "POS", "REF", "ALT"]]
