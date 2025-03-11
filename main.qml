import QtQuick
import QtQuick.Window
import QtQuick.Controls 2.15

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("RTT Viewer")

    Rectangle {
        id: rectangle
        x: 29
        y: 22
        width: 430
        height: 423
        color: "#b3acac"

        TextEdit {
            id: rtt_input
            text: qsTr("Text Edit")
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
            x: 11
            y: 16
            width: 375
            text: qsTr("Connect")
            anchors.left: rtt_output.right
            anchors.right: rtt_output.left
            anchors.top: rtt_output.bottom
            anchors.bottom: rtt_output.top
            anchors.leftMargin: -357
            anchors.rightMargin: 8
            anchors.topMargin: -317
            anchors.bottomMargin: 38
            anchors.horizontalCenter: rtt_output.horizontalCenter

            Connections {
                target: rtt_connect_button
                onClicked: {
                    rttHandler.read_rtt()
                }
            }
        }
    }

    ComboBox {
        id: comboBox
               x: 434
               y: 44
               width: 200
               model: rttHandler.get_usb_devices()

               // // Dostosowanie popup
               // popup: Popup {
               //     width: 300  // Szerokość rozwijanej listy
               //     y: comboBox.height  // Pozycja Y poniżej ComboBox
               //     parent: Overlay.overlay  // Ustaw rodzica na Overlay, aby mógł wystawać poza okno

               //     contentItem: ListView {
               //         implicitHeight: contentHeight
               //         model: comboBox.popup.visible ? comboBox.delegateModel : null
               //         currentIndex: comboBox.highlightedIndex

               //         delegate: ItemDelegate {
               //             width: comboBox.popup.width
               //             text: modelData
               //             highlighted: comboBox.highlightedIndex === index
               //             onClicked: {
               //                 comboBox.currentIndex = index
               //                 comboBox.popup.close()
               //             }
               //         }
               //     }
               // }
    }
}
