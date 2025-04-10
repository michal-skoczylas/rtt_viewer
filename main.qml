import QtQuick
import QtQuick.Window
import QtQuick.Controls 2.15
import QtQuick.Dialogs

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("RTT Viewer")

    Rectangle {
        id: bckg
        x: 29
        y: 22
        width: 430
        height: 423
        color: "#b3acac"

        TextEdit {
            id: rtt_input
            text: qsTr("")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: rtt_output.bottom
            anchors.bottom: parent.bottom
            anchors.topMargin: 41
            anchors.bottomMargin: 20
            font.pixelSize: 12
        }

        TextEdit {
            id: rtt_output
            x: 46
            y: 85
            width: 338
            height: 253
            text: rttHandler.received_data
            readOnly: true
            wrapMode: TextEdit.Wrap
            font.pixelSize: 12
        }

        Button {
            id: rtt_connect_button
            y: 16
            width: 375
            text: qsTr("Connect")

            Connections {
                target: rtt_connect_button
                onClicked: {
                    rttHandler.read_rtt()
                }
            }
        }
    }

    Button {
        id: button
        x: 472
        y: 51
        text: qsTr("send")

        Connections {
            target: button
            onClicked: {rttHandler.send_hejka()}
        }
    }

    Button {
        id: path_button
        x: 472
        y: 104
        text: qsTr("path")
        onClicked: fileDialog.open()
    }
    FileDialog {
                id: fileDialog
                title: "Save Response"

                onAccepted: {
                    rttHandler.set_save_path(fileDialog.fileUrl.toString().replace("file://", ""))
                }
    }

            Rectangle {
                id: background
                x: 0
                y: 0
                width: 640
                height: 480
                color: "#e3e0e0"

                Button {
                    id: get_files_combobox
                    x: 40
                    y: 74
                    text: qsTr("Button")
                }

                ComboBox {
                    id: dir_comboBox
                    x: 195
                    y: 76
                }
            }

    // ComboBox {
    //     id: comboBox
    //            x: 434
    //            y: 44
    //            width: 200
    //            model: rttHandler.get_usb_devices()

    //            // // Dostosowanie popup
    //            // popup: Popup {
    //            //     width: 300  // Szerokość rozwijanej listy
    //            //     y: comboBox.height  // Pozycja Y poniżej ComboBox
    //            //     parent: Overlay.overlay  // Ustaw rodzica na Overlay, aby mógł wystawać poza okno

    //            //     contentItem: ListView {
    //            //         implicitHeight: contentHeight
    //            //         model: comboBox.popup.visible ? comboBox.delegateModel : null
    //            //         currentIndex: comboBox.highlightedIndex

    //            //         delegate: ItemDelegate {
    //            //             width: comboBox.popup.width
    //            //             text: modelData
    //            //             highlighted: comboBox.highlightedIndex === index
    //            //             onClicked: {
    //            //                 comboBox.currentIndex = index
    //            //                 comboBox.popup.close()
    //            //             }
    //            //         }
    //            //     }
    //            // }
    // }
}
