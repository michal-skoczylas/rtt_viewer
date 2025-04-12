import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 800
    height: 600
    visible: true
    title: "RTT Viewer with Directory Tree"

    Rectangle {
        id: background
        x: 0
        y: 0
        width: 800
        height: 600
        color: "#e1f3f3f3"

        Connections {
            target: rttHandler
            function onDataReady(data) {
                console.log("Received data for ComboBox:", data)
                dir_comboBox.model = data
            }
        }

        Rectangle {
            id: listView_background
            x: 371
            y: 79
            width: 355
            height: 414
            color: "#c0bfbc"
            radius: 10

            ListView {
                id: fileListView
                anchors.fill: parent
                model: rttHandler.get_folder_contents(dir_comboBox.currentText)
                delegate: Item {
                    width: fileListView.width
                    height: 40

                    Rectangle {
                        width: parent.width
                        height: parent.height
                        color: "lightgray"
                        border.color: "black"

                        Text {
                            anchors.centerIn: parent
                            text: modelData
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onDoubleClicked: {
                            console.log("Selected file:", modelData)
                            // Tutaj możesz obsłużyć wybranie pliku
                        }
                    }
                }
            }
        }

        Rectangle {
            id: file_background
            x: 64
            y: 79
            width: 232
            height: 200
            color: "#c0bfbc"
            radius: 10

            Flow {
                id: _flow
                anchors.fill: parent
                anchors.leftMargin: 10
                anchors.rightMargin: 10
                anchors.topMargin: 10
                spacing: 10

                Button {
                    id: dir_button
                    text: qsTr("Load Directories")
                    onClicked: rttHandler.fill_combobox()
                }

                Button {
                    id: savePath_button
                    width: 85
                    text: qsTr("Select Path")
                    highlighted: false
                    flat: false
                }

                ComboBox {
                    id: dir_comboBox
                    width: 216
                    height: 24
                    model: []
                }

            }
        }
    }
}
