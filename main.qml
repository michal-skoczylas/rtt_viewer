import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: window
    width: 800
    height: 600
    visible: true
    title: "RTT Viewer with Directory Tree"

    property string selectedSavePath: "" // <-- przeniesione na poziom Window

    // --- Główne tło aplikacji ---
    Rectangle {
        id: background
        anchors.fill: parent
        color: "#f3f3f3" // jasne tło

        // --- SYGNAŁY Z PYTHONA ---
        Connections {
            target: rttHandler
            function onDataReady(data) {
                dir_comboBox.model = data
            }
        }
        Connections {
            target: rttHandler
            function onProgressChanged(value){
                fileProgressBar.value = value
            }
        }
        Connections {
            target: fileHandler
            function onSavePathSelected(path) {
                window.selectedSavePath = path
                console.log("Wybrana ścieżka do zapisu:", path)
            }
        }

        // --- LISTA PLIKÓW ---
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
                // Warunek na istnienie handlera!
                model: rttHandler ? rttHandler.get_folder_contents(dir_comboBox.currentText) : []
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
                                window.selectedSavePath !== ""
                            ) {
                                rttHandler.download_file(dir_comboBox.currentText, modelData, window.selectedSavePath)
                            } else {
                                console.log("No folder, file or save path selected");
                            }
                        }
                    }
                }
            }
        }

        // --- PANEL Z PRZYCISKAMI I WYBOREM KATALOGU ---
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
                        fileHandler.select_save_path()
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

        // --- PRZYCISK POBIERANIA PLIKU ---
        Button {
            id: save_button
            x: 64
            y: 521
            text: qsTr("Download")
            onClicked:{
                if (dir_comboBox.currentText !== "" && fileListView.currentIndex >= 0 && window.selectedSavePath !== "") {
                    var selectedFile = fileListView.model[fileListView.currentIndex];
                    rttHandler.download_file(dir_comboBox.currentText, selectedFile, window.selectedSavePath)
                }else{
                    console.log("No folder or file selected");
                }
            }
        }

        // --- PRZYCISK ODSWIEŻENIA LISTY PLIKÓW NA PŁYTCE ---
        Button {
            id: rtt_conn_button
            x: 597
            y: 22
            text: qsTr("Refresh file list")
            onClicked: {
                rttHandler.send_file_list_message();
            }
        }

        // --- PRZYCISK POWROTU DO WYBORU PŁYTKI ---
        Button {
            id: select_board_button
            x: 64
            y: 566
            text: qsTr("Select board")
            onClicked: {
                appManager.show_board_selector_from_main()
            }
        }

        // --- PASEK POSTĘPU POBIERANIA ---
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
                color: "#e0e0e0"
                radius: 12

                Rectangle {
                    width: parent.width * fileProgressBar.position
                    height: parent.height
                    color: "limegreen"
                    radius: 12
                }
            }
        }
    }
}