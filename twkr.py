import re

from collections import deque

class spe_charf():

    import os

    def advs(input_l, spe_char=[], exclude=True):

        rtn_l = []

        if exclude == True:

            bool_l = list(map(lambda x : x not in spe_char, input_l))

        else:

            bool_l = list(map(lambda x : x in spe_char, input_l))

        for x in range(len(bool_l)):

            if bool_l[x] == True:

                rtn_l.append(input_l[x])

        return rtn_l

    def advs_sub(input_l, sub_char=[], exclude=True):

        rtn_l = []

        if exclude == True:

            bool_l = list(map(lambda x : [ i not in x for i in sub_char ], input_l))

            for x in range(len(bool_l)):

                if all(bool_l[x]):

                    rtn_l.append(input_l[x])

            return rtn_l

        else:

            bool_l = list(map(lambda x : [ i in x for i in sub_char ], input_l))

            for x in range(len(bool_l)):

                if True in bool_l[x]:

                    rtn_l.append(input_l[x])

            return rtn_l

    def file_rec(path=".", tracker_l=[os.listdir(".")], cur_depth=0, depth="max", rtn_l=[], type_rtn="file", excl=[], sub_excl=[], frst_path="."):

        if path != frst_path or len(tracker_l) != 0:

            ln = len(tracker_l[cur_depth])

            cnt = 0

            last_len = len(rtn_l)

            while cnt < ln:

                cur_f = tracker_l[cur_depth][cnt]

                rtn_l.append(cur_f)
                
                if os.path.isdir(cur_f) == True:

                    if depth == "max" or cur_depth < depth:

                        path += "/{}".format(cur_f.split("/")[-1])

                        cur_depth += 1
        
                        tracker_l[-1] = advs(tracker_l[-1], rtn_l[last_len:])

                        tracker_l.append([ path + "/" + f for f in os.listdir(path) ])

                        return file_rec(path=path, tracker_l=tracker_l, cur_depth=cur_depth, depth=depth, rtn_l=rtn_l, excl=excl, sub_excl=sub_excl, frst_path=frst_path)

                cnt += 1

            if path != frst_path:

                path = "/".join(path.split("/")[:-1])

                cur_depth -= 1

            tracker_l[-1] = []

            tracker_l.pop()

            while len(tracker_l) > 1 and len(tracker_l[-1]) == 0:

                path = "/".join(path.split("/")[:-1])

                tracker_l.pop()

                cur_depth -= 1

            return file_rec(path=path, tracker_l=tracker_l, depth=depth, rtn_l=rtn_l, cur_depth=cur_depth, excl=excl, sub_excl=sub_excl, frst_path=frst_path)

        else:

            if type_rtn == "file":

                rtn_l2 = []
        
                for f in rtn_l:

                    if os.path.isdir(f) == False and "__pycache__" not in f and f not in excl:

                        rtn_l2.append(f)

            elif type_rtn == "folder":

                rtn_l2 = []
        
                for f in rtn_l:

                    if os.path.isdir(f) == True and "__pycache__" not in f and f not in excl:

                        rtn_l2.append(f)

            if len(sub_excl) > 0:

                print(sub_excl)

                rtn_l2 = advs_sub(rtn_l2, sub_excl)   

            return rtn_l2

