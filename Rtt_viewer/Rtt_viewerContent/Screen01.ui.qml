/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls
import Rtt_viewer

Rectangle {
    id: rectangle
    width: 1500
    height: Constants.height
    color: "#d4d4d4"


    Button {
        id: button
        x: 207
        y: 822
        width: 319
        height: 80
        text: qsTr("Select file location")

        Connections {
            target: button
            function onClicked() { console.log("clicked") }
        }
    }

    TextField {
        id: textField
        x: 546
        y: 842
        width: 808
        height: 40
        placeholderText: qsTr("Text Field")
    }

    ProgressBar {
        id: progressBar
        x: 1106
        y: 619
        width: 500
        height: 12
        value: 0.5
        rotation: 90
    }

    Rectangle {
        id: fileList
        x: 546
        y: 145
        width: 798
        height: 691
        color: "#ffffff"

        ListView {
            id: listView
            anchors.fill: parent
            model: ListModel {
                ListElement {
                    name: "Red"
                    colorCode: "red"
                }

                ListElement {
                    name: "Green"
                    colorCode: "green"
                }

                ListElement {
                    name: "Blue"
                    colorCode: "blue"
                }

                ListElement {
                    name: "White"
                    colorCode: "white"
                }
            }
            delegate: Row {
                spacing: 5
                Rectangle {
                    width: 100
                    height: 20
                    color: colorCode
                }

                Text {
                    width: 100
                    text: name
                }
            }

            Rectangle {
                id: rectangle1
                width: 200
                height: 200
                color: "#9f1a1a"
            }

            Rectangle {
                id: rectangle2
                x: 0
                y: 201
                width: 200
                height: 200
                color: "#ffffff"
            }
        }
    }

    Rectangle {
        id: combo
        x: 197
        y: 145
        width: 317
        height: 55
        color: "#e0e0e0"
        radius: 19

        ComboBox {
            id: dir_ComboBox
            width: 295
            height: 40
            anchors.centerIn: parent
        }
    }
    states: [
        State {
            name: "clicked"
        }
    ]
}
