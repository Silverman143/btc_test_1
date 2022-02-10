import csv
from pandas import *
import sqlite3
from sqlite3 import Error





def main():
    data = read_csv("btc_balance_sorted.csv")
    wallets = data['address'].tolist()



    w = 0
    counter = 0

    while w < 4689029:
        if (wallets[w][0] == '1'):
            counter +=1
            print(wallets[w])

        w+=1
        print(counter, end = "\r")




if __name__ == '__main__':
    main()
