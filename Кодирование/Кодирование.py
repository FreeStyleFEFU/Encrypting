import random
import os
from abc import ABC, abstractmethod

class Encrypt(ABC):

    def __init__(self, name_alphabet: str, name_text: str, name_key: str):
        
        self.name_alphabet = name_alphabet
        self.name_text=name_text
        self.name_key=name_key


    def read_key(self):
        with open(self.name_key, "r",encoding="utf8") as file:
                contents = file.readlines()
                keys_list = []
                for key in range(0,len(contents)):
                    keys_list.append("")
                    for i in contents[key]:
                        if i != " " and i != "\n":
                            keys_list[key]+=i                
        return keys_list
        """
        Считывает файл текста "name_key" и заносит результат в список text_list
        --------------------------------
        args: name_key
        --------------------------------
        returns: keys_list

        """


    def read_text(self):
        with open(self.name_text, "r", encoding="utf8") as file:
            contents = file.readlines()
            text_list = []
            for key in range(0,len(contents)):
                text_list.append("")
                for i in contents[key]:
                    text_list[key]+=i            
        return text_list
        """
        Считывает файл текста "name_text" и заносит результат в список text_list
        --------------------------------
        args: name_text
        --------------------------------
        returns: text_list

        """


    @abstractmethod
    def encrypt(self)->bool:
        """
        Шифрует файл текста "name_text" на основе файла ключа "name_key" и файла с алфавитом "name_alphabet".
        Шифрованный текст записывается в тот же файл текста "name_text"
        --------------------------------
        args: name_text, name_key, name_alphabet
        --------------------------------
        returns: true, false

        """
        pass

    @abstractmethod
    def decrypt(self)->bool:
        """
        Дешифрует файл текста "name_text" на основе файла ключа "name_key" и файла с алфавитом "name_alphabet".
        Шифрованный текст записывается в тот же файл текста "name_text"
        --------------------------------
        args: name_text, name_key, name_alphabet
        --------------------------------
        returns: true, false

        """
        pass

    @abstractmethod
    def gen_key(self)->bool:
        """
        Генерирует ключ либо рандомно на основе введенной пользователем размерности "n", либо на основе алфавита 
        "name_alphabet", либо и того и другого. Результат записывается в файл ключа "name_key"
        --------------------------------
        args:  n, name_alphabet
        --------------------------------
        returns: true, false

        """
        pass


class ReplaceEncrypt(Encrypt):   

    def encrypt(self):
        text_list = self.read_text()
        key_list = self.read_key()

        encrypt_text_list = []
        without_symbols=[]
        
        for line in range(0,len(text_list)):
            encrypt_text_list.append("")
            for symbol in text_list[line]:
                if symbol == " ":
                    encrypt_text_list[line]+=" "
                elif symbol == "\n":
                    encrypt_text_list[line]+="\n"
                elif symbol != " " and symbol !="\n":
                    flag=0
                    for key in key_list:
                        if key[0] == symbol:
                            encrypt_text_list[line]+=key[2]
                            flag=1
                            break
                    if flag == 0:
                        encrypt_text_list[line]+=symbol
                        without_symbols+=symbol
        print("Следующие символы не были зашифрованы, т.к. для них нет ключа в алфавите:"+ ', '.join(set(without_symbols)))
                                      
        with open(self.name_text, "w", encoding="utf-8") as file: #записываем зашифрованный текст в файл
            for line in encrypt_text_list:
                file.writelines(line )


    def decrypt(self):
        text_list = self.read_text()
        key_list = self.read_key()
        
        decrypt_text_list = []

        for line in range(0,len(text_list)):
            decrypt_text_list.append("")
            for symbol in text_list[line]:
                if symbol == " ":
                    decrypt_text_list[line]+=" "
                elif symbol == "\n":
                    decrypt_text_list[line]+="\n"
                elif symbol != " " and symbol !="\n":
                    flag=0
                    for key in key_list:
                        if key[2] == symbol:
                            decrypt_text_list[line]+=key[0]
                            flag=1
                            break
                    if flag == 0:
                        decrypt_text_list[line]+=symbol

        with open(self.name_text, "w", encoding="utf-8") as file: #записываем список ключей в файл
            for line in decrypt_text_list:
                file.writelines(line)

    def gen_key(self):
       
        #Считываем алфавит
        with open(self.name_alphabet, "r", encoding="utf-8") as file:
            alphabet = file.read()
            for symbol in alphabet:
                if symbol == " ":
                    print("Алфавит не должен содержать пробелов")
                if symbol == "/n":
                    print("Алфавит должен располагаться на одной строке")

        #Считываем текст и создаем файл ключа
            unique = ''.join(set(alphabet)) #выбираем уникальные символы из этой строки
            key_list = []
            for key in unique:
                single_key = str(key)+"="
                if key == " ":
                    single_key+=" "
                    key_list.append(single_key)
                if key == "\n":
                    single_key+="\n"
                    key_list.append(single_key)

                else:
                    rand = random.randint(0,len(unique)-1)
                    single_key+=unique[rand] #вносим в ключ рандомный символ алфавита
                    new_alphabet=""
                    for i in range(0, len(unique)): #удаляем из алфавита использованный символ
                        if i !=rand:
                            new_alphabet  += unique[i]
                    key_list.append(single_key)
                    unique = ""
                    for i in range(0,len(new_alphabet)):
                        unique += new_alphabet[i]

            with open(self.name_key, "w", encoding="utf-8") as file: #записываем список ключей в файл
                for line in key_list:
                    file.writelines(line + "\n")
            print("Ключи сгенерированы")



