import pathlib
import os
import re

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s



filepath1 = str(pathlib.Path().absolute()) + '/data/domain.txt'.replace('/', os.sep)
list_domain = []

with open(filepath1, encoding="utf8") as fp:
    line = fp.readline()
    cnt = 1
    while line:
        text = line.replace("\n", "").lower()
        text = text.replace("- ","")
        list_domain.append(text)
        line = fp.readline()
        cnt += 1

with open('story.txt',"w") as f:
    for i in range(len(list_domain)):
        f.write("- story : {} \n  steps:\n  - intent: {}\n  - action: utter_{} \n\n".format(list_domain[i],list_domain[i],list_domain[i],list_domain[i]))
