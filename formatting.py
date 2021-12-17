#deleting spaces between tags
def removing_spaces(text):
    k = 0
    string = ('>'.join([subtext.strip('\n' ' ' '\t') for subtext in text.split('>')]))
    i = 0
    while i < len(string)-2:
        if string[i] == '<' and string[i+1] == '/':
            z = i
            if (string[i-1] == '/n'  or string[i-1] == '/t' or string[i-1] == ' '):
                while(string[i-1] == '/n'  or string[i-1] == '/t' or string[i-1] == ' '):
                    k -= 1
                    i-=1
                    if (i==0): break
                string = string[:i-1] + string[z:]

        k += 1
        i += 1

    return string
    
    
#adding tap to prettify 
def adding_spaces(ind):
    i = 0
    string = str()
    while i < ind:
        string += "     "
        i += 1
    return string
