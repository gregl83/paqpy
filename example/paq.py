import argparse
import sys
import paqpy

def main():
    parser = argparse.ArgumentParser(
        description="Hash file or directory recursively."
    )
    parser.add_argument(
        "source",
        help="Source to hash (filesystem path)"
    )
    parser.add_argument(
        "--ignore-hidden", "-i",
        action="store_true",
        help="Ignore files or directories starting with dot or full stop (default: ignored)"
    )

    args = parser.parse_args()

    ignore_hidden = not args.ignore_hidden

    try:
        hash_result = paqpy.hash_source(args.source, ignore_hidden)
        print(hash_result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()