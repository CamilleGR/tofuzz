from tofuzz.models.fuzzed_request import fuzzed_request 
import threading, time
import sys, os
import argparse
from urllib.parse import urlparse
from tofuzz.utils.wordlist import load_wordlist, normalize_payload
from tofuzz.utils.cli_util import banner, print_details, is_fuzzable, parse_args


# Display request result
def fuzz_res(p, res, verbose=False) : 
    if verbose:
        print(f"{"#"*50}")
        print(f"{res.request.method} {res.request.url}")
        print(f"{res.request.headers}")
        print(f"{res.request.body}")
        print(f"{"#"*50}{os.linesep}")
        print(f"HTTP {res.status_code}")
        print(f"{res.text}")
        print(f"{"#"*50}{os.linesep}")
    return f"PAYLOAD={normalize_payload(p,25)} |\tHTTP {res.status_code} |\tlen = {len(res.text)}"


# Thread main : fuzz 
def fuzz(method, url, headers, body, wordlist, fuzz_body=False, fuzz_query=False, torConfig=None, fuzzToken=""):
    for w in wordlist : 
        req = fuzzed_request(method,url, headers=headers, body=body, FUZZ_TOKEN =fuzzToken, torConfig=torConfig)
        if fuzz_body : 
            req.fuzz_body(w) 
        if fuzz_query : 
            req.fuzz_query(w)
        print(fuzz_res(w, req.execute(), False))

def cli() : 
    # Parsing args
    print(banner())
    args = parse_args()

    # Common treatment and init
    
    wordlist = load_wordlist(args.wordlist.name,args.threads)
    FUZZ_QUERY = is_fuzzable(args.url , args.fuzzToken )
    FUZZ_BODY  = is_fuzzable(args.body , args.fuzzToken ) 
    print_details(args.method ,args.url ,args.wordlist , sum([len(w) for w in wordlist]), FUZZ_QUERY, FUZZ_BODY )
    torConfig = {"adress":args.torHost,"socks_port":args.torPort} if args.tor else None 


    threads = []


    for w in wordlist : 
        # Creating threads
        t = threading.Thread(target=fuzz, 
        args=(args.method ,args.url ,args.headers ,args.body ,), 
        kwargs={"wordlist":w,
        "fuzz_body": FUZZ_BODY , 
        "fuzz_query":FUZZ_QUERY,
        "torConfig": torConfig,
        "fuzzToken": args.fuzzToken
        })
        threads.append(t)

    start = time.time()
    for t in threads:
        t.start()

    for t in threads:
        t.join()


    end = time.time()
    print(f"{os.linesep*2}")
    print(f"Terminated with success")
    print(f"Execution time : {end - start:.2f} seconds")

if __name__ == '__main__':
    cli()