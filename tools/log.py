import os
from datetime import datetime

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), './log')


def log(log_type, message):
    time = datetime.now()
    out = '{} -- {}: {}\n'.format(time, log_type, message)

    with open(LOG_FILE_PATH, 'a') as f:
        f.write(out)


def last():
    with open(LOG_FILE_PATH, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode()
        print(last_line)


def tail(count=5):
    with open(LOG_FILE_PATH, 'r') as f:
        total_lines_wanted = count

        BLOCK_SIZE = 1024
        f.seek(0, 2)
        block_end_byte = f.tell()
        lines_to_go = total_lines_wanted
        block_number = -1
        blocks = []  # blocks of size BLOCK_SIZE, in reverse order starting
        # from the end of the file
        while lines_to_go > 0 and block_end_byte > 0:
            if (block_end_byte - BLOCK_SIZE > 0):
                # read the last block we haven't yet read
                f.seek(block_number*BLOCK_SIZE, 2)
                blocks.append(f.read(BLOCK_SIZE))
            else:
                # file too small, start from begining
                f.seek(0, 0)
                # only read what was not read
                blocks.append(f.read(block_end_byte))
            lines_found = blocks[-1].count('\n')
            lines_to_go -= lines_found
            block_end_byte -= BLOCK_SIZE
            block_number -= 1
        all_read_text = ''.join(reversed(blocks))
        for line in all_read_text.splitlines()[-total_lines_wanted:]:
            print(line)
