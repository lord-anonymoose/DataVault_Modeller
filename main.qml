import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

ApplicationWindow {
    id: mainWindow
    width: 700
    height: 180
    visible: true
    SystemPalette { id: myPalette; colorGroup: SystemPalette.Active }
    property color system_text_color: myPalette.text
    property int emptyFields: 0

    function callError (title, text) {
        errorMessage.title = title
        errorMessage.text = text
        errorMessage.open()
        logText.text = " "
    }

    function checkEmpty () {
        emptyFields = 0
        if (ldmText.text === "") {
            callError("Error!", "No file for Logical Data Model selected. Choose a file and try again, please.")
            emptyFields += 1
        }
        if (stText.text === "") {
            callError("Error!", "No file for Modelling Standards selected. Choose a file and try again, please.")
            emptyFields += 1
        }
        if (outputText.text === "") {
            callError("Error!", "No path for Output folder selected. Choose a folder and try again, please.")
            emptyFields += 1
        }
    }

    Column {
        // Logical Data Model Picker
        Row {
            Button {
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("Choose Model...")
                onClicked: ldmFileDialog.open()
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                id: ldmText
                color: system_text_color
                width: 500
            }
        }

        // Modelling Standard picker
        Row {
            Button {
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("Choose Standards...")
                onClicked: stDialog.open()
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                id: stText
                color: system_text_color
                width: 500
            }
        }

        // Output path picker
        Row {
            Button {
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("Choose Folder...")
                onClicked: outputDialog.open()
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                id: outputText
                color: system_text_color
                width: 500
            }
        }

        // Action buttons
        Row {
            // Model check
            anchors.horizontalCenter: parent.horizontalCenter
            Button {
                objectName: "checkButton"
                id: modelCheck
                text: qsTr("Check model")
                onClicked: {
                    checkEmpty()
                    if (emptyFields === 0) {
                        backend.checkModel(ldmText.text, outputText.text)
                        logText.text = "Successfully checked model! See the results in an output file"
                    }
                }
            }

            // DDL Generator
            Button {
                text: qsTr("Generate Database")
                onClicked: {
                    checkEmpty()
                    if (emptyFields === 0) {
                        backend.generateDatabase(ldmText.text, outputText.text)
                        logText.text = "Generated DDLs based on the model! See the results in an output file"
                    }
                }
             }
        }

        // Logging results
        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            Text {
                id: logText
                text: " "
                color: "green"
                height: 30
            }
        }

        //Copyright
        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            Text {
                id: copyrightText
                text: "Philipp Lazarev, 2023 ©"
                color: system_text_color
            }
        }
    }

    // Logical Data Model picker dialog
    FileDialog {
        id: ldmFileDialog
        currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)
        nameFilters: ["*.xlsx", "*.xlsm", "*.xltx", "*.xltm"]
        onAccepted: {
            var path = selectedFile.toString()
            path = path.replace(/^(file:\/{2})/,"");
            var cleanPath = decodeURIComponent(path);
            ldmText.text = cleanPath
        }
    }

    // Modelling Standards picker dialog
    FileDialog {
        id: stDialog
        currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)
        nameFilters: ["*.xlsx", "*.xlsm", "*.xltx", "*.xltm"]
        onAccepted: {
            var path = selectedFile.toString()
            path = path.replace(/^(file:\/{2})/,"");
            var cleanPath = decodeURIComponent(path);
            stText.text = cleanPath
        }
    }

    // Output path picker dialog
    FolderDialog {
        id: outputDialog
        title: "Please select folder which contains positive training data";
        currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)
        onAccepted: {
            var path = selectedFolder.toString()
            path = path.replace(/^(file:\/{2})/,"");
            var cleanPath = decodeURIComponent(path);
            outputText.text = cleanPath
        }

    }

    Connections {
        target: modelCheck
        function onSignalPrintTxt(boolValue) {
            return
        }
    }

    MessageDialog {
        id: errorMessage
    }
}
