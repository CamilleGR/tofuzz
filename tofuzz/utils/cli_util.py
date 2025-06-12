import os, argparse


def banner() : 
    return r"""    
___________     _____                     
\__    ___/____/ ____\_ __________________
  |    | /  _ \   __\  |  \___   /\___   /
  |    |(  <_> )  | |  |  //    /  /    / 
  |____| \____/|__| |____//_____ \/_____ \
                                \/      \/"""

def print_details(method,url, wordlist,nbword, fq, fb, body=None): 
    print(os.linesep)
    print(f"METHOD    : {method}")
    print(f"URL       : {url}")
    print(f"WORDLIST  : {wordlist.name} ({nbword})")
    print(f"FUZZ URL  : {fq}")
    print(f"FUZZ BODY : {fb}")
    if body : 
        print(f"{os.linesep*3}{body}")
    print("-"*50)

def parse_args():
    parser = argparse.ArgumentParser(prog='ToFuzz', description='ToFuzz – Tor-enabled HTTP fuzzer.')

    parser.add_argument('-X', '--method', default='GET', help='HTTP method to use (default: GET)')
    parser.add_argument('-u', '--url', required=True, help='Target URL with FUZZ token')
    parser.add_argument('-H','--headers', type=str, help='HTTP headers as JSON string')
    parser.add_argument('-b','--body', type=str, help='HTTP body as raw string or JSON string')
    parser.add_argument('-w', '--wordlist', type=argparse.FileType('r'), required=True, help='Path to wordlist file')
    parser.add_argument('--fuzzToken', default='FUZZ', help='Token to replace in URL/body (default: FUZZ)')
    parser.add_argument("-t",'--threads', type=int, default=1, help='Number of threads')
    parser.add_argument("-v",'--verbose', action="store_true", default=False, help='Verbose Mode')
    parser.add_argument("-T",'--tor', action="store_true", default=False, help='Use Tor network')
    parser.add_argument('--torHost', default='127.0.0.1', help='Tor SOCKS5 proxy host (default: 127.0.0.1)')
    parser.add_argument('--torPort', type=int, default=9050, help='Tor SOCKS5 proxy port (default: 9050)')

    return parser.parse_args()

def is_fuzzable(x, token) :
    is_fuzzable=False  
    if type(x) is dict : 
        for k,v in x.items() : 
            if token in k or token in v : 
                return True
    elif type(x) is str : 
        return token in x 

    return False
