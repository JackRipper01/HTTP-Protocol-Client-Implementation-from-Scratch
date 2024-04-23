class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_linebold(*text):
    print(bcolors.BOLD,end='')
    print(*text)
    print(bcolors.ENDC,end='')

def print_header(*text):
    print(bcolors.BOLD,end='')
    print(bcolors.UNDERLINE,end='')
    print(bcolors.HEADER,end='')
    print(*text)
    print(bcolors.ENDC,end='')

def print_success(*text):
    print(bcolors.OKCYAN,end='')
    print(bcolors.UNDERLINE,end='')
    print(*text)
    print(bcolors.ENDC,end='')

def print_warning(*text):
    print(bcolors.WARNING,end='')
    print(bcolors.UNDERLINE,end='')
    print(*text)
    print(bcolors.ENDC,end='')

def print_error(*text):
    print(bcolors.FAIL,end='')
    print(bcolors.UNDERLINE,end='')
    print(*text)
    print(bcolors.ENDC,end='')

def print_OK_200(*text):
    print(bcolors.OKGREEN,end='')
    print(*text)
    print(bcolors.ENDC,end='')
    
def print_warn_300(*text):
    print(bcolors.WARNING,end='')
    print(*text)
    print(bcolors.ENDC,end='')

def print_fail_400(*text):
    print(bcolors.FAIL,end='')
    print(*text)
    print(bcolors.ENDC,end='')


if __name__ == '__main__':
    print(bcolors.UNDERLINE + bcolors.BOLD + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
    print("ASD")