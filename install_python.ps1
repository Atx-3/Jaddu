$url = "https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
$output = "python_installer.exe"
Write-Host "Downloading Python 3.12... from $url"
try {
    Invoke-WebRequest -Uri $url -OutFile $output
    Write-Host "Download complete provided."
    Write-Host "Installing Python... (Please wait ~2 minutes)"
    Start-Process -FilePath $output -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Write-Host "Python installed successfully!"
} catch {
    Write-Error "Failed to install Python. Error: $_"
}
