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
                            var message = rttHandler.construct_message(dir_comboBox.currentText, modelData)
                            rttHandler.send_message(message)
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
                    onClicked:{
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
                        if (dir_comboBox.currentText !== "" && fileListView.currentIndex >=0){
                            var selectedFile = fileListView.model[fileListView.currentIndex];
                            console.log("Selected folder:",dir_comboBox.currentText);
                            console.log("Selected file: ", selectedFile);
                            rttHandler.process_selected_items(dir_comboBox.currentText, selectedFile);
                        }else{
                            console.log("No folder or file selected");
                        }
            }
        }

        Button {
            id: rtt_conn_button
            x: 597
            y: 22
            text: qsTr("connect to rtt")
            onClicked: {
                rttHandler.send_file_list_message();
            }
        }
    }
}