class unnester():

    def inter_max(inpt_l, max_=-1000, get_lst=True):

        for lst in range(len(inpt_l)):

            diff_l = []

            for el in range(len(inpt_l[lst]) - 1):

                 diff_l.append(inpt_l[lst][el + 1] - inpt_l[lst][el])

            if max(diff_l) > max_:

                max_ = max(diff_l)

        cnt = 0

        for lst in inpt_l:

            inpt_l[cnt] = [] 
        
            add_val = lst[0]

            while add_val <= lst[-1]:

                inpt_l[cnt].append(add_val)

                add_val += max_

            if get_lst and lst[-1] != inpt_l[cnt][-1]:

                inpt_l[cnt].append(lst[-1])

            cnt += 1

        return inpt_l

    def inter_min(inpt_l, min_=1000, sensi=3,  sensi2=3, how_to_op=deque(["divide"]), how_to_val=deque([3])):

        diff_l2 = []

        diff_l = []

        for lst in range(len(inpt_l)):

            for idx in range(len(inpt_l[lst]) - 1):

                diff_l.append(round((inpt_l[lst][idx + 1] - inpt_l[lst][idx]), sensi))

            [ diff_l2.append(el) for el in diff_l ]

            if min(diff_l) < min_:

                min_ = min(diff_l)

                diff_l = []

        def verify(diff_l2, min_):

            for delta in diff_l2:

                pre_val = delta / min_ % 1

                pre_val_str = str(pre_val).split(".")[1][0:(sensi+1)]

                if pre_val_str[-1] != "9":

                    all_eq = 0

                else:

                    all_eq = 1

                    for i in range(len(pre_val_str) - 1):

                        if pre_val_str[i + 1] != pre_val_str[i] or pre_val_str[i] != "9":

                            all_eq == 0

                if round(pre_val * (10 ** sensi), 0) != 0 and all_eq != 1:

                    ht = how_to_op[0]

                    nb = how_to_val[0]

                    if len(how_to_op) > 1:

                        how_to_op.popleft()

                    if len(how_to_val) > 1:

                        how_to_val.popleft()
                    
                    if ht == "divide":

                        min_ /= nb

                        min_ = round(min_, sensi)

                    elif ht == "add":

                        min_ += nb

                    elif ht == "multiply":

                        min_ *= nb

                    elif ht == "substract":

                        min_ -= nb

                    return verify(diff_l2=diff_l2, min_=min_)

            cnt = 0

            for lst in inpt_l:

                inpt_l[cnt] = []

                add_val = lst[0]

                while add_val <= lst[-1]:

                    inpt_l[cnt].append(add_val)

                    add_val += min_ 

                    add_val = round(add_val, sensi2)

                cnt += 1
        
            return inpt_l

        rtn_l = verify(diff_l2=diff_l2, min_=min_)

        return rtn_l

    def nestfind(input_l, dim_search):

        rtn_lb = input_l

        for i in dim_search:

            rtn_lb = rtn_lb[i]

        return rtn_lb

    def end_(input_l, rtn_l, flag_l, dim_end):

        idx = -1

        adjust = 1

        for el in range(len(flag_l)):

            if el == 0:

                idx += len(unnester.nestfind(input_l, flag_l[el])) + flag_l[el][-1]

            elif len(flag_l[el]) == len(flag_l[el - 1]):

                idx += len(unnester.nestfind(input_l, flag_l[el])) + (flag_l[el][-1] - flag_l[el - 1][-1]) - 1

            elif len(flag_l[el]) > len(flag_l[el - 1]): 

                idx += len(unnester.nestfind(input_l, flag_l[el])) - (len(unnester.nestfind(input_l, flag_l[el - 1])) - flag_l[el][-1])

            else:

                len_flag_l_curr = len(flag_l[el])

                remain_idx = 0

                for i in range(1, len(flag_l[el - 1]) - len_flag_l_curr + 1):

                    remain_idx += len(unnester.nestfind(input_l, flag_l[el - 1][0:len(flag_l[el - 1]) - i])) - flag_l[el - 1][-i] - 1

                idx += len(unnester.nestfind(input_l, flag_l[el])) + (flag_l[el][-1] - flag_l[el - 1][len_flag_l_curr - 1]) - 1 + remain_idx 

            if len(flag_l[el]) == dim_end:

                cur = unnester.nestfind(input_l, flag_l[el])

                rtn_l[idx - len(cur) + adjust:idx + adjust] = [cur]

                adjust -= (len(cur) - 1)

        return rtn_l

    def ns(input_l, dim_end=1, strt_l=[], rtn_l=[], id_rec_main=0, wrk_l=None, flag_l=[]):

        wrk_l = input_l

        wrk_l_pre = []

        for i in range(len(strt_l)):

            wrk_l_pre.append(wrk_l)

            if type(wrk_l[strt_l[i]]) != list:

                wrk_l = [wrk_l[strt_l[i]]]

            else:

                wrk_l = wrk_l[strt_l[i]]

        list_status = False

        if len(strt_l) == 0:

            cnt = id_rec_main

        else:

            cnt = 0

        while list_status == False and cnt < len(wrk_l):

            if type(wrk_l[cnt]) == list:

                strt_l.append(cnt)

                list_status = True

            else:

                if len(strt_l) == 0:

                    id_rec_main += 1

                rtn_l.append(wrk_l[cnt])

            cnt += 1

        if list_status == False:

            if len(strt_l) > 0:

                if strt_l[-1] + 1 == len(wrk_l_pre[-1]):

                    if len(strt_l) == 1:

                        id_rec_main += 1

                        if id_rec_main == len(input_l):

                            return unnester.end_(input_l, rtn_l, flag_l, dim_end)

                    strt_l.pop()

                    wrk_l_pre.pop()

                if len(strt_l) > 0:

                    next_ = False

                    while next_ == False and len(strt_l) > 0:

                        if strt_l[-1] + 1 < len(wrk_l_pre[-1]):

                            if strt_l[-1] < len(wrk_l_pre[-1]) - 1:

                                stop = 0

                                while stop == 0:

                                    strt_l[-1] += 1

                                    if strt_l[-1] == len(wrk_l_pre[-1]) - 1:

                                        if len(strt_l) == 1:

                                            id_rec_main += 1

                                            strt_l.pop()

                                            if id_rec_main == len(input_l):

                                                return unnester.end_(input_l, rtn_l, flag_l, dim_end)

                                        stop = 1

                                    else:

                                        if  type(wrk_l_pre[-1][strt_l[-1]]) == list:

                                            stop = 1

                                        else:

                                            rtn_l.append(wrk_l_pre[-1][strt_l[-1]])

                                        if len(strt_l) == 1:

                                            id_rec_main += 1

                                            if id_rec_main == len(input_l):

                                                return unnester.end_(input_l, rtn_l, flag_l, dim_end)
                            else:

                                strt_l[-1] += 1

                                if len(strt_l) == 1:

                                    id_rec_main += 1

                                    if id_rec_main == len(input_l):

                                        return unnester.end_(input_l, rtn_l, flag_l, dim_end) 

                            next_ = True

                        else:

                            strt_l.pop()

                            wrk_l_pre.pop() 

                            if len(strt_l) == 0:

                                id_rec_main += 1

                                if id_rec_main == len(input_l):

                                    return unnester.end_(input_l, rtn_l, flag_l, dim_end)

                else:

                    id_rec_main += 1

                    if id_rec_main == len(input_l):

                        return unnester.end_(input_l, rtn_l, flag_l, dim_end)

            elif id_rec_main == len(input_l):

                return unnester.end_(input_l, rtn_l, flag_l, dim_end) 

        if len(strt_l) <= dim_end and len(strt_l) > 0 and type(unnester.nestfind(input_l, strt_l)) == list:

            if len(flag_l) > 0:

                if strt_l != flag_l[-1]:

                    flag_l.append([ el for el in strt_l ])

            else:

                flag_l.append([ el for el in strt_l ])

        return unnester.ns(input_l, dim_end, strt_l, rtn_l, id_rec_main, wrk_l, flag_l)

class globe():

    def distance(lat1, long1, lat_l, long_l, alt_l=None, alt1=None):

        rtnl = []

        for i in range(len(lat_l)):

            sin_comp = abs(math.sin(math.pi * ((lat_l[i] + 90) / 180))) 

            if abs(long1 - long_l[i]) != 0:

                delta_long = (40075 / (360 / abs(long1 - long_l[i]))) * sin_comp

            else:

                delta_long = 0

            if abs(lat1 - lat_l[i]) != 0:
            
                delta_lat = 20037.5 / (180 / abs(lat1 - lat_l[i]))

            else:

                delta_lat = 0

            delta_f = (delta_lat ** 2 + delta_long ** 2) ** 0.5

            if alt1 != None:

                delta_f = ((alt1 - alt_l[i]) ** 2 + delta_f ** 2) ** 0.5 

            rtnl.append(delta_f)

        return(rtnl)

