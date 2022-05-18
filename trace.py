import socket


def trace(ip, hops):
    try:
        dest = socket.gethostbyname(ip)
    except socket.error:
        log("Can't resolve ip address for {}. Check internet connection".format(
            ip))
        return
    log('tracing: {}'.format(dest))
    ttl = 0
    port = 33434
    try:
        while ttl < hops:
            ttl += 1
            receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                     socket.IPPROTO_ICMP)
            receiver.bind(('', port))
            receiver.settimeout(2)
            sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                   socket.getprotobyname('udp'))
            sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            sender.sendto(b'1234', (dest, port))
            answer_from = None
            try:
                _, answer_from = receiver.recvfrom(65536)
            except socket.error:
                pass
            finally:
                receiver.close()
                sender.close()
            if answer_from:
                #  as_num = get_info(answer_from[0])
                log('{:<3}{:<20}'.format(ttl, answer_from[0]))
            else:
                log('{}\t *****'.format(ttl))
                continue
            if answer_from[0] == dest:
                break
    except Exception as e:
        print('Something went wrong: {}'.format(e))


def log(str):
    print(str)


print('ip or domain:')
ip = input()
trace(ip, 30)
