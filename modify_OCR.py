from jamo import h2j, j2hcj
from similarity import get_similarity


def modify_lv(bad_num):
    bad_lst = list(bad_num)
    new_lst = []
    for i in range(len(bad_lst)):
        c = bad_lst[i]
        if c == '.' or c == ',':
            continue
        if c == 'n':
            c = '0'
        elif c == '?':
            c = '2'
        elif (c == 'R') or (c == 'F'):
            c = '6'
        elif c == 'E':
            c = '5'
        elif c == 'ø':
            c = '0'
        if c.isdecimal():
            new_lst.append(c)
    return int(''.join(new_lst))


def modify_weekly_pnt(bad_num):
    bad_lst = list(bad_num)
    new_lst = []
    for i in range(len(bad_lst)):
        c = bad_lst[i]
        if c == '.' or c == ',':
            continue
        if c in ('ø', '[', '(', '!', 'I', 'l'):
            c = '0'
        elif c == '?':
            c = '2'
        elif c == 'R':
            c = '6'
        elif c in ('E', 'F'):
            c = '5'
        if c.isdecimal():
            new_lst.append(c)
    if len(new_lst) == 0:
        num = 0
    else:
        num = int(''.join(new_lst))
    return num


def modify_boss_pnt(bad_num):
    bad_lst = list(bad_num)
    new_lst = []
    for i in range(len(bad_lst)):
        c = bad_lst[i]
        if c == '.' or c == ',':
            continue
        if c in ('ø', '[', '(', '!', 'I', 'a', 'l'):
            c = '0'
        elif c == '?':
            c = '2'
        elif c in ('F', 'E', 'R'):
            c = '6'
        if c.isdecimal():
            new_lst.append(c)
    if len(new_lst) == 0:
        num = 0
    else:
        num = int(''.join(new_lst))
    if num == 1:
        num = 0
    return num


def modify_flag_pnt(bad_num):
    bad_lst = list(bad_num)
    new_lst = []
    for i in range(len(bad_lst)):
        c = bad_lst[i]
        if c == 'C':
            continue
        if c == '.' or c == ',':
            if int(''.join(new_lst)) == 1:
                return 1000
            continue
        if c in ('ø', '[', '(', '!', 'I', 'a', 'l'):
            c = '0'
        elif c == '?':
            c = '2'
        elif c in ('F', 'E', 'R'):
            c = '6'
        if c.isdecimal():
            new_lst.append(c)
    if len(new_lst) == 0:
        num = 0
    else:
        num = int(''.join(new_lst))
    if num == 1:
        num = 0
    if (num < 100) and (num > 0):
        num *= 10
    if num % 50 != 0:
        ten = num % 100
        num -= ten
        num += 50
    return num


def modify_pos(bad_str, pos_gt=('메린이', '메잘알', '메둥이', '메애기', '부캐바버', '메태기', '구구구구', '유령')):
    h2j_position = []
    for pos in pos_gt:
        h2j_position.append(j2hcj(h2j(pos)))
    bad_pos = j2hcj(h2j(bad_str))
    max_sim = 0
    max_idx = 0
    for i, pos in enumerate(h2j_position):
        temp = get_similarity(bad_pos, pos)
        if max_sim < temp:
            max_idx = i
            max_sim = temp
    return pos_gt[max_idx]




def validation(week_pnt, boss_pnt, flag_pnt):
    if week_pnt == 1 and flag_pnt == 0:
        week_pnt = 0
    elif week_pnt == 0 and flag_pnt != 0:
        week_pnt = 5
    return week_pnt, boss_pnt, flag_pnt
