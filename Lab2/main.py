import socket
import click
from pythonping import ping

def check(host, count, interval, timeout, payload):
    res = ping(
            host,
            count=count,
            interval=interval,
            timeout=timeout,
            size=payload - 28,
            df=True,
        )
    return res.success()

def hostname_resolves(hostname):
    try:
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0

@click.command()
@click.argument('host', type=str, required=True)
@click.option('--count', '-c', type=click.IntRange(min=1), default=3, help='Ping count')
@click.option('--timeout', '-W', type=click.FloatRange(min=0), default=1, help='Ping timeout (in seconds)')
@click.option('--interval', '-i', type=click.FloatRange(min=0), default=0.1, help='Ping interval (in seconds)')
def main(host, count, interval, timeout):
    if not hostname_resolves(host):
        print(f'Hostname {host} is unknown')
        exit(1)

    l = 28
    r = 5000
    while r - l > 1:
        tm = (l + r) // 2
        print(f'Checking {host} with payload of {tm} bytes...')
        try:
            if check(host, count, timeout, interval, tm):
                l = tm
            else:
                r = tm
        except Exception as e:
            print('Encountered error: ')
            print(e)
            exit(1)

    if l == 28:
        print(f'Host {host} unreachable')
    else:
        print(f'Maximum transmission unit is {l} bytes')


if __name__ == '__main__':
    main()