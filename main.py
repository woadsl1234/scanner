import argparse
import logging
import sys
import 


def run(args):
    pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="scanner")
    parser.add_argument("-d","--domain",metavar="",
        help="domain name")
    parser.add_argument("-o","--out",metavar="",default="domains.log",
        help="result out file")
    args = parser.parse_args()

    try:
        run(args)
    except KeyboardInterrupt:
        logging.info("Ctrl C - Stopping Client")
        sys.exit(1)