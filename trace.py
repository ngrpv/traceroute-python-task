import argparse
import socket
import json
import requests


def get_info(ip):
    try:
        info = json.loads(
            requests.get("http://ipinfo.io/{0}/json".format(ip)).content)
        return '{:<30}{:<5}'.format(info.get('org', ''), info.get('country', ''))
    except Exception:
        return "*****"


def trace(ip, hops, timeout):
    try:
        dest = socket.gethostbyname(ip)
    except socket.error:
        log(f"Can't resolve ip address for {ip}. Check internet connection")
        return
    log('tracing: {}'.format(dest))
    ttl = 0
    port = 33434
    try:
        while ttl < hops:
            ttl += 1
            with socket.socket(socket.AF_INET, socket.SOCK_RAW,
                               socket.IPPROTO_ICMP) as receiver:
                receiver.bind(('', port))
                receiver.settimeout(timeout)
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                   socket.getprotobyname('udp')) as sender:
                    sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
                    sender.sendto(b'1234', (dest, port))
                    answer_from = None
                    try:
                        _, answer_from = receiver.recvfrom(65536)
                    except socket.error:
                        pass
                    if answer_from:
                        as_num = get_info(answer_from[0])
                        log('{:<3}{:<20}{:<25}'.format(ttl, answer_from[0], as_num))
                    else:
                        log('{}\t *****'.format(ttl))
                        continue
                    if answer_from[0] == dest:
                        break
    except Exception as e:
        print('Something went wrong: {}'.format(e))


def log(str):
    print(str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Tracer with detecting country, autonomous system and provider")
    parser.add_argument('-t', '--timeout', help='Timeout for ping (ms)', default=1000, type=int)
    parser.add_argument('-m', '--max-hops', help='Max count of hops', default=30, type=int)
    args = parser.parse_args()
    print('ip or domain:')
    ip = input()
    trace(ip, args.max_hops, args.timeout / 1000)
