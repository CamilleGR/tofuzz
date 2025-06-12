import pytest
from tofuzz.utils.wordlist import load_wordlist

def test_load_wordlist():
    wl = load_wordlist("resources/test_wordlist.txt")
    print(wl)
    assert len(wl) is 1
    assert len(wl[0]) is not 0
    assert "AAAAA" in wl[0][0]

def test_splitted2_load_wordlist():
    wl = load_wordlist("resources/test_wordlist.txt",2)
    print(wl)
    assert len(wl) is 2
    assert len(wl[0]) is not 0
    assert "AAAAA" in wl[0][0]

def test_splitted3_load_wordlist():
    wl = load_wordlist("resources/test_wordlist.txt",3)
    print(wl)
    assert len(wl) is 3
    assert len(wl[0]) is not 0
    assert "AAAAA" in wl[0][0]
    assert "AAAAAAAAAA" in wl[1][0]
    assert "AAAAAAAAAAAAAAA" in wl[2][0]

def test_splitted_limit_load_wordlist():
    wl = load_wordlist("resources/test_wordlist.txt",20)
    print(wl)
    assert len(wl) is 15
    assert len(wl[0]) is not 0
    assert "A" in wl[0][0]
    assert "B" in wl[1][0]
    assert "C" in wl[2][0]


def test_splitted_limit_load_wordlist():
    wl = load_wordlist("resources/test_wordlist.txt",10)
    print(wl)
    assert len(wl) is 10
    sum = 0
    for w in wl : 
        sum+= len(w)
    assert sum is 15