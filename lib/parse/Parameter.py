import argparse


def Parameter():
    parser = argparse.ArgumentParser(description="scanner v1.0 ckj123")
    parser.add_argument("-d","--domain",metavar="ckj123.com",
        help="domain name")
    parser.add_argument("-u","--url",metavar="",help="url name")
    args = parser.parse_args()
    return args