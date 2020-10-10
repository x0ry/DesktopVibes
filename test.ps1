
$program = [string]$(Get-Content -Raw -Path "C:\Users\x0ry\Documents\phue-master\ExternalVariablesHashTable.txt").Trim()
$slideselect = $program -as [int]
function fStartProcess([string]$sProcess,[string]$sArgs,[ref]$pOutPut)
{
    $oProcessInfo = New-Object System.Diagnostics.ProcessStartInfo
    $oProcessInfo.FileName = $sProcess
    $oProcessInfo.RedirectStandardError = $true
    $oProcessInfo.RedirectStandardOutput = $true
    $oProcessInfo.UseShellExecute = $false
    $oProcessInfo.Arguments = $sArgs
    $oProcessInfo.UseShellExecute = $false
    $oProcessInfo.CreateNoWindow = $true
    $oProcess = New-Object System.Diagnostics.Process
    $oProcess.StartInfo = $oProcessInfo
    $oProcess.Start() | Out-Null
    $oProcess.WaitForExit() | Out-Null
    $sSTDOUT = $oProcess.StandardOutput.ReadToEnd()
    $sSTDERR = $oProcess.StandardError.ReadToEnd()
    $pOutPut.Value=$sSTDOUT
    return $oProcess.ExitCode
}
$files = dir -path "C:\Users\x0ry\Documents\phue-master\images" -recurse
if($slideselect -gt -1){
$sample = $files[$slideselect]
if ($slideselect -gt 13){$slideselect = 0}
Out-File -FilePath "C:\Users\x0ry\Documents\phue-master\ExternalVariablesHashTable.txt" -InputObject $($slideselect+1) -Encoding ascii;
}
else {$sample = $files | get-random -count 1}
$setwallpapersrc = @"
using System.Runtime.InteropServices;
public class wallpaper
{
public const int SetDesktopWallpaper = 20;
public const int UpdateIniFile = 0x01;
public const int SendWinIniChange = 0x02;
[DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
private static extern int SystemParametersInfo (int uAction, int uParam, string lpvParam, int fuWinIni);
public static void SetWallpaper ( string path )
{
SystemParametersInfo( SetDesktopWallpaper, 0, path, UpdateIniFile | SendWinIniChange );
}
}
"@
Add-Type -TypeDefinition $setwallpapersrc
[wallpaper]::SetWallpaper($sample.FullName) 

Sleep -seconds .5

$Output=""
$iRet=fStartProcess python "C:\Users\x0ry\Documents\phue-master\test.py" ([ref]$Output)
write-host $Output.Trim()

Set-ItemProperty -Path "HKCU:\Control Panel\Colors" -Name "HotTrackingColor" -Value $Output
Set-ItemProperty -Path "HKCU:\Control Panel\Colors" -Name "Hilight" -Value $Output
 Start-Sleep -s 1
 rundll32.exe user32.dll, UpdatePerUserSystemParameters, 0, $false
#Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP" -Name "DesktopImagePath" -Value $sample.FullName
#Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP" -Name "DesktopImageUrl" -Value $sample.FullName
#Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP" -Name "LockScreenImagePath" -Value $sample.FullName
#Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP" -Name "LockScreenImageUrl" -Value $sample.FullName