import QtQuick
import QtQuick.Controls
import QtQuick.Layouts 2.15

Window{
    id: mainWindow
    width: 800
    height: 600
    visible: true
    title: qstr("Wybór płytki")

    Rectangle {
        id: background_rectangle
        color: "#e3e0e0"
        anchors.fill: parent
        ListModel{
            id: stmBoards
            ListElement {name:"STM123123"}
            ListElement{name:"XDDD"}

        }
        Rectangle{
            id: mainContainer
            anchors.centerIn: parent
            width: Math.min(parent.width *0.9,700)
            height: Math.min(parent.height *0.9,500)
            color: "#e1f3f3f3"
            radius: 10
            border.color: "#dddddd"
            border.width: 1
        }


    }

}
