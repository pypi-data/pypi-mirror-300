def chopet(message):
    print(message)

def qosh(x, y):
    return x + y

def ayir(x, y):
    return x - y

def kopayt(x, y):
    return x * y

def bol(x, y):
    return x / y

def max_qiymat(x):
    return max(x)

def min_qiymat(x):
    return min(x)

def uzun(x):
    return len(x)

def format_raqam(x):
    return f"{x:.2f}"

def matnga_otkaz(x):
    return str(x)

def butun_qiymat(x):
    return int(x)

def haqiqiy_qiymat(x):
    return float(x)

def kvadrat(x):
    return x ** 2

def kub(x):
    return x ** 3

def ildiz_ol(x):
    from math import sqrt
    return sqrt(x)

def qoldiq(x, y):
    return x % y

def ulush_ol(x, y):
    return x // y

def tartibla(x):
    return sorted(x)

def avvalgi_qismini_ol(x):
    return x[1:]

def oxirgi_qismini_ol(x):
    return x[:-1]

def listdan_qidir(x, y):
    return x.find(y)

def mavjudmi(x, y):
    return y in x

def havola_parsela(x):
    import urllib.parse
    return urllib.parse.urlparse(x)

def fayl_oqish(x):
    with open(x, 'r') as file:
        return file.read()
    
def TxtYaratish(txtnomi):
    try:
        with open(txtnomi + '.txt', 'w') as f:
            f.write('')
        print(f"{txtnomi}.txt fayli muvaffaqiyatli yaratildi.")
    except Exception as e:
        print(f"Xato yuz berdi: {e}")    

def fayl_yozish_EskiMalumotlarniOchishib(x, data):
    with open(x, 'w') as file:
        file.write(data)

def fayl_yozish_EskiMalumotlarniSaqlab(x, data):
    with open(x, 'a') as file:
        file.write(data)     

def fayl_qatorlar_ol(x):
    with open(x, 'r') as file:
        return file.readlines()

def vaqt_ol():
    from datetime import datetime
    return datetime.now()

def vaqt_formatlash(x):
    from datetime import datetime
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def ipni_top(x):
    import socket
    return socket.gethostbyname(x)

def formatla(x, y):
    return f"{x:{y}}"
