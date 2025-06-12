from tofuzz.models.fuzzed_request import fuzzed_request
from pytest_httpserver import HTTPServer
import pytest

@pytest.fixture(scope="session")
def httpserver_listen_address():
    return ("localhost", 8888)


METHOD = "POST"
URL = "localhost?paramA=FUZZ&paramB=stay"
HEADERS = {"Content-Type":"application/json"}
BODY = {"user":"toto", "password":"FUZZ12345"}


def test_request_initialization():
    url = "http://example.com"
    req = fuzzed_request("GET",url)
    assert req.url == url
    assert req.method == "GET"

def test_fuzz_body() : 
    req = fuzzed_request(METHOD,URL, headers=HEADERS, body=BODY)
    req.fuzz_body("$$$$$$")
    assert "$$$$$$" in req.body["password"] 
    assert "$$$$$$" not in req.url

def test_fuzz_query() : 
    req = fuzzed_request(METHOD,URL, headers=HEADERS, body=BODY)
    req.fuzz_query("$payload1$")
    print(req)

    assert "$payload1$" not in req.body["password"] 
    assert "$payload1$" in req.url


def test_execute(httpserver: HTTPServer):
    httpserver.expect_request("/").respond_with_json({"foo": "bar"})
    req = fuzzed_request("GET",httpserver.url_for("/"))
    assert req.execute().json() == {"foo": "bar"}