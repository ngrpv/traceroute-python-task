from app import app as server
from time import sleep


def test_index_returns_html():
    response = server.test_client().get("/")
    assert b'<!doctype html>' in response.data
    assert response.status_code == 200


def test_trace_returns_id():
    response = server.test_client().get('/trace',
                                        query_string=dict(target='google.com',
                                                          max_ttl=30,
                                                          timeout=1000))
    assert all(char.isdigit() for char in response.data.decode())
    assert response.status_code == 200


def test_trace_returns_bad_request_if_invalid_target():
    response = server.test_client().get('/trace',
                                        query_string=dict(target='m.m',
                                                          max_ttl=30,
                                                          timeout=1000))
    assert response.status_code == 400


def test_get_state_returns_tracing_data_by_id():
    client = server.test_client()
    id = client.get('/trace',
                    query_string=dict(
                        target='google.com',
                        max_ttl=30,
                        timeout=1000)).data
    response = client.get(f"/get-state/{id.decode()}")
    assert response.status_code == 200
    assert b'is_finished' and b'call_arguments' and b'nodes' in response.data


def test_get_state_returns_ip_info():
    client = server.test_client()
    id = client.get('/trace',
                    query_string=dict(
                        target='google.com',
                        max_ttl=30,
                        timeout=1000)).data
    sleep(1)
    response = client.get(f'/get-state/{id.decode()}')

    assert response.status_code == 200
    print(response.data.decode())
