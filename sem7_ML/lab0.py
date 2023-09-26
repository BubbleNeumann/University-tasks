with open('input.txt', 'r') as inp, open('output.txt', 'w') as out:
    lines = inp.readlines()
    for line in lines:
        arr = line.split(',')
        try:
            out.write(f'{int(arr[1]) + int(arr[2])}\n')
        except:
            pass
