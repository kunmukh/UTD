# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 3/7/21
# File name: 
# Project name:

def main ():
    # 2a.
    check_keys_per_sec = 2 ** 32

    key_len1 = 56
    key_len2 = 64
    key_len3 = 80

    # total possible keys
    total_key1 = 2 ** key_len1
    total_key2 = 2 ** key_len2
    total_key3 = 2 ** key_len3

    # amount of time taken
    find_key1_time_taken_sec = total_key1 / check_keys_per_sec
    find_key2_time_taken_sec = total_key2 / check_keys_per_sec
    find_key3_time_taken_sec = total_key3 / check_keys_per_sec

    # convert sec to year
    find_key1_time_taken_year = find_key1_time_taken_sec / (60 * 60 * 24 * 365)
    find_key2_time_taken_year = find_key2_time_taken_sec / (60 * 60 * 24 * 365)
    find_key3_time_taken_year = find_key3_time_taken_sec / (60 * 60 * 24 * 365)

    print("2a: {}:{} {}:{} {}:{}".format(key_len1, find_key1_time_taken_year,
                                         key_len2, find_key2_time_taken_year,
                                         key_len3, find_key3_time_taken_year))

    # 2b
    key_len = 128
    total_key = 2 ** key_len

    # amount of time taken
    find_key_time_taken_sec = total_key / check_keys_per_sec

    # convert sec to year
    find_key_time_taken_year = find_key_time_taken_sec / (60 * 60 * 24 * 365)

    # convert year to universe
    find_key_time_taken_universe = find_key_time_taken_year / 13700000000

    print("2b: {}:{}".format(key_len, find_key_time_taken_universe))


if __name__ == '__main__':
    main()