class PermulationEncrypt(Encrypt):


    def encrypt(self):
        with open(self.name_text, "r", encoding="utf-8") as file:
            contents = file.readlines()
            single_string = ""
            for line in contents:
                for i in line:
                        single_string+=i
        keys_list = []
        with open(self.name_key, "r") as file:
            contents = file.readlines()                    
            for key in range(0,len(contents)):
                keys_list.append("")
                for i in contents[key]:
                    if i != " " and i != "\n":
                        keys_list[key]+=i

        new_text=""
        last = len(single_string)%len(keys_list)
        for block in range(0,len(single_string)-last,len(keys_list)):               #шифруем
            blok = []
            for symbol in range(0,len(keys_list)):                              # заполняем список блока, чтобы в дальнейшем обращаться по индексу к каждому элементу
                blok.append("")
            for symbol in range(0,len(keys_list)):
                #print(keys_list)
                blok[int(keys_list[symbol])] = single_string[int(block)+int(symbol)]
            new_text+="".join(blok)   

        for symbol in range(len(single_string)-1,len(single_string)-last-1,-1):         #инверсируем последний оставшийся блок
            new_text += single_string[symbol]

        #print(new_text)           
        with open(self.name_text, "w", encoding="utf-8") as file: #записываем список ключей в файл
            for line in new_text:
                file.writelines(line)

        

        single_string = new_text
        new_text=""
        for block in range(0,len(single_string)-last,len(keys_list)):               #расшифровка
            for symbol in range(0,len(keys_list)):         
                new_text+=single_string[block+int(keys_list[symbol])]
        

        for symbol in range(len(single_string)-1,len(single_string)-last-1,-1):         #инверсируем последний оставшийся блок
            new_text += single_string[symbol]

        return
          
    def decrypt(self):
        with open(self.name_text, "r", encoding="utf-8") as file:
            contents = file.readlines()
            single_string = ""
            for line in contents:
                for i in line:
                        single_string+=i
        keys_list = []
        with open(self.name_key, "r") as file:
            contents = file.readlines()                    
            for key in range(0,len(contents)):
                keys_list.append("")
                for i in contents[key]:
                    if i != " " and i != "\n":
                        keys_list[key]+=i
        

        new_text=""
        last = len(single_string)%len(keys_list)
        for block in range(0,len(single_string)-last,len(keys_list)):               #расшифровка
            for symbol in range(0,len(keys_list)):         
                new_text+=single_string[block+int(keys_list[symbol])]
        

        for symbol in range(len(single_string)-1,len(single_string)-last-1,-1):         #инверсируем последний оставшийся блок
            new_text += single_string[symbol]

        #print(new_text)           
        with open(self.name_text, "w", encoding="utf-8") as file: #записываем список ключей в файл
            for line in new_text:
                file.writelines(line)
            
    def gen_key(self):
        contents=[]
        single_string = ""
        try:
            with open(self.name_text, "r", encoding="utf-8") as file:
                contents = file.readlines()
                for line in contents:
                    for i in line:
                        single_string+=i  
        except:
             with open(self.name_text, "r") as file:
                contents = file.readlines()
                for line in contents:
                    for i in line:
                        single_string+=i  
        print("Введите количество символов ключа")
        n = int(input())
        keys=[]
        for i in range(0,n):
            keys.append(i)

        new_keys = []
        flag = []
        for i in range(0,len(keys)):
            flag.append(0)

        f = 0    
        while f<1:
            f = 1    
            rand = random.randint(0,len(keys)-1)
            if(flag[rand] == 0):
                new_keys.append(keys[rand])
                flag[rand] = 1
            for i in flag:
                if i == 0:
                    f = 0

        with open(self.name_key, "w", encoding="utf-8") as file: #записываем список ключей в файл
            for line in new_keys:
                file.writelines(f'{str(line)}\n')
        

