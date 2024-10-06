# src/flexiai/scripts/cli.py
import argparse
from flexiai import __version__

def main():
    parser = argparse.ArgumentParser(description="FlexiAI CLI")
    parser.add_argument('--version', action='store_true', help='Show the version of FlexiAI')
    args = parser.parse_args()

    if args.version:
        print(f"FlexiAI version: {__version__}")
