#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from lib.core.data import MY_LOGGER, conf
import itertools
import multiprocessing
import string
import dns.resolver

def more_sub(x=3):
    it = itertools.combinations_with_replacement(string.ascii_lowercase, x)
    return it


def subdomain(url,dict):
    target = url.strip()
    correct_sub = {}
    resolver = dns.resolver.Resolver(configure=False)
    resolver.timeout = 5.0
    nameserver = ['223.5.5.5','223.6.6.6','119.29.29.29','182.254.116.116','8.8.8.8']
    resolver.nameservers = nameserver
    MY_LOGGER.info("domain start")
    for sub in dict:
        sub = sub.strip()
        if sub in correct_sub.keys():
            continue
        subname = sub+"."+target
        try:
            result = resolver.query(subname)
            correct_sub[sub] = result
        except Exception:
            pass

    MY_LOGGER.info("domain success")

    print(correct_sub)
if __name__ == '__main__':
    url = "baidu.com"
    with open('../../dics/domain/domain.txt') as f:
        domain = f.readlines()
    conf.process = 5
    multiprocessing.freeze_support()
    all_process = []
    for process_num in range(conf.process):
        p = multiprocessing.Process(target=subdomain,args=(url,domain))
        all_process.append(p)
        p.start()



