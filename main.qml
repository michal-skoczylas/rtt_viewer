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
            y: 50
            text: qsTr("Load Directories")
            onClicked: rttHandler.fill_combobox()
        }

        C        ComboBox {
            id: dir_comboBox
            x: 73
            y: 100
            width: 200
            model: []
            onCurrentIndexChanged: {
                if (currentIndex >= 0) {
                    console.log("Selected directory:", currentText)
                    var contents = rttHandler.get_folder_contents(currentText)
                    subDirComboBox.model = contents
                    console.log("Subdirectory contents:", contents)
                }
            }
        }

        ComboBox {
            id: subDirComboBox
            x: 300
            y: 100
            width: 200
            model: []
        }

        Connections {
            target: rttHandler
            function onDataReady(data) {
                console.log("Received data for ComboBox:", data)
                dir_comboBox.model = data
            }
        }
    }
}