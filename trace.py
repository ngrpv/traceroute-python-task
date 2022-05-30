import argparse
import json
import socket

import requests


def get_info(ip) -> (str, str):
    try:
        info = json.loads(
            requests.get(f"https://ipinfo.io/{ip}/json").content)
        # return f'{info.get("org", ""):<30}{info.get("country", ""):<5}'
        return info.get("org", ""), info.get("country", "")
    except Exception:
        return "*****"


class TraceResult:
    def __init__(self, ttl, ip="*****", country="", provider=""):
        self.ttl = ttl
        self.ip = ip
        self.country = country
        self.provider = provider

    def __str__(self):
        return f'{self.ttl:<3}{self.ip:<20}{self.provider:<30}{self.country:<5}'


class Tracer:
    def __init__(self, max_hops: int, destination_ip: str, port: int, timeout_in_ms: int):
        self._max_hops = max_hops
        self._destination = destination_ip
        self._port = port
        self._timeout = timeout_in_ms / 1000

    def start(self):
        # log('tracing: {}'.format(self._destination))
        port = 33434
        try:
            with socket.socket(
                    socket.AF_INET, socket.SOCK_RAW,
                    socket.IPPROTO_ICMP
            ) as receiver:
                receiver.bind(('', port))
                receiver.settimeout(self._timeout)
                yield from self._start_sender(receiver)
        except Exception as e:
            print('Something went wrong: {}'.format(e))

    def _start_sender(self, receiver: socket.socket):
        with socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM,
                socket.getprotobyname('udp')
        ) as sender:
            for ttl in range(1, self._max_hops + 1):
                sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
                sender.sendto(b'1234', (self._destination, self._port))
                answer_from = None
                try:
                    _, answer_from = receiver.recvfrom(65536)
                except socket.error:
                    pass
                if answer_from:
                    ip_info = get_info(answer_from[0])
                    yield TraceResult(ttl, answer_from[0], ip_info[1], ip_info[0])
                #  log('{:<3}{:<20}{:<25}'.format(ttl, answer_from[0], ip_info))
                else:
                    yield TraceResult(ttl)
                    #       log('{}\t *****'.format(ttl))
                    continue
                if answer_from[0] == self._destination:
                    break



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Tracer with detecting country, autonomous system and provider")
    parser.add_argument('-t', '--timeout', help='Timeout for ping (ms)', default=1000, type=int)
    parser.add_argument('-m', '--max-hops', help='Max count of hops', default=30, type=int)
    args = parser.parse_args()
    ip_or_domain = input('ip or domain: ')
    try:
        dest = socket.gethostbyname(ip_or_domain)
    except socket.error:
        #    log(f"Can't resolve ip address for {ip_or_domain}. Check internet connection")
        exit()
    tracer = Tracer(args.max_hops, dest, 33343, args.timeout)
    # trace(ip_or_domain, args.max_hops, args.timeout / 1000)
    for i in tracer.start():
        print(i)
