#!/usr/bin/env python3

from pathlib import Path

def write_seq_as_fasta(
    seq: str,
    header: str,
    output_path: str | Path,  # Python 3.10以降（3.9以前は Union[str, Path]）
    row_len: int = 60,
    mode: str = 'w'
) -> None:
    """
    Args:
        header: ヘッダー行
        row_len: 各行を何塩基にするか
        mode: 'w' (write) か 'a' (append)
    """
    output_path = Path(output_path)

    with output_path.open(mode) as out:
        out.write(header + '\n')
        for i in range(0, len(seq), row_len):
            out.write(seq[i:i + row_len] + '\n')
