value = input("write text: ")
ans=""
for char in value:
    if(char.isalpha()):
        new_chr = ((ord(char)-97+2)%26)+97
        print(chr(new_chr))
        ans += chr(new_chr)
    else:
        
        new_chr = ((ord(char)-65+2)%26)+65
        print(chr(new_chr))
        ans += chr(new_chr)
