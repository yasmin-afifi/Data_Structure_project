from Stack import *
from final_formatting import *

#function used  to detect errors
def detectErrors(lines):
    j = 0
    no_of_lines = 1
    m = Stack()
    n = Stack()
    errors = Stack()
    list_of_errors = []
    while j < len(lines):
        if lines[j] == '\n':
            no_of_lines = no_of_lines + 1
        if lines[j] == '<':
            j+=1
            if (lines[j] >= 'A' and lines[j] <= 'Z') or (lines[j] >= 'a' and lines <= 'z'):
                s = ''
                while lines[j] != '>':
                    s += lines[j]
                    j+=1
                j+=1
                m.push(s)
                n.push(no_of_lines)
            else:
              if lines[j] == '/':
                j+=1
                s =''
                while lines[j] != '>':
                    s += lines[j]   #s=id
                    j+=1
                j+=1
                c = 0
                if(not m.is_empty() and m.top() != s):  #m.top=user
                    while(not m.is_empty() and m.top() != s):
                        errors.push(m.top())
                        m.pop()
                        c+=1
                    if(m.is_empty()):
                        list_of_errors.append(no_of_lines)
                        while(not errors.is_empty()):
                            m.push(errors.top())
                            errors.pop()
                    else:
                        m.pop()
                        while(c!=0 and not n.is_empty()):
                            list_of_errors.append(n.top())
                            n.pop()
                            c-=1
                elif(m.is_empty()):
                    list_of_errors.append(no_of_lines)
                else:
                    if (not m.is_empty()):
                     m.pop()
                     n.pop()

        else:
            j+=1
    if (not m.is_empty()):
        list_of_errors.append(n.top())
        n.pop()
    text = ''
    for i in range(len(list_of_errors)):
        text+= 'Error ' + str(i + 1) + ' in line ' + str(list_of_errors[i]) + '\n'
        i=i+1
    return text