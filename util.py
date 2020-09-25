import sys


def err(msg):
    print(f'Error: {msg.lower()}')
    sys.exit(1)


def keyboard_interrupt():
    print('Aborted: keyboard interrupt')
    sys.exit(2)
