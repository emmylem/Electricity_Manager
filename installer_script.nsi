!define APP_NAME "Electricity Manager"
!define APP_EXE "electricity.exe" ; This is the executable generated from your Python script

Name "${APP_NAME} Installer"
OutFile "${APP_NAME}_Setup.exe"

Section
SetOutPath "$INSTDIR"
File "dist\electricity" ; Include your Python executable here
CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
Delete "$INSTDIR\${APP_EXE}"
Delete "$INSTDIR\Uninstall.exe"
Delete "$DESKTOP\${APP_NAME}.lnk"
RMDir "$INSTDIR"
SectionEnd
