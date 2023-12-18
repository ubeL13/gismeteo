# -*- coding: utf-8 -*-
import sys
import sepparate, years, weeks, function, iterator
from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QToolTip,
    QPushButton,
    QApplication,
    QDesktopWidget,
    QFileDialog,
    QLabel,
    QMessageBox,
    QCalendarWidget,
)
from PyQt5.QtGui import QIcon, QFont


class YaCalendar(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 700, 500)

        self.UiComponents()

        self.show()

    def UiComponents(self):
        self.setWindowTitle("Find data")

        self.label = QLabel(self)
        self.label.adjustSize()
        self.label.move(450, 150)

        self.file_name = None
        self.target_date = None
        self.date = QLabel(self)
        self.temp_morning = QLabel(self)
        self.pres_morning = QLabel(self)
        self.wind_morning = QLabel(self)
        self.temp_evening = QLabel(self)
        self.pres_evening = QLabel(self)
        self.wind_evening = QLabel(self)

        btn1 = QPushButton("Выбрать файл", self)
        btn1.setToolTip(
            "Нажмите на кнопку для выбора csv файла."
        )
        btn1.clicked.connect(self.makeFileName)
        btn1.resize(btn1.sizeHint())
        btn1.move(450, 50)

        calendar = QCalendarWidget(self)
        calendar.setGridVisible(True)
        calendar.setGeometry(20, 20, 400, 400)
        calendar.clicked.connect(self.makeDate)

        value = calendar.selectedDate()

    def makeDate(self, value):
        data = str(value)[19:]
        data_list = data.split(",")
        year = data_list[0]
        mouth = data_list[1][1:]
        if len(mouth) == 1:
            mouth = "0" + mouth
        day = data_list[2][1:]
        day = day.replace(")", "")
        if len(day) == 1:
            day = "0" + day
        self.target_date = year + "-" + mouth + "-" + day
        self._find_date_from_file()

    def _find_date_from_file(self):
        if self.file_name:
            data = function.get_date_from_file(self.target_date, self.file_name)
            if data is not None:
                self.label.setText("Данные для переданной даты:")
                self.label.adjustSize()
                self.label.move(450, 120)
                self.print_dict(data)
            else:
                self.label.setText("Данных по переданной дате нет.")
                self.label.adjustSize()
                self.label.move(450, 120)
                self.date.setText("")
                self.temp_morning.setText("")
                self.pres_morning.setText("")
                self.wind_morning.setText("")
                self.temp_evening.setText("")
                self.pres_evening.setText("")
                self.wind_evening.setText("")
        else:
            reply = QMessageBox.question(
                self,
                "Сообщение",
                "Вы должны выбрать файл. Выбрать файл?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
                )
            if reply == QMessageBox.Yes:
                self.makeFileName()
            else:
                return

    def makeFileName(self):
        """Get file from directory"""
        folderpath = QFileDialog.getExistingDirectory(self, "Выберете папку")
        file = QFileDialog.getOpenFileName(
            self, "Выберете файл", folderpath, "CSV File (*.csv)"
        )
        self.file_name = file[0]

    def print_dict(self, dictionary):
        """Print thr dict"""
        dictionary_values = []
        for i, j in dictionary.items():
            dictionary_values.append(j.encode("WINDOWS_1251"))
        self.date.setText("Дата: " + dictionary_values[0].decode("UTF-8"))
        self.date.adjustSize()
        self.date.move(450, 150)
        self.temp_morning.setText(
            "Температура днем: " + dictionary_values[1].decode("UTF-8")
        )
        self.temp_morning.adjustSize()
        self.temp_morning.move(450, 180)
        self.pres_morning.setText(
            "Давление днем: " + dictionary_values[2].decode("UTF-8")
        )
        self.pres_morning.adjustSize()
        self.pres_morning.move(450, 210)
        self.wind_morning.setText("Ветер днем: " + dictionary_values[3].decode("UTF-8"))
        self.wind_morning.adjustSize()
        self.wind_morning.move(450, 240)
        self.temp_evening.setText(
            "Температура вечером: " + dictionary_values[4].decode("UTF-8")
        )
        self.temp_evening.adjustSize()
        self.temp_evening.move(450, 270)
        self.pres_evening.setText(
            "Давление вечером: " + dictionary_values[5].decode("UTF-8")
        )
        self.pres_evening.adjustSize()
        self.pres_evening.move(450, 300)
        self.wind_evening.setText(
            "Ветер вечером: " + dictionary_values[6].decode("UTF-8")
        )
        self.wind_evening.adjustSize()
        self.wind_evening.move(450, 330)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self._iterator = None
        QToolTip.setFont(QFont("SansSerif", 14))

        self.calendar = None

        self.setToolTip("Это <b>QWidget</b> виджет")
        self.label = QLabel(self)
        self.label.setText("")
        self.label.adjustSize()
        self.label.move(150, 50)

        self.date = QLabel(self)
        self.temp_morning = QLabel(self)
        self.pres_morning = QLabel(self)
        self.wind_morning = QLabel(self)
        self.temp_evening = QLabel(self)
        self.pres_evening = QLabel(self)
        self.wind_evening = QLabel(self)

        btn1 = QPushButton("X и Y", self)
        btn1.setToolTip(
            "Нажмите на кнопку для разделения исходного файла на два файла с датами и с метеоданными."
        )
        btn1.clicked.connect(self._divide_on_two)
        btn1.resize(btn1.sizeHint())
        btn1.move(50, 10)

        btn2 = QPushButton("Разделить по годам", self)
        btn2.setToolTip(
            "Нажмите на кнопку для разделения исходного датасета на файлы с данными по годам."
        )
        btn2.clicked.connect(self._divide_by_years)
        btn2.resize(btn2.sizeHint())
        btn2.move(250, 10)

        btn3 = QPushButton("Разделить по неделям", self)
        btn3.setToolTip(
            "Нажмите на кнопку для разделения исходного датасета на файлы с данными по неделям."
        )
        btn3.clicked.connect(self._divide_by_week)
        btn3.resize(btn3.sizeHint())
        btn3.move(50, 50)

        btn4 = QPushButton("Получить данные", self)
        btn4.setToolTip(
            "Нажмите на кнопку для получения данных из файла по переданной дате."
        )
        btn4.clicked.connect(self.show_new_window)
        btn4.resize(btn4.sizeHint())
        btn4.move(250, 50)

        btn5 = QPushButton("Создать итератор", self)
        btn5.setToolTip("Нажмите на кнопку для создания итератора для файла.")
        btn5.clicked.connect(self.create_iterator)
        btn5.resize(btn5.sizeHint())
        btn5.move(50, 100)

        btn6 = QPushButton("Получить следущие данные", self)
        btn6.setToolTip(
            "Нажмите на кнопку для получения данных по следущей дате из файла."
        )
        btn6.clicked.connect(self._window_next)
        btn6.resize(btn6.sizeHint())
        btn6.move(250, 100)

        qbtn = QPushButton("Выход", self)
        qbtn.setToolTip("Нажмите для кнопки для выхода.")
        qbtn.clicked.connect(self._quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(350, 400)
        self.resize(450, 450)
        self.center()
        self.setWindowTitle("app")
        self.setWindowIcon(QIcon("web.png"))

        self.show()

    def center(self):
        """Move the window to the center. Return None"""
        location = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        location.moveCenter(center)
        self.move(location.topLeft())

    def _divide_on_two(self):
        """Divides the source file into two new ones. The first contains only dates, the second only weather data. Return None"""
        csv_file = self.get_file()
        sepparate.divide_on_x_y(csv_file)

    def _divide_by_years(self):
        """Divide the source csv_file by years. Return None"""
        csv_file = self.get_file()
        years.divide_by_years(csv_file)

    def _divide_by_week(self):
        """Divide list by weeks and create the csv_files. Return None."""
        csv_file = self.get_file()
        weeks.divide_by_week(csv_file)

    def show_new_window(self, checked):
        if self.calendar is None:
            self.calendar = YaCalendar()
            self.calendar.show()
        else:
            self.calendar = None

    def closeEvent(self, event):
        """Get MessageBox for exit"""
        reply = QMessageBox.question(
            self,
            "Сообщение",
            "Вы уверены, что хотите выйти?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def create_iterator(self):
        """Create the iterator for csv_file"""
        csv_file = self.get_file()
        self._iterator = iterator.Iterator(csv_file)

    def _window_next(self):
        """Get the next date in file"""
        if self._iterator is not None:
            try:
                next_data = self._iterator.__next__()
                self.label.setText("Следущие данные в файле:")
                self.label.adjustSize()
                self.label.move(100, 150)
                self.print_dict(next_data)
            except Exception:
                self.label.setText("Данные закончились.")
                self.label.adjustSize()
                self.label.move(200, 50)
                self.date.setText("")
                self.temp_morning.setText("")
                self.pres_morning.setText("")
                self.wind_morning.setText("")
                self.temp_evening.setText("")
                self.pres_evening.setText("")
                self.wind_evening.setText("")

        else:
            reply = QMessageBox.question(
                self,
                "Сообщение",
                "Вы должны создать итератор для файла! Создать итератор?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.create_iterator()
            else:
                return

    def get_file(self):
        """Get file from directory"""
        folderpath = QFileDialog.getExistingDirectory(self, "Выберете папку")
        file_name = QFileDialog.getOpenFileName(
            self, "Выберете файл", folderpath, "CSV File (*.csv)"
        )
        return file_name[0]

    def print_dict(self, dictionary):
        """Print thr dict"""
        dictionary_values = []
        for i, j in dictionary.items():
            dictionary_values.append(j.encode("WINDOWS_1251"))
        self.date.setText("Дата: " + dictionary_values[0].decode("UTF-8"))
        self.date.adjustSize()
        self.date.move(10, 200)
        self.temp_morning.setText(
            "Температура днем: " + dictionary_values[1].decode("UTF-8")
        )
        self.temp_morning.adjustSize()
        self.temp_morning.move(150, 200)
        self.pres_morning.setText(
            "Давление днем: " + dictionary_values[2].decode("UTF-8")
        )
        self.pres_morning.adjustSize()
        self.pres_morning.move(150, 170)
        self.wind_morning.setText("Ветер днем: " + dictionary_values[3].decode("UTF-8"))
        self.wind_morning.adjustSize()
        self.wind_morning.move(450, 450)
        self.temp_evening.setText(
            "Температура вечером: " + dictionary_values[4].decode("UTF-8")
        )
        self.temp_evening.adjustSize()
        self.temp_evening.move(450, 450)
        self.pres_evening.setText(
            "Давление вечером: " + dictionary_values[5].decode("UTF-8")
        )
        self.pres_evening.adjustSize()
        self.pres_evening.move(150, 230)
        self.wind_evening.setText(
            "Ветер вечером: " + dictionary_values[6].decode("UTF-8")
        )
        self.wind_evening.adjustSize()
        self.wind_evening.move(150, 260)

    def _quit(self):
        """Get MessageBox for exit"""
        reply = QMessageBox.question(
            self,
            "Сообщение",
            "Вы уверены, что хотите выйти?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()
        else:
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ex = Example()
    window = Window()
    sys.exit(app.exec_())
