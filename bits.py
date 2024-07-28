def text_to_int(text):
    s = []
    for i in text:
        s.append(int(ord(i)))
    return s

def int_to_text(i):
    text = ""
    for b in i:
        text += chr(b)
    return text
   