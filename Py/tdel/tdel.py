import os
import datetime

#Храним файлы n дней
n = 1
#Определяем текущую дату 
today = datetime.datetime.today()

try: 
#Собираем все файлы которые есть в папке в массив:
    path = "C:\\Users\\admin\\Videos\\Debut"
    files = os.listdir(path)

#В цикле проверяем каждый файл и дату его создания, если 
#если файл создан за n дней до сегодня, удаляем его

    for i in range(0,len(files),1):
        f_path = os.path.join(path,files[i])
        file_ut = os.path.getctime(f_path)  
        file_dt = datetime.datetime.fromtimestamp(file_ut)
    
        tdiff = (today - file_dt).days
    
        if tdiff >= n:
            os.remove(f_path)
            print('-', endl = '')
    print('OK')

except FileNotFoundError:
    print ('File not found')

