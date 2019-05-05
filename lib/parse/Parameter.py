import argparse


def Parameter():
    parser = argparse.ArgumentParser(description="scanner v1.0 ckj123")
    parser.add_argument("-d","--domain",metavar="",
        help="domain name")
    args = parser.parse_args()
    return args