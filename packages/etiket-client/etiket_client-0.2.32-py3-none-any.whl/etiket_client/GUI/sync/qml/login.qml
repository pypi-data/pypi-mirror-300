import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Controls.Material 2.12

Item {

    TextField {
        id: usernameInput
        width: parent.width * 0.8
        placeholderText: "username"
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 45
        selectByMouse: true
    }

    TextField {
        id: passwordInput
        width: parent.width * 0.8
        placeholderText: "Password"
        anchors.top: usernameInput.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 10
        echoMode: TextInput.Password
        selectByMouse: true
        KeyNavigation.tab : loginBotton
        Keys.onReturnPressed: loginBotton.clicked()
    }

    Text {
        id: institutionDescription
        text: "Please select your institution:"
        anchors.top: passwordInput.bottom
        anchors.topMargin: 30
        font.pixelSize: 14
        x : parent.width * 0.1
        color: "#D3D3D3"
    }

    ComboBox {
        id: institutionComboBox
        width: parent.width * 0.8
        anchors.top: institutionDescription.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 7
        model: loginMgr.institutions
        currentIndex: 0
    }



    Text {
        anchors.top: institutionComboBox.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 50
        
        id: errorLogIn
        visible : false
        color: Material.color(Material.Red, Material.Shade300)
        font.pixelSize: 12
        text: "Username or password is incorrect, please try again."
        Layout.preferredHeight: 100
        
        SequentialAnimation {
            id : errorLogInAnimation
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: 10; duration: 60 }
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: -10; duration: 60 }
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: 10; duration: 60 }
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: -10; duration: 60 }
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: 0; duration: 30 }
        }
    }

    Button {
        id : loginBotton
        text: "Login"
        width: parent.width * 0.4
        anchors.top: errorLogIn.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 20

        Material.accent: Material.BlueGrey

        function login() {
            errorLogIn.visible = false;
            var state = loginMgr.login(usernameInput.text, passwordInput.text, institutionComboBox.currentText);
            errorLogIn.visible = !state;
            errorLogInAnimation.restart();
        }

        onClicked: loginBotton.login()
        Keys.onReturnPressed: loginBotton.login()
        Keys.onEnterPressed: loginBotton.login()
    }

    Text {
        anchors.top: loginBotton.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 30

        text: "Click here if you don't have an account."
        font.pixelSize: 12
        color: "white"
    }
}