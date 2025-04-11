import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 800
    height: 600
    visible: true
    title: "RTT Viewer with Directory Tree"

    Rectangle {
        id: rectangle
        x: 0
        y: 0
        width: 800
        height: 600
        color: "#6b5f5f"

        Button {
            id: dir_button
            x: 73
            y: 118
            text: qsTr("Button")
            onClicked: rttHandler.fill_combobox()
        }

        ComboBox {
            id: dir_comboBox
            x: 348
            y: 120
            model: []
            Connections{
                target: rttHandler
                function onDataReady(data){
                console.log("Received data for ComboBox:", data)

                    dir_comboBox.model=data
                }

            }
            }
        }
    }

