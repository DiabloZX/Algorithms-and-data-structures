from PyQt5 import QtWidgets, QtCore


class TrackWidget:
    def __init__(self, track_name, track_time, free_space):
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
        widgetlabel_2 = QtWidgets.QLabel(track_time)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widgetlabel_2.sizePolicy().hasHeightForWidth())
        widgetlabel_2.setSizePolicy(sizePolicy)
        widgetlabel_2.setStyleSheet("border:none;\n"
                                    "font: 63 12pt \"Segoe UI Semibold\";\n"
                                    "color: rgb(255, 255, 255);")
        widgetlabel_2.setMinimumSize(QtCore.QSize(60, 60))
        widgetlabel_2.setScaledContents(True)
        widgetlabel_2.setAlignment(QtCore.Qt.AlignCenter)
        widgetlabel_2.setWordWrap(True)
        widgetlabel_2.setObjectName("label_2")
        widgethorizontalLayout.addWidget(widgetlabel_2)

        widgethorizontalLayout.setStretch(0, 10)
        widgethorizontalLayout.setStretch(1, 1)
        self.widget.setLayout(widgethorizontalLayout)
        self.widget.setStyleSheet("border:none;\n"
                                  "background-color: rgba(255, 255, 255, 0);")
