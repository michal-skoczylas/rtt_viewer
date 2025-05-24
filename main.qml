import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: window
    width: 800
    height: 600
    visible: true
    title: "RTT Viewer with Directory Tree"

    Rectangle {
        id: background
        anchors.fill: parent
        color: "#f3f3f3" // jasne tło

        Connections {
            target: rttHandler
            function onDataReady(data) {
                dir_comboBox.model = data
            }
        }
        Connections{
            target: rttHandler
            function onProgressChanged(value){
                fileProgressBar.value = value
            }
        }
                property string selectedSavePath: ""
        
        Connections {
            target: fileHandler
            function onSavePathSelected(path) {
                selectedSavePath = path
                console.log("Wybrana ścieżka do zapisu:", path)
            }
        }

        Rectangle {
            id: listView_background
            x: 371
            y: 79
            width: 355
            height: 414
            color: "#e0e0e0"
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
                        color: "#f9f9f9"
                        border.color: "#b0b0b0"

                        Text {
                            anchors.centerIn: parent
                            text: modelData
                            color: "black"
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onDoubleClicked: {
                         if (
            dir_comboBox.currentText !== "" &&
            modelData !== "" &&
            selectedSavePath !== ""
        ) {
            rttHandler.download_file(dir_comboBox.currentText, modelData, selectedSavePath)
        } else {
            console.log("No folder, file or save path selected");
        }
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
            color: "#e0e0e0"
            radius: 10

            Flow {
                anchors.fill: parent
                anchors.margins: 10
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
                    onClicked: {
                        var path = fileHandler.select_save_path()
                        if (path !==""){
                            console.log("Selected save path: ", path)
                        }
                    }
                }

                ComboBox {
                    id: dir_comboBox
                    width: 216
                    height: 24
                    model: []
                }
            }
        }

        Button {
            id: save_button
            x: 64
            y: 521
            text: qsTr("Button")
            onClicked:{
                if (dir_comboBox.currentText !== "" && fileListView.currentIndex >= 0 && selectedSavePath !== "") {
                    var selectedFile = fileListView.model[fileListView.currentIndex];
                    rttHandler.download_file(dir_comboBox.currentText, selectedFile, selectedSavePath)
                }else{
                    console.log("No folder or file selected");
                }
            }
        }

        Button {
            id: rtt_conn_button
            x: 597
            y: 22
            text: qsTr("super")
            onClicked: {
                rttHandler.send_file_list_message();
            }
        }

        Button {
            id: select_board_button
            x: 64
            y: 566
            text: qsTr("Select board")
            onClicked: {
                appManager.show_board_selector_from_main()
            }
        }
                // ...przyciski...
        
               ProgressBar {
            id: fileProgressBar
            width: 400
            height: 24
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 20
            from: 0
            to: 1
            value: 0
            visible: value > 0 && value < 1
        
            contentItem: Rectangle {
                anchors.fill: parent
                color: "#e0e0e0" // tło paska
                radius: 12
        
                Rectangle {
                    width: parent.width * fileProgressBar.position
                    height: parent.height
                    color: "limegreen" // kolor wypełnienia
                    radius: 12
                }
            }
        } 
    }
}
