#!/usr/bin/env python3
from pathlib import Path
import argparse

from app.backup_verification import sha256, verify_recovered_zip


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("backup", type=Path)
    args = parser.parse_args()
    manifest = verify_recovered_zip(args.backup)
    print("Backup SHA-256 :", sha256(args.backup))
    print("Posts          :", manifest["counts"]["posts"])
    print("Images         :", manifest["counts"]["user_images"])
    print("Image refs     :", manifest["counts"]["image_references"])
    print("Verification   : OK")


if __name__ == "__main__":
    main()
