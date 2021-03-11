from math import gcd

#----- Setting up to process cycle inputs -----

# returns a set of members in the input
def input_to_items(input):
    items = set() 
    item = ""
    for char in input:
        if(char != '('):
            if((char == ' ' or char == ')') and item != ""):
                items.add(item)
                item = ""
            else:
                item += char
    return sorted(items, key=int) 

def find_size(input):
    max_string = ""
    mx = 0
    for char in input:
        if(char != '('):
            if((char == ' ' or char == ')') and max_string != ""):
                if int(max_string) > mx :
                    mx = int(max_string)
                max_string = ""
            else:
                max_string += char
    return mx

def process_input(input):
    # Checks for parentheses closure
    lp = []
    rp = []
    for i in range(len(input)):
        if input[i] == '(':
            lp.append(i)
        elif input[i] == ')':
            rp.append(i)
    if len(lp) != len(rp):
        raise Exception('Mismatched Parentheses.')
    else:
        for i in range(len(lp)):
            if lp[i] > rp[i]:
                raise Exception('Mismatched Parentheses.')

    pin = input.replace('(', '')
    pin = pin.split(')')
    pin.pop()
    pin = [i.split(' ') for i in pin]
    
    # Checks for duplicate indices in cycles
    for i in pin:
        if has_duplicates(i):
            raise Exception('The same number cannot be used twice in a cycle')
    
    return pin 

# Check if input is disjoint
def is_disjoint(textin):
    textin = textin.replace('(', '')
    textin = textin.replace(')', ' ')
    listin = textin.split()

    if has_duplicates(listin):
        return False
    return True

def has_duplicates(listin):
    set_of_elem = set()
    for elem in listin:
        if elem in set_of_elem:
            return True
        else:
            set_of_elem.add(elem)
    return False

# Reduce a permutation input to disjoint cycles
def reduce_cycle(input):
    size = find_size(input)

    mapping = process_input(input)
    search_from = input_to_items(input)
    output = list(map(str, list(range(1, size+1))))
    for i in range(1, size+1):
        temp = str(i)
        for cycle in reversed(mapping):
            try: 
                index = cycle.index(str(temp))
                temp = cycle[(index + 1) % len(cycle)]
            except: 
                pass
        output[i-1] = temp
    return display_as_cycle(output)

# displays in cycle form (after reduce_cycle(); array form input)
def display_as_cycle(arr_in):
    size = len(arr_in)
    checklist = [False] * size
    # Print in cycle form
    cycle = '('
    count = head = current = 0
    while count < size: 
        if arr_in[current] == str(current + 1):
            checklist[current] = True
            try:
                head = current = checklist.index(False)
            except:
                pass
            count += 1

        else:
            if int(arr_in[current]) - 1 != head:
                cycle += str(current + 1) + ' '
                count += 1
                checklist[current] = True
                current = int(arr_in[current]) - 1

            else:
                cycle += str(current + 1)
                cycle += ')('
                count += 1
                checklist[current] = True
                try:
                    current = head = checklist.index(False)
                except:
                    pass
    cycle = cycle[:-1]
    return cycle

def lcm(listin):
    lcm = listin[0]
    for i in listin[1:]:
        lcm = lcm * i / gcd(lcm, i)
    return lcm

#----- Methods for finding order and parity -----

# order is the LCM of length of disjoint cycles
def find_order(textin):
    if not is_disjoint(textin):
        textin = reduce_cycle(textin)
    lens = [len(i) for i in process_input(textin)]
    return int(lcm(lens))

# parity is -1 to the power of transpositions
def find_parity(textin):
    transpositions = [len(i) - 1 for i in process_input(textin)]
    return (-1)**sum(transpositions)

print(find_order("(1 2 3)(3 5)(1 4)(2 6)(4 7)"))
print(reduce_cycle("(1 2 3)(3 5)(1 4)(2 6)(4 7)"))
print(find_parity("(1 2 3)(3 5)(5 1)(2 4)(1 7)"))



