#!/usr/bin/env python

import os
import glob
import re
import random

def sort_pool(pool):
    ## Check number of multi-line pool.
    number_of_pool_multi = 0
    for i in range(len(pool)):
        if pool[i] == ('['):
            number_of_pool_multi += 1

    ## Dynamically create multi-line lists.
    multi_list_url = [[] for i in range(number_of_pool_multi)]
    multi_list_comment = [[] for i in range(number_of_pool_multi)]

    ## Sort...
    multi_line = False
    multi_index = 0
    pool_single_url = []
    pool_single_comment = []

    for i in range(len(pool)):
        if multi_line and pool[i] == ']':
            multi_line = False
            multi_index = multi_index + 1

        elif multi_line and pool[i].startswith('"'):
            url = re.search(r'"(.*)#', pool[i])
            if url != None:
                multi_list_url[multi_index].append(url.group(1))
            comment = re.search(r'#(.*)"', pool[i])
            if comment != None:
                multi_list_comment[multi_index].append(comment.group(1))

        elif pool[i] == '[':
            multi_line = True

        elif pool[i].startswith('"'):
            url = re.search(r'"(.*)#', pool[i])
            if url != None:
                pool_single_url.append(url.group(1))
            comment = re.search(r'#(.*)"', pool[i])
            if comment != None:
                pool_single_comment.append(comment.group(1))

    ## Pick a random url in each multi-line pool,
    ## append it to single url pool.
    for i in range(number_of_pool_multi):
        single_ulr_index = random.sample(range(len(multi_list_url[i])), 1)[0]
        single_url = multi_list_url[i][single_ulr_index]
        single_comment = multi_list_comment[i][single_ulr_index]
        pool_single_url.append(single_url)
        pool_single_comment.append(single_comment)

    return(pool_single_url, pool_single_comment)

def read_pools(pool):
    SDWDATE_POOL_ONE = False
    SDWDATE_POOL_TWO = False
    SDWDATE_POOL_THREE = False

    pool_one = []
    pool_two = []
    pool_three = []

    pool_one_url = []
    pool_two_url = []
    pool_three_url = []

    if os.path.exists('/etc/sdwdate.d/'):
        files = sorted(glob.glob('/etc/sdwdate.d/*'))

        if files:
            conf_found = False
            for conf in files:
                if not conf.endswith('~') and conf.count('.dpkg-') == 0:
                    conf_found = True
                    with open(conf) as c:
                        for line in c:
                            line = line.strip()
                            if line.startswith('SDWDATE_POOL_ONE'):
                                SDWDATE_POOL_ONE = True

                            elif line.startswith('SDWDATE_POOL_TWO'):
                                SDWDATE_POOL_ONE = False
                                SDWDATE_POOL_TWO = True

                            elif line.startswith('SDWDATE_POOL_THREE'):
                                SDWDATE_POOL_ONE = False
                                SDWDATE_POOL_TWO = False
                                SDWDATE_POOL_THREE = True

                            elif SDWDATE_POOL_ONE and not line.startswith('##'):
                                pool_one.append(line)

                            elif SDWDATE_POOL_TWO and not line.startswith('##'):
                                pool_two.append(line)

                            elif SDWDATE_POOL_THREE and not line.startswith('##'):
                                pool_three.append(line)

            if not conf_found:
                print('No valid file found in user configuration folder "/etc/sdwdate.d".')

        else:
            print('No file found in user configuration folder "/etc/sdwdate.d".')

    else:
        print('User configuration folder "/etc/sdwdate.d" does not exist.')

    pool_one_url, pool_one_comment = sort_pool(pool_one)
    pool_two_url , pool_two_comment = sort_pool(pool_two)
    pool_three_url, pool_three_comment = sort_pool(pool_three)

    pool_url = [pool_one_url, pool_two_url, pool_three_url]
    pool_comment = [pool_one_comment, pool_two_comment, pool_three_comment]

    return(pool_url[pool],
           pool_comment[pool])


if __name__ == "__main__":
    read_pools()
