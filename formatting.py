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

#prettifying the xml
def formatting(text):
    
    xml = removing_spaces(text)
    ind =0
    new_xml = str()
    
    i =0
 
    
    while i < len(xml):
        
        if i+1  < len(xml) and xml[i+1] == "<":
            if i+2 < len(xml) and xml[i+2] != "/":
            
                ind+=1
                new_xml += xml[i]
                
                i+=1
            
                if (xml[i-1 ] == ">"):
                
                    new_xml += "\n"
                    new_xml += adding_spaces(ind)
                
                
                
            else:
            
                new_xml += xml[i]
                
                i+=1
            
                if (xml[i-1 ] == ">"):
                
                    new_xml += "\n"
                    new_xml += adding_spaces(ind)
                         
                ind -=1 
            
            
        if i + 1 < len(xml):
            if ( xml[i] == '?' or xml[i] == '/') and xml[i + 1] == '>':
                ind -= 1
        
        new_xml += xml[i]
        i += 1            
            
    return new_xml