class GammaEncrypt(Encrypt):
    

    def encrypt(self):
        with open(self.name_text, "r", encoding="utf-8") as file:
            contents = file.readlines()
            text = ""
            for line in contents:
                for i in line:
                        text+=i
        
        with open("gamma_key.txt", "r", encoding="utf-8") as file:
                    contents = file.readlines()
                    alphabet = []
                    for key in range(0,len(contents)):
                        alphabet.append("")
                        for i in contents[key]:
                            if i != "\n":
                                alphabet[key]+=i

        keys_list = []
        with open(self.name_key, "r") as file:
            contents = file.readlines()                    
            for key in range(0,len(contents)):
                keys_list.append("")
                for i in contents[key]:
                    if i != " " and i != "\n":
                        keys_list[key]+=i

        cipher = ""
        last = len(text) % len(keys_list) # нужен для того, чтобы цикл прошелся по количеству, кратному размеру ключа
        for block in range(0,len(text)-last,len(keys_list)):
            for symbol in range(0,len(keys_list)):
                number_cipher = 0
                flag = 0
                for s in alphabet:
                    if s[0] == text[block+symbol]: # если первый символ в файле ключа равен символу текста                       
                        number_cipher = (int(s[len(s)-1]) + int(keys_list[symbol]))%len(alphabet) # цифра, которой равен символ + соответствующее число в ключе % размерность ключа
                        print(str(s[len(s)-1]) +"   "+ str(keys_list[symbol]) +"   "+ str(len(alphabet))+"   "+str(number_cipher))
                        break
                    elif s[0] == "\\": # это для интера, ведь \n
                        number_cipher = (int(s[len(s)-1]) + int(keys_list[symbol]))%len(keys_list)
                        print(str(s[len(s)-1]) +"   "+ str(keys_list[symbol]) +"   "+ str(len(alphabet))+"   "+str(number_cipher)+'***')
                        break
                print(number_cipher)
                for s in alphabet:
                    print(s[len(s)-1]+ "   "+ str(number_cipher))
                    if int(s[len(s)-1]) == number_cipher:
                        if s[0] == "\\":                           
                            cipher += "\n"
                        else:
                            cipher += s[0]

        
        for symbol in range(0, last):
            number_cipher = 0
            flag = 0
            for s in alphabet:
                if s[0] == text[len(text) - last + symbol]:                        
                    number_cipher = (int(s[len(s)-1]) + int(keys_list[symbol]))%len(alphabet)
                    #print(str(s[len(s)-1]) +"   "+ str(keys_list[symbol]) +"   "+ str(len(alphabet))+"   "+str(number_cipher))
                    break
                elif s[0] == "\\":
                    number_cipher = (int(s[len(s)-1]) + int(keys_list[symbol]))%len(alphabet)
                    #print(str(s[len(s)-1]) +"   "+ str(keys_list[symbol]) +"   "+ str(len(alphabet))+"   "+str(number_cipher)+'***')
                    break
            #print(number_cipher)
            for s in alphabet:
                #print(s[len(s)-1]+ "   "+ str(number_cipher))
                if int(s[len(s)-1]) == number_cipher:
                    if s[0] == "\\":                           
                        cipher += "\n"
                    else:
                        #print(number_cipher,"    ", s[len(s)-1],"    ",s[0])
                        cipher += s[0]

        #print(cipher)
        
        with open(self.name_text, "w", encoding="utf-8") as file: #записываем список ключей в файл
            for line in cipher:
                file.writelines(line)

    def decrypt(self):
        with open(self.name_text, "r", encoding="utf-8") as file:
            contents = file.readlines()
            text = ""
            for line in contents:
                for i in line:
                        text+=i
        
        with open("gamma_key.txt", "r",encoding="utf-8") as file:
                    contents = file.readlines()
                    alphabet = []
                    for key in range(0,len(contents)):
                        alphabet.append("")
                        for i in contents[key]:
                            if i != "\n":
                                alphabet[key]+=i

        keys_list = []
        with open(self.name_key, "r", encoding="utf-8") as file:
            contents = file.readlines()                    
            for key in range(0,len(contents)):
                keys_list.append("")
                for i in contents[key]:
                    if i != " " and i != "\n":
                        keys_list[key]+=i

        cipher = ""
        last = len(text) % len(keys_list)
        for block in range(0,len(text)-last,len(keys_list)):
            for symbol in range(0,len(keys_list)):
                number_cipher = 0
                flag = 0
                for s in alphabet:
                    if s[0] == text[block+symbol]:                        
                        number_cipher = (int(s[len(s)-1]) - int(keys_list[symbol]))%len(alphabet)
                        print(str(s[len(s)-1]) +"   "+ str(keys_list[symbol]) +"   "+ str(len(alphabet))+"   "+str(number_cipher))
                        break
                    elif s[0] == "\\":
                        number_cipher = (int(s[len(s)-1]) - int(keys_list[symbol]))%len(alphabet)
                        print(str(s[len(s)-1]) +"   "+ str(keys_list[symbol]) +"   "+ str(len(alphabet))+"   "+str(number_cipher)+'***')
                        break
                #print(number_cipher)
                for s in alphabet:
                    #print(s[len(s)-1]+ "   "+ str(number_cipher))
                    if int(s[len(s)-1]) == number_cipher:
                        if s[0] == "\\":                           
                            cipher += "\n"
                        else:
                            cipher += s[0]

        
        for symbol in range(0, last):
            number_cipher = 0
            flag = 0
            for s in alphabet:
                if s[0] == text[len(text) - last + symbol]:                        
                    number_cipher = (int(s[len(s)-1]) - int(keys_list[symbol]))%len(alphabet)
                    print(str(s[len(s)-1]) +"   "+ str(keys_list[symbol]) +"   "+ str(len(alphabet))+"   "+str(number_cipher))
                    break
                elif s[0] == "\\":
                    number_cipher = (int(s[len(s)-1]) - int(keys_list[symbol]))%len(alphabet)
                    print(str(s[len(s)-1]) +"   "+ str(keys_list[symbol]) +"   "+ str(len(alphabet))+"   "+str(number_cipher)+'***')
                    break
            #print(number_cipher)
            for s in alphabet:
                #print(s[len(s)-1]+ "   "+ str(number_cipher))
                if int(s[len(s)-1]) == number_cipher:
                    if s[0] == "\\":                           
                        cipher += "\n"
                    else:
                        cipher += s[0]

        print(cipher)
        
        with open(self.name_text, "w", encoding="utf8") as file: #записываем список ключей в файл
            for line in cipher:
                file.writelines(line)

    def gen_key(self):

                #Считываем текст и создаем файл ключа
        with open(self.name_text, "r", encoding="utf-8") as file:
            contents = file.readlines()
            single_string = ""
            for line in contents:
                for i in line:
                        single_string+=i     #делаем из текста единую строку
            unique = ''.join(set(single_string)) #выбираем уникальные символы из этой строки
            

            print("Введите количество символов ключа")
            n = int(input())

            keys=[]
            for i in range(0,n):
                flag = 0
                while flag == 0:
                    rand = random.randint(0,99)
                    keys.append(rand)
                    flag=1
                    for j in range(0,len(keys)-1):
                        if keys[j] == rand:
                            keys.pop()
                            flag=0
                 


            with open(self.name_key, "w", encoding="utf-8") as file: #записываем список ключей в файл
                for line in keys:
                    file.writelines(f'{str(line)}\n')

            #print(unique)

            with open("gamma_key.txt", "w", encoding="utf-8") as file: #записываем список ключей в файл
                for line in range(0,len(unique)):
                    if unique[line] == "\n":
                        file.writelines("\\n"+"="+str(line)+'\n')
                        print("\n="+str(line)+'\n')
                    else:
                        file.writelines(f'{unique[line]}={line}\n')        
                           


