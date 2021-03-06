import sys
import sqlite3
import tgBot
from sqlite3 import Error
from bit import Key
from time import time
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

with open('wallets.txt', 'r') as file:
    wallets = file.read()

max_p = 115792089237316195423570985008687907852837564279074904382605163141518161494336
sep_p = round(max_p / cpu_count())

# random bruteforce
'''
Will randomly generate addresses
'''



def RBF(r):
    print(f'Instance: {r + 1} - Generating random addresses...')

    startTime = time()

    i = 0


    while True:
        pk = Key()

        i+=1;
        if (time()- startTime >= 60):
            ts = f'Instance: {r + 1} - Generating addresses...  speed = {i/60} s'
            print(ts)
            
            i = 0;
            startTime = time()




        if pk.address in wallets:
            print(f'Instance: {r + 1} - Found: {pk.address}')
            with open('found.txt', 'a') as result:
                result.write(f'{pk.to_wif()}')


# traditional bruteforce (slowest)
'''
Will try every INT from 0 to max possible
'''


def TBF(r):
    sint = sep_p * r
    mint = sep_p * (r + 1)
    start = time()
    print(f'Instance: {r + 1} - Generating addresses...')
    while sint < mint:
        try:
            pk = Key.from_int(sint)
            print(pk.to_wif())
            if pk.address in wallets:
                print(f'Instance: {r + 1} - Found: {pk.address}')
                with open('found.txt', 'a') as result:
                    result.write(f'{pk.to_wif()}\n')
        except ValueError:
            pass
        sint += 1
    print(f'Instance: {r + 1}  - Done after %s' % (time() - start))


# optimized traditional bruteforce
'''
Will try every INT between 10**75 and max possibility.
This methode is based on the best practice to get the safest address possible.
'''


def OTBF(r):
    sint = (sep_p * r) + 10 ** 75 if r == 0 else (sep_p * r)
    mint = (sep_p * (r + 1))

    data = f'Instance: {r + 1} - Generating addresses... '
    print(data)
    startTime = time()

    i = 0


    while sint < mint:
        try:
            pk = Key.from_int(sint)
            i+=1;
            if (time()- startTime >= 10):
                ts = f'Instance: {r + 1} - Generating addresses...  speed = {i/10} s'
                print(ts)
                i = 0;
                startTime = time()

            # if data is None:
            #     print('There is no component named %s'%name)
            # else:
            #     print(f'Instance: {r + 1} - Found: {pk.address}')
            #     with open('found.txt', 'a') as result:
            #         result.write(f'{pk.to_wif()}\n')

            if pk.address in wallets:
                print(f'Instance: {r + 1} - Found: {pk.address}')
                with open('found.txt', 'a') as result:
                    result.write(f'{pk.to_wif()}\n')
        except ValueError:
            pass
        sint += 1


def main():
    # set bruteforce mode
    mode = [None, RBF, TBF, OTBF]

    global walletsCounter
    walletsCounter = 0

    try:
        print('Select bruteforce mode:\n0 - Exit\n1 - RBF\n2 - TBF\n3 - OTBF')
        choice = int(input('> '))
        print(f'How many cores do you want to use ({cpu_count()} available)')
        cpu_cores = int(input('> '))
        cpu_cores = cpu_cores if 0 < cpu_cores < cpu_count() else cpu_count()
        option = choice if 0 < choice <= len(mode) - 1 else 0
    except ValueError:
        option = 0
        cpu_cores = 0

    if mode[option]:
        print(f'Starting bruteforce instances in mode: {mode[option].__name__} with {cpu_cores} core(s)\n')

        with ProcessPoolExecutor() as executor:
            executor.map(mode[option], range(cpu_cores))

    print('Stopping...')


if __name__ == '__main__':
    main()
