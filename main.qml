import QtQuick
import QtQuick.Window
import QtQuick.Controls 2.15

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")

    Button {
        id: rtt_connect_button
        x: 40
        y: 38
        text: qsTr("Connect")

        Connections {
            target: rtt_connect_button
            onClicked: {
                rttHandler.read_rtt()
            }
        }
    }

    TextEdit {
        id: rtt_output
           x: 128
           y: 102
           width: 338
           height: 253
           text: rttHandler.received_data
           readOnly: true
           wrapMode: TextEdit.Wrap
           font.pixelSize: 12
    }
}
