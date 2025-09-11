#!/usr/bin/env python3
import pandas as pd
import re


def remove_gene_rows(gtf_df: pd.DataFrame) -> pd.DataFrame:
    """
    GTF DataFrameから 'feature' 列が 'gene' の行を除外して返す。
    """
    return gtf_df[gtf_df["feature"] != "gene"].copy()


def add_gene_to_transcript_id(gtf_df: pd.DataFrame) -> pd.DataFrame:
    """
    transcript_id に gene_id を付加して「GENEID_TRANSCRIPTID」の形式に変換する。
    """
    df = gtf_df.copy()
    df["transcript_id"] = df["gene_id"].astype(str) + "_" + df["transcript_id"].astype(str)
    return df


def make_attributes_from_columns(row: pd.Series, col_list: list[str]) -> str:
    """
    指定した列名リストから attribute 文字列を作成。
    'col "value"; col "value";' 形式にする。
    """
    parts = []
    for col in col_list:
        if col in row and pd.notna(row[col]):
            parts.append(f'{col} "{row[col]}"')
    return "; ".join(parts) + ";" if parts else ""


def update_attribute_column(df: pd.DataFrame,
                            attr_cols: list[str]) -> pd.DataFrame:
    """
    DataFrameに attribute 列を（attr_cols を組み合わせて）追加/更新する。
    """
    df = df.copy()
    def make_attr(row):
        return make_attributes_from_columns(row, attr_cols)
    #
    df["attribute"] = df.apply(make_attr, axis=1)
    return df


#def update_attribute_column(df: pd.DataFrame,
#                            gene_cols: list[str],
#                            other_cols: list[str]) -> pd.DataFrame:
#    """
#    DataFrameに attribute 列を追加/更新する。
#    feature == "gene" の行は gene_cols を使用。
#    それ以外は other_cols を使用。
#    """
#    df = df.copy()    
#    def make_attr(row):
#        if row["feature"] == "gene":
#            return make_attributes_from_columns(row, gene_cols)
#        else:
#            return make_attributes_from_columns(row, other_cols)
#
#    df["attribute"] = df.apply(make_attr, axis=1)
#    return df
                              

def set_score_frame_to_dot(df: pd.DataFrame) -> pd.DataFrame:
    """
    DataFrameの 'score' と 'frame' 列を '.' に置き換える。
    """
    df = df.copy()
    df["score"] = "."
    df["frame"] = "."
    return df
  

def df_to_gtf(df: pd.DataFrame, output_path: str) -> None:
    """
    DataFrameをGTF形式で保存。
    """
    gtf_cols = ["seqname","source","feature","start","end","score","strand","frame","attribute"]
    df[gtf_cols].to_csv(output_path, sep="\t", header=False, index=False, quoting=3)
