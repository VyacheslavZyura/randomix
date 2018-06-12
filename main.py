# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys, os, random, shutil

#Функции

# Выбор необходимой папки, при нажатии "Отсюда"
# Если папка не выбирается, выскакивает ошибка, которая снова запускает
# необходимое окно
def src_FileDialog():

    dialog_src = QtWidgets.QFileDialog(parent=window,
                               filter="",
                               caption="Отсюда будут собраны музыкальные композиции")
    dialog_src.setFileMode(QtWidgets.QFileDialog.Directory)
    dialog_src.setOption(QtWidgets.QFileDialog.ShowDirsOnly, False)
    dialog_src.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
    result_src = dialog_src.exec()
    if result_src == QtWidgets.QDialog.Accepted:
        global src0
        src0 = dialog_src.selectedFiles()
        src_button.setToolTip(src0[0])
    else:
        QtWidgets.QMessageBox.information(window, "Вы не выбрали папку", 
                                            "Чтобы все сработало, программа должна знать откуда генерировать песни",
                                            buttons=QtWidgets.QMessageBox.Ok,
                                            defaultButton=QtWidgets.QMessageBox.Ok)
        src_FileDialog()

# Выбор необходимой папки, при нажатии "Сюда"
# Если папка не выбирается, выскакивает ошибка, которая снова запускает
# необходимое окно
def dst_FileDialog():

    dialog_dst = QtWidgets.QFileDialog(parent=window,
                               filter="",
                               caption="Сюда будут сгенерированы случайные композиции")
    dialog_dst.setFileMode(QtWidgets.QFileDialog.Directory)
    dialog_dst.setOption(QtWidgets.QFileDialog.ShowDirsOnly, False)
    dialog_dst.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
    result_dst = dialog_dst.exec()
    if result_dst == QtWidgets.QDialog.Accepted:
        global dst0
        dst0 = dialog_dst.selectedFiles()
        dst_button.setToolTip(dst0[0])
    else:
        QtWidgets.QMessageBox.information(window, "Вы не выбрали папку", 
                                            "Чтобы все сработало, программа должна знать куда генерировать песни",
                                            buttons=QtWidgets.QMessageBox.Ok,
                                            defaultButton=QtWidgets.QMessageBox.Ok)
        dst_FileDialog()

# Запускается при нажатии кнопки "Сформировать"
def general_func():
    if src0 and dst0 and size_Box.value(): # Необходима проверка на ошибку вхожных данных
        size = size_Box.value()        
        sort_music(src0,dst0,size)
       
        QtWidgets.QMessageBox.information(window, "Готово", 
                                            "Песни собраны, наслаждайтесь!",
                                            buttons=QtWidgets.QMessageBox.Ok,
                                            defaultButton=QtWidgets.QMessageBox.Ok)
    else: 
        QtWidgets.QMessageBox.information(window, "Вы ввели не все данные", 
                                            "Чтобы все заработало, программа должна знать откуда, куда и сколько песен генерировать",
                                            buttons=QtWidgets.QMessageBox.Ok,
                                            defaultButton=QtWidgets.QMessageBox.Ok)
        
# Функция сортировки файлов, принимает на вход три переменные путь "отсюда", "сюда"
# и переменную ограничения размера
def sort_music(src, dst, size):
    files = [] 
    src = src0[0]
    dst = dst0[0]
    dir_size = 0
    dir_limit = size*1024*1024 # перевод из мб в байты
    lim_file = 21*1024*1024 # ограничение на вес файла
    type = ".mp3"

    # создаем список всех файлов в директории и всех подпапках
    for top, x, f in os.walk(src):
        for nm in f:
            files.append(os.path.join(top, nm))
    
    # фильтруем список файлов по необходимому расширению и перемешиваем
    res = [z for z in files if (z.endswith(type)) and (os.path.getsize(z)<= lim_file)]
    random.shuffle(res)
   
    # копирование файлов, ограничено заданным размером size
    for file in res:
        dir_size += os.path.getsize(file)
        if dir_size > dir_limit:
            break
        shutil.copy (file, dst)


