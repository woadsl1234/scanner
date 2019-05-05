from termcolor import colored
from lib.core.config import *
from tld import get_fld
import time
import json
import requests
import os
from lib.core.data import *

def at_channel(): #control slack @channel
    return("<!channel> " if at_channel_enabled else "")

def slack(data): #posting to Slack
    webhook_url = posting_webhook
    slack_data = {'text': data}
    response = requests.post(
                        webhook_url,
                        data = json.dumps(slack_data),
                        headers = {'Content-Type': 'application/json'}
                            )
    if response.status_code != 200:
        error = "Request to slack returned an error {}, the response is:\n{}".format(response.status_code, response.text)
        logger.error(error)
    if slack_sleep_enabled:
        time.sleep(1)

def posting_to_slack(result, dns_resolve, dns_output): #sending result to slack workplace
    global domain_to_monitor
    global new_subdomains
    if dns_resolve:
        dns_result = dns_output
        if dns_result:
            dns_result = {k:v for k,v in dns_result.items() if v} #filters non-resolving subdomains
            rev_url = []
            print(colored("\n[!] Exporting result to Slack. Please do not interrupt!", "red"))
            for url in dns_result:
                url = url.replace('*.', '')
                url = url.replace('+ ', '')
                rev_url.append(get_fld(url, fix_protocol = True))

            unique_list = list(set(new_subdomains) & set(dns_result.keys())) #filters non-resolving subdomains from new_subdomains list

            for subdomain in unique_list:
                data = "{}:new: {}".format(at_channel(), subdomain)
                slack(data)
                try:
                    if dns_result[subdomain]["A"]:
                        for i in dns_result[subdomain]["A"]:
                            data = "```A : {}```".format(i)
                            slack(data)
                except: pass
                try:
                    if dns_result[subdomain]['CNAME']:
                        for i in dns_result[subdomain]['CNAME']:
                            data = "```CNAME : {}```".format(i)
                            slack(data)
                except: pass
            print(colored("\n[!] Done. ", "green"))
            rev_url = list(set(rev_url))
            for url in rev_url:
                os.system("rm -f ./output/" + url.lower() + ".txt")
                os.system("mv -f ./output/" + url.lower() + "_tmp.txt " + "./output/" + url.lower() + ".txt") #save the temporary one
            os.system("rm -f ./output/*_tmp.txt") #remove the remaining tmp files

    elif result:
        rev_url = []
        print(colored("\n[!] Exporting the result to Slack. Please don't interrupt!", "red"))
        for url in result:
            url = "https://" + url.replace('+ ', '')
            rev_url.append(get_fld(url))
            data = "{}:new: {}".format(at_channel(), url)
            slack(data)
        print(colored("\n[!] Done. ", "green"))
        rev_url = list(set(rev_url))

        for url in rev_url:
            os.system("rm -f ./output/" + url.lower() + ".txt")
            os.system("mv -f ./output/" + url.lower() + "_tmp.txt " + "./output/" + url.lower() + ".txt") #save the temporary one
        os.system("rm -f ./output/*_tmp.txt") #remove the remaining tmp files

    else:
        if not domain_to_monitor:
            data = "{}:-1: We couldn't find any new valid subdomains.".format(at_channel())
            slack(data)
            print(colored("\n[!] Done. ", "green"))
            os.system("rm -f ./output/*_tmp.txt")
        else: pass