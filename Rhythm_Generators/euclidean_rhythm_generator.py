
def generate_euclidean(onsets, pulses):
    front = [[1] for i in range(onsets)]
    back = [[0] for i in range(pulses)]
    return [item for sublist in euclidian_recursive(front, back) for item in sublist]


def euclidian_recursive(front, back):
    if len(back) <= 1:
        return front+back
    else:
        new_front = []
        while len(front) > 0 and len(back) > 0:
            new_front.append(front.pop()+back.pop())
        return euclidian_recursive(new_front, back+front)

def euclidian_splitter(array):
    # This can be done better....
    res = []
    sub_array = []
    while len(array) > 0:
        val = array.pop(0)
        if val == 1:
            res.append(sub_array)
            sub_array = [1]
        else:
            sub_array.append(val)
    res.append(sub_array)
    return res[1:]



if __name__ == '__main__':
    print(generate_euclidean(6, 8))
    euc = generate_euclidean(6, 8)
    print(euclidian_splitter(euc))

