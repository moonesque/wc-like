import sys
import re
import os


class Argparse:
    available_options = ['-l', '-w', '-c', '-b', '-h']
    def __init__(self, arg_list):
        self.filename_list = []
        self.option_list = []
        self.valid_options = []
        self.invalid_options = []
        for arg in arg_list[1:]:
            if arg.startswith('-'):
                self.option_list.append(arg)
            else:
                self.filename_list.append(arg)
        for option in self.option_list:
            if option in self.available_options:
                self.valid_options.append(option)
            else:
                self.invalid_options.append(option)
        if self.invalid_options:
            print("invalid option:")
            for i in self.invalid_options:
                print(i)
            print("Try -h for more information")
            sys.exit(1)
        if '-h' in self.valid_options:
            print('''Simple word count program.displays the count of: newline, word, character, byte in that order for each file given.
When no file given reads standard input.
The following options are on by default.You may use each to only get that count.
-l  display newline count
-w  display word count
-c  display character count
-b  display byte count

-h display this help text''')
            sys.exit(0)
        self.newline_count = False
        self.word_count = False
        self.character_count = False
        self.byte_count = False
        if '-l' in self.valid_options:
            self.newline_count = True
        if '-w' in self.valid_options:
            self.word_count = True
        if '-c' in self.valid_options:
            self.character_count = True
        if '-b' in self.valid_options:
            self.byte_count = True


def wc(argparse):
    if argparse.filename_list:
        total_nc = 0
        total_cc = 0
        total_bc = 0
        total_wc = 0
        for i in argparse.filename_list:
            try:
                file = open(i, "r")
                nc, cc, bc, wc = do_wc(file, argparse, i)
                file.close()
                total_nc += nc
                total_cc += cc
                total_bc += bc
                total_wc += wc
            except FileNotFoundError:
                print('No such file as "', i, '"')
        if len(argparse.filename_list) > 1:
            print(' ', total_nc, '  ', total_wc, '  ', total_cc,'  ', total_bc,'  ', 'total') 
    else:
        while True:
            try:
                if os.isatty(0):
                    file = input()
                    do_wc(file, argparse, '')
                else:
                    file = sys.stdin.read()
                    do_wc(file, argparse, '')
                    sys.exit(0)
            except KeyboardInterrupt:
                print('')
                sys.exit(1)



def do_wc(file, arg, i):
    if arg.filename_list:
        content = file.read()
    else:
        content = file
    newline_count = 0
    character_count = 0
    byte_count = 0
    word_count = 0
    #word_re = re.compile('\S+')
    #word_count =len(word_re.findall(content))
    character_count = len(content.encode('utf-8'))
    for k in content:
        if k == '\n':
            newline_count += 1
    state = 'ws'
    for k in content:
        if k in [' ', '\n', '\t']:
            state = 'ws'
            continue
        elif state == 'ws':
            word_count += 1
            state = 'word'
        
    byte_count = character_count
    if arg.newline_count == True or not arg.valid_options:
        sys.stdout.write('  ')
        sys.stdout.write(str(newline_count))
        sys.stdout.write('  ')
    if arg.word_count == True or not arg.valid_options:
        sys.stdout.write('  ')
        sys.stdout.write(str(word_count))
        sys.stdout.write('  ')
    if arg.character_count == True or not arg.valid_options:
        sys.stdout.write('  ')
        sys.stdout.write(str(character_count))
        sys.stdout.write('  ')
    if arg.byte_count == True or not arg.valid_options:
        sys.stdout.write('  ')
        sys.stdout.write(str(byte_count))
        sys.stdout.write('  ')
    sys.stdout.write('  ')
    sys.stdout.write(i)
    print('')
    return newline_count, character_count, byte_count, word_count


def main():
    arg = Argparse(sys.argv)
    wc(arg)
main()
