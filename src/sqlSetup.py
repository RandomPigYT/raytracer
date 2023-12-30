import os
import sys


def readLoginFromFile(handle):
    lines = handle.readlines()
    print("Hostname:", lines[0][:-1])
    print("User:", lines[1][:-1])
    res = os.system(
        "mysql -h {} -u {} -p < ./sqlSetup.sql".format(lines[0][:-1], lines[1][:-1])
    )
    sys.exit(res)
    



try:
    loginText = open("./loginSave")
    readLoginFromFile(loginText)
except FileNotFoundError:
    loginText = open("./loginSave", "w")

    print("MySQL Login")

    host = input("Hostname: ")
    user = input("User: ")

    res = os.system("mysql -h {} -u {} -p < ./sqlSetup.sql".format(host, user))
    loginText.writelines([host + "\n", user + "\n"])
    loginText.close()

    sys.exit(res)
