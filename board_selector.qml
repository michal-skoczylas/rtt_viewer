import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: mainWindow
    width: 800
    height: 600
    visible: true
    title: qsTr("Wybór płytki")  // Poprawione qstr na qsTr
    Rectangle{
        id: background_rect
        color: "#e1f3f3f3"
        anchors.fill: parent

        // Główny layout - ColumnLayout jest lepszy niż zwykły Column
        ColumnLayout {
            anchors.fill: parent
            spacing: 10  // Zmniejszony spacing z 100

            // Pasek wyszukiwania (przeniesiony na górę)
            Rectangle {
                id: search_bar_rect
                color: background_rect.color
                Layout.fillWidth: true
                Layout.preferredHeight: 50

                TextField {
                    id: searchField
                    width: 792
                    height: 40
                    anchors.verticalCenter: parent.verticalCenter
                    placeholderText: "Szukaj płytki..."
                    font.pixelSize: 14
                    anchors.horizontalCenter: parent.horizontalCenter

                    background: Rectangle {
                        id: reeec
                        color: "#e3e0e0"
                        implicitWidth: 200
                        implicitHeight: 40
                        border.color: {
                            if (!searchField.enabled) return "#cccccc"
                            return searchField.activeFocus ? "#0066cc" : "#aaaaaa"
                        }
                        border.width: searchField.activeFocus ? 2 : 1
                        radius: 8
                    }

                    // Styl placeholder tekstu
                    placeholderTextColor: "#888888"

                    // Kolor zaznaczonego tekstu
                    selectionColor: "#0066cc80"  // Niebieski z przezroczystością

                }
            }

            // Główny kontener
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
                    color: "#f3f3f3"  // Poprawiony kolor (usunięto 'e1' przed hex)
                    radius: 10
                    border.color: "#dddddd"
                    border.width: 1

                    // Model powinien być zdefiniowany na poziomie Window/Item
                    ListView {
                        anchors.fill: parent
                        anchors.margins: 10
                        model: stmBoards
                        spacing: 5

                        delegate: Rectangle {
                            width: parent.width
                            height: 40
                            color: "#ffffff"
                            radius: 5

                            Text {
                                anchors.centerIn: parent
                                text: model.name
                            }
                        }
                    }
                }
            }

            // Przycisk wyboru (na dole)
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
            }

            ListModel {
                id: stmBoards
                ListElement { name: "STM123123" }
                ListElement { name: "XDDD" }
            }
        }

        // Model powinien być zdefiniowany tutaj, a nie wewnątrz Rectangle
    }

}

