
# coding: utf-8
#Скрипт архивирует выбранные папки которые перечисленны в list.txt и заливает их в облако
#Настройки хранятся в файле setting.ini

#Загрузим библиотеки:
import os
import zipfile
import time
import datetime
import shutil 

logf    = open("output.log", 'w') 
in_data = []

#Считываем настройки из файла setting.ini (пока только путь для создания архивов):
with open ('setting.ini', 'r') as inf:
    in_data.append(inf.readlines())

#Используемые пути (возможно стоит вынести во внешний файл конфигурации):
backup_path = in_data[0][0]

#Переменные времени
start_time = time.time() #Время начала архивации
end_time   = 0           #Время конца архивации

#Для создания метки архива и папки:
time_stamp = datetime.datetime.now().time().strftime('%H%M%S') #Текущее время 
date_stamp = datetime.datetime.now().date().strftime('%Y%m%d') #Текущая дата  

#Дата и время создания архива:
print(datetime.datetime.now())
logf.write(str(datetime.datetime.now()) + '\n')


#Проверим существует ли путь для резервного копирования, и если нет создадим его:
if os.path.exists(backup_path):
    print('Путь для резервного копирования: OK')
    logf.write('Путь для резервного копирования: OK' + '\n')
else:
    os.mkdir(backup_path)
    print('Путь для резервного копирования создан')
    logf.write('Путь для резервного копирования создан' + '\n')

#Массивы для обработки данных.
#data хранит в себе список папок которые неообходимо заархивировать.
out_data=[]

#Откроем и прочитаем файл со списком папок которые необходимо заархивировать:
with open ('list.txt', 'r') as inf:
    out_data.append(inf.readlines())

# Обрежем от массива служебные символы:
for i in range(0,len(out_data[0]),1):
    out_data[0][i] = out_data[0][i].strip()    
    
#bstat хранит статистику архивирования (размерность количество заархивированых папок * 2
#(количество обработанных каталогов и файлов)). Генерируется отдельно так как нужна
#размерность data
bstat = [[0 for i in range(0,len(out_data[0]),1)] for j in range(0,2,1)]    

#Сгенирируем имя папки из текущей даты и времени:
os.mkdir (backup_path + '\\' + date_stamp + '_' + time_stamp)
print("Создана папка:", backup_path + '\\' + date_stamp + '_' + time_stamp)
logf.write("Создана папка:"+ '\t' + backup_path + '\\' + date_stamp + '_' + time_stamp + '\n')

#Архивирование
data_type = 0 #0 - Files, 1 - Dirs
fname   = 0     #Для выделения имени файлы и зезультата комманды os.path.splitext
dirname = 1     #Для выделения результата команды os.path.split

not_exist = 0   #1 - данные не существуют

#Для выбранной папки из list.txt:
archd_dirs  = 0 #Заархивировано папок
archd_files = 0 #Заархивировано файлов

real_dirs   = 0 #Количество папок для архивации
real_files  = 0 #Файлов для архивации

total_dirs  = 0
total_files = 0

for i in range(0,len(out_data[0]),1):
    print()
#Проверяем существование файлов, в случае если файл отсутствует, пропускаем его
    if os.path.exists(str(out_data[0][i])):
        print("Путь", str(out_data[0][i]), "существует, обрабатываем:")
        logf.write("Путь" + ' ' + str(out_data[0][i]) + ' ' + "существует, обрабатываем:" + ' ')
        not_exist = 0
    else:
        print("Путь", str(out_data[0][i]), "не существует, пропускаем.")
        logf.write("Путь" + ' ' + str(out_data[0][i]) + ' ' + "не существует, пропускаем." + '\n')
        not_exist = 1

    if not_exist == 0:
#Разбиваем данные на группы: файлы и папки, у файлов отрезаем расширение   
        if os.path.isfile(out_data[0][i]):
            data_type = 0
            zfile = os.path.splitext (os.path.split(out_data[0][i])[dirname])[fname]  + '_' + date_stamp +'.zip'
        else:
            data_type = 1
            zfile = os.path.split(out_data[0][i])[dirname] + '_' + date_stamp +'.zip'
        
        bzip = zipfile.ZipFile (backup_path + "\\" + date_stamp+'_'+time_stamp + "\\" + zfile, 'w')

#Архивируем папки:
        if data_type == 1:   
            for folder, subfolders, files in os.walk(out_data[0][i].strip()):
                print('*', end = '')
        
                for subfolder in subfolders:
                    #Подсчитаем количество папок
                    real_dirs = real_dirs + 1
                
                    bzip.write(os.path.join(folder, subfolder), os.path.relpath(os.path.join(folder, subfolder), out_data[0][i]), compress_type = zipfile.ZIP_STORED)  
                    #Подсчитаем количество обработанных папок
                    archd_dirs = archd_dirs + 1
                
                for file in files:
                    real_files  = real_files + 1
                    bzip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), out_data[0][i]), compress_type = zipfile.ZIP_STORED)               
                    archd_files  = archd_files + 1

#Архивируем файлы:
        else:
            print('*', end = '')
            real_files  = real_files + 1
            bzip.write(out_data[0][i], compress_type = zipfile.ZIP_STORED)
            archd_files  = archd_files + 1

        print()    
        if archd_dirs == real_dirs and archd_files == real_files:
            print("OK")
            logf.write("OK" + '\n')
        else:
            print('Ошибка')
            logf.write('Ошибка' + '\n')
        
        total_dirs  = total_dirs  + archd_dirs
        total_files = total_files + archd_files
        archd_dirs  = 0 
        archd_files = 0 
        real_dirs   = 0 
        real_files  = 0 
    
bzip.close()
#Вычисляем время затраченное на архивирование в сек.
end_time   = time.time()
print()
print("Всего обработано папок:", total_dirs)
logf.write('\n' + "Всего обработано папок: " + str(total_dirs) + '\n')

print("Всего обработано файлов:", total_files)
logf.write("Всего обработано файлов: " + str(total_files) + '\n')

print("Затрачено времени на создание архивов: ", str(end_time-start_time), "сек")
logf.write("Затрачено времени на создание архивов: " + str(round(end_time-start_time, 3)) + ' ' + "сек" + '\n')

logf.close()

#Копируем полученный лог в папку архивов:
shutil.move('output.log', backup_path + '\\' + date_stamp + '_' + time_stamp)


