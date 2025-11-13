#!/usr/bin/env python3
"""
Fix mixed-encoding CSV files by detecting line encodings
and rewriting them as UTF-8.
"""

import chardet
from ftfy import fix_text
import argparse


def fix_csv(input_file, output_file):
    with (
        open(input_file, "rb") as f_in,
        open(output_file, "w", encoding="utf-8", newline="") as f_out,
    ):
        for raw_line in f_in:
            # Detect encoding of this line
            result = chardet.detect(raw_line)
            enc = result["encoding"] or "utf-8"

            try:
                decoded_line = raw_line.decode(enc)
            except Exception:
                decoded_line = raw_line.decode("utf-8", errors="replace")

            # Clean mojibake if present
            decoded_line = fix_text(decoded_line)

            f_out.write(decoded_line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix mixed-encoding CSV to UTF-8")
    parser.add_argument("input", help="Input CSV file with mixed encodings")
    parser.add_argument("output", help="Output cleaned CSV file (UTF-8)")
    args = parser.parse_args()

    fix_csv(args.input, args.output)
    print(f"✅ Cleaned file written to {args.output}")