def gui():



    replace = ReplaceEncrypt("alphabet.txt", "text.txt", "key.txt")
    permulation = PermulationEncrypt("alphabet.txt","text.txt", "key.txt")
    gamma = GammaEncrypt("alphabet.txt","text.txt", "key.txt")
    flag = 0
    while flag < 1:
        print("1 - Замены \n2 - Перестановки \n3 - Гаммирование")
        try:
            n = int(input())
        except:
            print("Данные введены некорректно")
            gui()
        if n != 1 and n != 2 and n != 3:
            print("Не выбран ни один из вариантов")
            gui()
            return
        elif n == 1:
            while flag < 1:
                print("1 - Сгенерировать ключ \n2 - Вывести текст \n3 - Вывести ключ \n4 - Зашифровать \n5 - Расшифровать \n6 - Другой шифр" )
                try:
                    n = int(input())
                except:
                    print("Данные введены некорректно")
                if n != 1 and n != 2 and n != 3 and n != 4 and n != 5 and n !=6:
                    print("Не выбран ни один из вариантов")
                    gui()
                elif n == 1:
                    replace.gen_key()
                elif n == 2:
                    text = "".join(replace.read_text())
                    print(text)
                elif n == 3:
                    list = "; ".join(replace.read_key())
                    print(list)
                elif n == 4:
                    replace.encrypt()
                elif n == 5:
                    replace.decrypt()
                elif n == 6:
                    gui()
                    return
        elif n == 2:
            while flag < 1:
                print("1 - Сгенерировать ключ \n2 - Вывести текст \n3 - Вывести ключ \n4 - Зашифровать \n5 - Расшифровать \n6 - Другой шифр" )
                try:
                    n = int(input())
                except:
                    print("Данные введены некорректно")
                if n != 1 and n != 2 and n != 3 and n != 4 and n != 5 and n !=6:
                    print("Не выбран ни один из вариантов")
                    gui()
                elif n == 1:
                    permulation.gen_key()
                    print("Ключи сгенерированы")
                elif n == 2:
                    text = "".join(permulation.read_text())
                    print(text)
                elif n == 3:
                    key = "; ".join(permulation.read_key())
                    print(key)
                elif n == 4:
                    permulation.encrypt()
                elif n == 5:
                    permulation.decrypt()
                elif n == 6:
                    gui()
                    return
        elif n == 3:
            while flag < 1:
                print("1 - Сгенерировать ключ \n2 - Вывести текст \n3 - Вывести ключ \n4 - Зашифровать \n5 - Расшифровать \n6 - Другой шифр" )
                try:
                    n = int(input())
                except:
                    print("Данные введены некорректно")
                if n != 1 and n != 2 and n != 3 and n != 4 and n != 5 and n !=6:
                    print("Не выбран ни один из вариантов")
                    gui()
                elif n == 1:
                    gamma.gen_key()
                    print("Ключи сгенерированы")
                elif n == 2:
                    text = "".join(gamma.read_text())
                    print(text)
                elif n == 3:
                  key = "; ".join(gamma.read_key())
                  print(key)
                elif n == 4:
                    gamma.encrypt()
                elif n == 5:
                    gamma.decrypt()
                elif n == 6:
                    gui()
                    return


        


if __name__ == "__main__":
    gui()

