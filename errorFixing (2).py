from Stack import *
from final_formatting import *
#used to fix open tags
def errorFixing(line):
    lines = removing_spaces(line)
    j = 0
    m = Stack()
    k = ''
    arr = []
    st = Stack()
    no_of_lines = 1
    str_between_tags = ""
    # new = str()
    new = ''
    errors = Stack()
    while j < len(lines):
        if lines[j] == '<':
            j += 1
            k = ''
            if (lines[j] >= 'A' and lines[j] <= 'Z') or (lines[j] >= 'a' and lines <= 'z'):
                new = new + str_between_tags
                str_between_tags = ''
                new = new + '<'
                while lines[j] != '>':
                    k += lines[j]  # id
                    new = new + lines[j]
                    j += 1
                new = new + lines[j]  # <users> <user>
                j += 1
                m.push(k)  # users user
            else:
                if lines[j] == '/':
                    j += 1
                    s = ''
                    while lines[j] != '>':
                        s += lines[j]  # id
                        j += 1
                    j += 1
                    if (not m.is_empty() and m.top() == s):  # m.top=user s=id
                        new = new + str_between_tags + f'</{m.top()}>'
                        str_between_tags = ''
                        m.pop()
                    else:
                        while (not m.is_empty() and m.top() != s):
                            errors.push(m.top())  # errors= id
                            m.pop()  # user w users
                        if (m.is_empty()):
                            new = new + '<' + s + '>' + str_between_tags
                            str_between_tags = ''
                            while (not errors.is_empty()):
                                m.push(errors.top())
                                errors.pop()

                            new = new + '</' + s + '>'
                        else:
                            while(not errors.is_empty()):
                                st.push(errors.top())  # id
                                errors.pop()
                            if(s == m.top()):
                                new = new + str_between_tags + f'</{m.top()}>'
                                str_between_tags = ''
                                m.pop()
        else:
            str_between_tags = str_between_tags + lines[j]
            j = j + 1
    while(not m.is_empty()):
        st.push(m.top())
        m.pop()
    return(formatting(fix_closed(new,st)))

#
# #used to fix the closed tags
def fix_closed(lines,st2):
    j = 0
    text =''
    while j < len(lines):
        if lines[j] == '<':
            text += lines[j]
            j+=1
            s =''
            if((lines[j] >= 'A' and lines[j] <= 'Z') or (lines[j] >= 'a' and lines[j] <= 'z')):
                while lines[j] != '>':
                    text += lines[j]
                    s+= lines[j]
                    j+=1
                text += lines[j]
                j+=1
                if(not st2.is_empty() and st2.top() == s):
                    while(lines[j] != '<'):
                        text += lines[j]
                        j+=1
                    s2 = ''
                    if lines[j + 1] == '/':
                        j+=2
                        while lines[j] != '>':
                            s2 += lines[j]
                            j+=1
                        if(s2 != s):
                            st2.pop()
                            text = text + '</' + s + '>'
                            text = text + '</' + s2 + '>'
                            j+=1
                        else:
                            text = text + '</' + s2 + '>'
                            j+=1
                    elif(not st2.is_empty()):
                        st2.pop()
                        text = text + '</' + s + '>'


        else:
            text += lines[j]
            j+=1
    while(not st2.is_empty()):
        text = text + '</' + st2.top() + '>'
        st2.pop()
    return formatting(text)