#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from lib.core.data import MY_LOGGER, conf
import itertools
import multiprocessing
import string
import time
import progressbar
from gevent import monkey
monkey.patch_all()
from gevent.queue import PriorityQueue
import gevent
import dns.resolver

def more_sub(x=3):
    ret = []
    it = itertools.combinations_with_replacement(string.ascii_lowercase, x)
    for i in it:
        ret.append(''.join(i))
    return ret

def ascii_sub(x=3):
    ret = []
    for i in range(x):
        ret += more_sub(i+1)
    return ret

class subdomain:
    def __init__(self, url, process, level = 3):
        MY_LOGGER.info("domain start")
        with open('dics/domain/domain.txt') as f:
            self.normal_dict = f.readlines()
        self.ascii_dict = ascii_sub(level)
        self.process = process
        self.target = url.strip()
        dns_servers = ['223.5.5.5', '223.6.6.6', '119.29.29.29', '182.254.116.116', '8.8.8.8']
        self.dns_servers = dns_servers
        self.dns_count = len(dns_servers)
        self.correct_sub = {}
        self.resolvers = [dns.resolver.Resolver(configure=False) for _ in range(self.process)]
        for _r in self.resolvers:
            _r.lifetime = _r.timeout = 5.0
            _r.nameservers = dns_servers
        widgets = ['domain_search: ', progressbar.Percentage(), ' ', progressbar.Bar('#'), ' ', progressbar.Timer(),
                   ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
        self.dict = self.normal_dict + self.ascii_dict
        self.len_dict = len(self.dict)
        self.p = progressbar.ProgressBar(maxval=self.len_dict, widgets=widgets).start()
        self.scan_count = 0

    def _scan(self, j):
        self.resolvers[j].nameservers = [self.dns_servers[j % self.dns_count]]
        for sub in self.dict[j::self.process]:
            self.scan_count += 1
            sub = sub.strip()
            if sub in self.correct_sub.keys():
                self.p.update(self.scan_count)
                time.sleep(0.05)
                continue
            subname = sub + "." + self.target
            try:
                answers = self.resolvers[j].query(subname)
                ips = ','.join(sorted([answer.address for answer in answers]))
                if ips in ['1.1.1.1', '127.0.0.1', '0.0.0.0']:
                    self.p.update(self.scan_count)
                    time.sleep(0.05)
                    continue
                self.correct_sub[sub] = ips
                self.p.update(self.scan_count)
                time.sleep(0.05)
            except Exception:
                self.p.update(self.scan_count)
                time.sleep(0.05)


    def run(self):
        threads = [gevent.spawn(self._scan, i) for i in range(self.process)]
        gevent.joinall(threads)
        self.p.finish()

    def get_correct_sub(self):
        return self.correct_sub


if __name__ == '__main__':
    url = "baidu.com"
    conf.process = 5
    multiprocessing.freeze_support()
    all_process = []
    sub = subdomain(url,4)
    sub.run()




