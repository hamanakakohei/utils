#!/usr/bin/env python3

import numpy as np
from typing import Optional
import pyBigWig


def get_bw_values_of_a_interval(
    url: str, chrom: str, start: int, end: int,
    nan_to_zero: bool = True,
    out_file: Optional[str] = None
) -> Optional[np.ndarray]:
    """
    Fetch values from a BigWig file over a specified interval.
    url例:
        - http://hgdownload.soe.ucsc.edu/gbdb/hg38/phyloP100way/phyloP100way.bw
        - https://hgdownload.soe.ucsc.edu/gbdb/hg38/fantom5/ctssTotalCounts.fwd.bw
    Returns:
        If out_file is None, returns the array. Otherwise, saves to file.
    """
    with pyBigWig.open(url) as bw:
        values = bw.values(chrom, start, end, numpy=True)

    arr = np.array(values, dtype=np.float32).reshape(-1, 1)
    if nan_to_zero:
        arr = np.nan_to_num(arr, nan=0.0)

    if out_file:
        np.save(out_file, arr)
        return None
    else:
        return arr
