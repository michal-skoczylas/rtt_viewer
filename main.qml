import QtQuick
import QtQuick.Window
import QtQuick.Controls 2.15

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("RTT Viewer")

    Button {
        id: rtt_connect_button
        y: 38
        text: qsTr("Connect")
        anchors.left: rtt_output.right
        anchors.right: rtt_output.left
        anchors.top: rtt_output.bottom
        anchors.bottom: rtt_output.top
        anchors.leftMargin: -426
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
