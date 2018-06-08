#!/usr/bin/env python

"""Check your CMS document against PubComm guidelines."""


import os
import sys
import argparse


def main(in_args=sys.argv):
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(in_args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