# Приложение

# Параметры приложения - стиль и иконка
app = QtWidgets.QApplication(sys.argv)
app.setStyle("windowsvista") 
main_icon = QtGui.QIcon(".\Temp\icon.ico")
app.setWindowIcon(main_icon)    

# Главное окно, параметры, иконка в верхней полосе
window = QtWidgets.QWidget()
window.setWindowFlags(QtCore.Qt.Window | 
                      QtCore.Qt.MSWindowsFixedSizeDialogHint)
window.setWindowTitle("Randomix")
window.setWindowIcon(main_icon)
window.resize(234, 172)
window.setWindowOpacity(.94)  

# Шрифты
font = QtGui.QFont()
font.setPointSize(10)
font.setWeight(50)

# Кнопка "Сформировать"
active_button = QtWidgets.QPushButton("Сформировать", window)
active_button.setGeometry(110, 115, 115, 50)
active_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
active_button_icon = QtGui.QIcon()  # Иконка для кнопки "Сформировать"
active_button_icon.addPixmap(QtGui.QPixmap(".\Temp\icon.ico"),
                 QtGui.QIcon.Normal, QtGui.QIcon.Off)
active_button.setIcon(active_button_icon)
active_button.setIconSize(QtCore.QSize(24, 24)) # Размеры иконки
active_button.setToolTip("Сформировать случайный список песен")
active_button.clicked.connect(general_func)

# Кнопка "Отсюда"
src_button = QtWidgets.QPushButton("Отсюда", window)
src_button.setGeometry(10, 10, 100, 100)
src_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
src_button_icon = QtGui.QIcon()  # Иконка для кнопки "Отсюда"
src_button_icon.addPixmap(QtGui.QPixmap(".\Temp\src.ico"),
                 QtGui.QIcon.Normal, QtGui.QIcon.Off)
src_button.setIcon(src_button_icon)
src_button.setIconSize(QtCore.QSize(24, 24)) # Размеры иконки
src_button.setToolTip("Не выбрано")
src_button.clicked.connect(src_FileDialog)

# Кнопка "Сюда"
dst_button = QtWidgets.QPushButton("Сюда", window)
dst_button.setGeometry(120, 10, 100, 100)
dst_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
dst_button_icon = QtGui.QIcon()  # Иконка для кнопки "Cюда"
dst_button_icon.addPixmap(QtGui.QPixmap(".\Temp\dst.ico"),
                 QtGui.QIcon.Normal, QtGui.QIcon.On)
dst_button.setIcon(dst_button_icon)
dst_button.setIconSize(QtCore.QSize(24, 24)) # Размеры иконки
dst_button.setToolTip("Не выбрано")
dst_button.clicked.connect(dst_FileDialog)

# Надпись 
size_label = QtWidgets.QLabel(window)
size_label.setText("Количество, MB")
size_label.setGeometry(QtCore.QRect(16, 110, 81, 20))
size_label.setToolTip("Выставить ограничение на размер будущего плейлиста")

# Поле для ввода чисел
size_Box = QtWidgets.QSpinBox(window)
size_Box.setGeometry(QtCore.QRect(10, 130, 91, 31))
size_Box.setFont(font)
size_Box.setValue(15)
size_Box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
size_Box.setRange(5, 55000)
size_Box.setAlignment(QtCore.Qt.AlignRight|
                      QtCore.Qt.AlignTrailing|
                      QtCore.Qt.AlignVCenter)

# положение в центре экрана, отображение
desktop = QtWidgets.QApplication.desktop()
x = (desktop.width() - window.width()) // 2
y = (desktop.height() - window.height()) // 2
window.move(x, y)
window.show()
sys.exit(app.exec_())