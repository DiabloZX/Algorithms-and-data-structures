from PyQt5 import QtWidgets, QtCore


class CurrentTrackWidget:
    def __init__(self, track_name, free_space):
        self.widget = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(426, 60))

        widgethorizontalLayout = QtWidgets.QHBoxLayout()
        widgethorizontalLayout.setContentsMargins(10, 0, 15, 0)
        widgethorizontalLayout.setSpacing(10)
        widgethorizontalLayout.setObjectName("horizontalLayout")

        if len(track_name) > free_space:
            track_name = track_name[:int(free_space)] + "..."

        widgetlabel = QtWidgets.QLabel(track_name)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widgetlabel.sizePolicy().hasHeightForWidth())
        widgetlabel.setSizePolicy(sizePolicy)
        widgetlabel.setStyleSheet("border:none;\n"
                                  "font: 63 16pt \"Segoe UI Semibold\";\n"
                                  "color: rgb(255, 255, 255);")
        widgetlabel.setMinimumSize(QtCore.QSize(0, 60))
        widgetlabel.setObjectName("label")
        widgethorizontalLayout.addWidget(widgetlabel)

        pushButton = QtWidgets.QPushButton()
        pushButton.setMinimumSize(QtCore.QSize(50, 50))
        pushButton.setStyleSheet("QPushButton{\n"
                                 "    border: none;\n"
                                 "    font: 63 25pt \"Segoe UI Semibold\";\n"
                                 "    color: rgb(255, 255, 255);\n"
                                 "}")
        pushButton.setObjectName("pushButton")
        pushButton.setText("▶")
        widgethorizontalLayout.addWidget(pushButton)

        widgethorizontalLayout.setStretch(0, 10)
        widgethorizontalLayout.setStretch(1, 1)
        self.widget.setLayout(widgethorizontalLayout)
        self.widget.setStyleSheet("border:none;\n"
                                  "background-color: rgba(255, 255, 255, 0);")
