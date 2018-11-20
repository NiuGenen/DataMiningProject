def print_list(data, elem_line_nr):
    data=[]
    n = data.__len__()
    cnt = 0
    str = ""
    for item in data:
        str = str + item.__str__() + "\t"
        cnt += 1
        if cnt is elem_line_nr:
            print(str)
            str = ""
            cnt = 0
    if cnt < elem_line_nr:
        print(str)

def add_into_dict(_dict, _k, _v, op, init_value):
    if op is "+":
        if _dict.__contains__(_k):
            _dict[_k] += _v
        else:
            _dict[_k] = init_value
