Set fileSystem = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

projectFolder = fileSystem.GetParentFolderName(WScript.ScriptFullName)
pythonWindowless = projectFolder & "\.venv\Scripts\pythonw.exe"
jarvisScript = projectFolder & "\jarvis.py"
heartbeatPath = shell.ExpandEnvironmentStrings("%TEMP%") & "\jarvis_vbs_heartbeat.txt"
stopPath = shell.ExpandEnvironmentStrings("%TEMP%") & "\jarvis_vbs_stop.txt"

If Not fileSystem.FileExists(pythonWindowless) Then
    pythonWindowless = "pythonw.exe"
End If

shell.CurrentDirectory = projectFolder
commandLine = Chr(34) & pythonWindowless & Chr(34) & " " & Chr(34) & jarvisScript & Chr(34)
shell.Environment("Process")("JARVIS_VBS_HEARTBEAT") = heartbeatPath
On Error Resume Next
fileSystem.DeleteFile stopPath, True
On Error GoTo 0
Set heartbeatFile = fileSystem.CreateTextFile(heartbeatPath, True)
heartbeatFile.WriteLine "JARVIS ACTIVE"
heartbeatFile.Close

Set jarvisProcess = shell.Exec(commandLine)
Do While jarvisProcess.Status = 0
    If fileSystem.FileExists(stopPath) Then
        jarvisProcess.Terminate
        Exit Do
    End If
    Set heartbeatFile = fileSystem.CreateTextFile(heartbeatPath, True)
    heartbeatFile.WriteLine "JARVIS ACTIVE"
    heartbeatFile.Close
    WScript.Sleep 500
Loop

On Error Resume Next
fileSystem.DeleteFile heartbeatPath, True
fileSystem.DeleteFile stopPath, True
