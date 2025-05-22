import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts
import QtQuick.Controls.Fusion
Window {
    id: mainWindow
    width: 800
    height: 600
    visible: true
    title: qsTr("Wybór płytki")

    Rectangle {
        id: background_rect
        color: "#e1f3f3f3"
        anchors.fill: parent

        ColumnLayout {
            anchors.fill: parent
            spacing: 10

            // Lista płytek
            Rectangle {
                id: mainContainer
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "#f3f3f3"
                radius: 10
                border.color: "#dddddd"
                border.width: 1

                ListView {
                    id: listView
                    anchors.fill: parent
                    anchors.margins: 10
                    model: stmBoards
                    spacing: 5

                    delegate: Rectangle {
                        width: parent.width
                        height: 40
                        radius: 5
                        color: model.isSelected ? "#d3d3d3" : "#ffffff"  // Zmiana koloru po zaznaczeniu

                        Text {
                            anchors.centerIn: parent
                            text: model.name
                        }

                        MouseArea {
                            id: mouseArea
                            anchors.fill: parent
                            onClicked: {
                                // Zaznacz element
                                for (let i = 0; i < stmBoards.count; i++) {
                                    stmBoards.setProperty(i, "isSelected", false);
                                }
                                stmBoards.setProperty(index, "isSelected", true);
                            }
                            onDoubleClicked: {
                                // Wyślij sygnał po dwukrotnym kliknięciu
                                boardHandler.select_board(model.name);
                            }
                        }
                    }
                }
            }

            // Przycisk wyboru
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
                    // Wyślij sygnał dla zaznaczonego elementu
                    for (let i = 0; i < stmBoards.count; i++) {
                        if (stmBoards.get(i).isSelected) {
                            boardHandler.select_board(stmBoards.get(i).name);
                            break;
                        }
                    }
                }
            }

            ListModel {
                id: stmBoards
                ListElement { name: "STM123123"; isSelected: false }
                ListElement { name: "XDDD"; isSelected: false }
            }
        }
    }
}