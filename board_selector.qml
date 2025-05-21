import QtQuick 2.15
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: mainWindow
    width: 800
    height: 600
    visible: true
    title: qsTr("Wybór płytki")

    property string selectedBoard: ""  

    Rectangle{
        id: background_rect
        color: "#e1f3f3f3"
        anchors.fill: parent

        ColumnLayout {
            anchors.fill: parent
            spacing: 10

            // ... search bar i inne elementy ...

            Rectangle {
                id: background_rectangle
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: background_rect.color

                Rectangle {
                    id: mainContainer
                    anchors.centerIn: parent
                    width: Math.min(parent.width * 0.9, 700)
                    height: Math.min(parent.height * 0.9, 500)
                    color: "#f3f3f3"
                    radius: 10
                    border.color: "#dddddd"
                    border.width: 1

                    ListView {
                        id: boardListView
                        anchors.fill: parent
                        anchors.margins: 10
                        model: stmBoards
                        spacing: 5

                        delegate: Rectangle {
                            width: parent.width
                            height: 40
                            color: ListView.isCurrentItem ? "#b3e5fc" : "#ffffff"
                            radius: 5

                            Text {
                                anchors.centerIn: parent
                                text: model.name
                            }

                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    boardListView.currentIndex = index
                                    mainWindow.selectedBoard = model.name
                                }
                            }
                        }
                    }
                }
            }

            Button {
                id: select_button
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 200
                Layout.preferredHeight: 50
                text: qsTr("Wybierz płytkę")

                background: Rectangle {
                    color: "#d3d3d3"
                    radius: 8
                }
                onClicked: {
                    if (mainWindow.selectedBoard !== "") {
                        console.log("Wybrana płytka:", mainWindow.selectedBoard)
                        // Możesz tu wywołać slot w Pythonie, np.:
                        // boardSelector.select_board(mainWindow.selectedBoard)
                        windowManager.create_new_window()
                    } else {
                        console.log("Nie wybrano płytki!")
                    }
                }
            }

            ListModel {
                id: stmBoards
                ListElement { name: "STM32F413ZH" }
                ListElement { name: "INNA" }
                ListElement { name: "STM32F103C8" }
            }
        }
    }
}