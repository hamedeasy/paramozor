#!/usr/bin/python3

# Name:         Paramozor
# Purpose:      ???
# Author:       Hamed izadi - hamedizadi@gmail.com
# Created:      ???
# Copyright:    (c) 2017 hamedizadi
# Licence:      Free to use, Only for research and do not use it for illegal purposes!
# Version:      1.0


from collections import OrderedDict
from urllib.parse import urlparse
from collections import Counter
from string import whitespace
from random import sample
import requests.exceptions
import requests
import argparse
import operator
import sys
import time

def main():
    parser = argparse.ArgumentParser(description='Paramozor.py - ???. by Hamed Izadi @hezd')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-u', '--url', help='Target URL (http://www.example.com/page.php?parameter=value)', required=True)
    parser.add_argument('-a', '--useragent', help='Set custom user-agent string')
    parser.add_argument('-d', '--delay', help='Set delay between requests (secends)', type=float)
    # parser.add_argument('-r', '--randip', action='store_true', help='Random IP for X-Forwarded-For')
    parser.add_argument('-x', '--proxy', help='Set proxy (https://IP:PORT)')
    parser.add_argument('-p', '--post', help='Data string to be sent through POST (parameter=value&also=another)')
    parser.add_argument('-c', '--cookie', help='HTTP Cookie header')
    # parser.add_argument('-t', '--type', help='Type of char [sqli | xss | others]', choices=['sql','xss','others','all'], default='all')
    if len(sys.argv)==1: parser.print_help(); sys.exit(0)
    args = parser.parse_args()


    bla = """


                                                                           
              _ __   __ _ _ __ __ _ _ __ ___   ___ _______  _ __ 
             | '_ \ / _` | '__/ _` | '_ ` _ \ / _ \_  / _ \| '__|
             | |_) | (_| | | | (_| | | | | | | (_) / / (_) | |   
             | .__/ \__,_|_|  \__,_|_| |_| |_|\___/___\___/|_|   
             |_|                                                             


        Paramozor - ???.
        Copyright (c) 2017 Hamed Izadi (@hezd). 

        


    """
    print (bla)

    url = args.url
    print ("    Result for  URL: ", url, "\r\n")
    base_url = "bla"
    param_list = {}
    proxies = {}
    des = 0
    headers = {}


    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


    if (len(url) - (len(domain) - 1)) == 0:
        url = domain
 
    #Proxy
    if args.proxy:
        if "https" in args.proxy[:5]:
            proxies['https'] = args.proxy
        elif "http" in args.proxy[:4]:
            proxies['http'] = args.proxy
        else:
            print ("\r\n\tSomething wrong with proxy, please Check Paramozor usage!!!\r\n")
            sys.exit()
    #Proxy

    #Headers
    if args.useragent:
        headers['user-agent'] = args.useragent
    else:
        headers['user-agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    # if args.randip:
    #     headers['X-Forwarded-For'] = randomIP()
    if args.cookie:
        headers['cookie'] = args.cookie
    #Headers

    #upordown
    try:
        r = requests.get(domain, proxies=proxies, headers=headers, allow_redirects=False, timeout=20)
        r.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print ("\r\nTarget appears to be down!!\r\n")
        sys.exit()
    #upordown




    if not args.post:
        if "?" in url:
            des = 1
            urls = url.split("&")
            c = len(urls)
            part_1 = urls[0].split("?")
            base_url = part_1[0]
            del urls[0]
        else:
            urls = url.split("/")
            base_url = domain
            del urls[0:3]


    if args.post:
        paramp = args.post.split("&")


    def parameters_equal (arg):
        s_arg=arg.split("=")
        param_list[s_arg[0]] = s_arg[1]
        return;

    def parameters_slash (arg,param_count):
        param_list["param_"+str(param_count)] = arg
        return;



    if not args.post:
        if des == 1:
            parameters_equal(part_1[1])
            for url in urls:
                parameters_equal(url)
        else:
            param_count = 1
            for url in urls:
                parameters_slash(url, param_count)
                param_count = param_count + 1


    if args.post:
        for param in paramp:
            parameters_equal(param)


    chars = {}
    def file2dic (filename):
        f = open(filename, 'r')
        for line in f:
            param_split = line.rpartition('X')
            chars[param_split[0]] = param_split[2]

            
    file2dic ('chars/allcharacters.csv')
    param_list = OrderedDict(sorted(param_list.items()))


    for name_m, value_m in param_list.items():



        print ("\r\n                 ※※※   Parameter Name \"" , name_m , "\"   ※※※\r\n")
        print ("           characters |  mirrored | status code | description\r")
        print ("         -------------+-----------+-------------+--------------\r")

        params = {}
        rs = []
        q = ""
        c = 0
        values_s_M = {}
        trycount = 0

        for char, string in chars.items():
            c = c + 1

            if args.delay:
                time.sleep(args.delay)

            name_m = str(name_m)
            value_m = str(value_m)
            param_list[name_m] = value_m + char + char

            charx = value_m + char + char
            #Send-Request
            for i in range(3):
                try:
                    if args.post:
                        req = requests.post(url, data=param_list, headers=headers, proxies=proxies, allow_redirects=False, timeout=10)
                    else:
                        if des == 1:
                            req = requests.get(base_url, params=param_list, headers=headers, proxies=proxies, allow_redirects=False, timeout=10)
                        else:
                            base_url = domain
                            base_url = base_url + '/'.join(param_list.values())
                            req = requests.get(base_url, headers=headers, proxies=proxies, allow_redirects=False, timeout=10)
                            base_url = domain




                    r.raise_for_status()



                    values_s = []
                    if value_m in req.text:
                        values_text = req.text.split(value_m)
                        values_text.pop(0)

                        for x in values_text:
                            values_s.append(value_m + x[0:14])

                    values_s_M[char] = '  ███  '.join(values_s).strip()




                    if (charx in req.text):
                        string = string[:-1]
                        print ("               {}      |     OK    |     {}     | {}".format(char, str(req.status_code), string.strip()))
                    else:
                        print ("               {}      |     --    |     {}     | {}".format(char, str(req.status_code), string.strip()))

        

                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                    print (" Retrying ... [ ", char, " ]")
                    trycount = trycount + 1
                    continue
                else:
                    break    
            else:
                print (" Skipping ... [ ", char, " ]")
                continue

        
            #Send-Request
            param_list[name_m] = value_m




        name_m = str(name_m)
        value_m = str(value_m)

        
        param_list[name_m] = value_m + char + char



        #Summary
        for k, v in values_s_M.items():
            if v:
                print ('\r\n-----------------------------+ Result for [', k ,'] +-----------------------------\r\n')
                print (v.replace('\n', ' ').replace('\r', '').replace(' ', ''),'\r\n', end="")
        print ("  ")
        #Summary





if __name__ == '__main__':
    main()
