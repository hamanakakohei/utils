#!/usr/bin/env python3

import pandas as pd


def has_header(filepath):
    """1行目がヘッダーかどうかを自動判定（2列目と3列目がintならヘッダーなしと判定）"""
    with open(filepath) as f:
        first_line = f.readline().strip().split("\t")
        try:
            int(first_line[1])
            int(first_line[2])
            return False
        except (ValueError, IndexError):
            return True


def read_bed_with_auto_header(filepath):
    """
    BEDファイルを、ヘッダーの有無を自動判定して読み込む。
    ヘッダーなしの場合、最初の12列に汎用的なBED列名を自動で付ける。
    """
    bed_column_names = [
        "chrom", "start", "end", "name", "score", "strand",
        "thickStart", "thickEnd", "itemRgb", "blockCount", "blockSizes", "blockStarts"
    ]

    if has_header(filepath):
        df = pd.read_csv(filepath, sep="\t", dtype=str)
    else:
        df = pd.read_csv(filepath, sep="\t", header=None, dtype=str)
        num_cols = df.shape[1]
        colnames = bed_column_names[:num_cols] + [f"col{i+1}" for i in range(num_cols - len(bed_column_names))]
        df.columns = colnames[:num_cols]

    return df


def variant_to_bed(input_path, output_path, margin=0):
    """
    Convert variant file (chr:pos:ref:alt + meta) to BED format.
    """
    
    df = pd.read_csv(input_path, sep="\t", header=None, dtype=str)
    df.columns = ["variant_id", "meta"]
    
    # variant_id を分解
    split_cols = df["variant_id"].str.split(":", expand=True)
    split_cols.columns = ["chr", "pos", "ref", "alt"]
    df = pd.concat([df, split_cols], axis=1)
    
    df["pos"] = df["pos"].astype(int)
    df["start"] = df["pos"] - 1
    df["end"] = df["start"] + df["ref"].str.len()
    if margin > 0:
        df["start"] = df["start"] - margin
        df["end"] = df["end"] + margin
        df["start"] = df["start"].clip(lower=0)
    
    df["name"] = df["variant_id"] + ";" + df["meta"]
    df = df.sort_values(["chr", "start"])
    df[["chr", "start", "end", "name"]].to_csv(output_path, sep="\t", header=False, index=False)
