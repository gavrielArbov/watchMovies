function LogError {
    param ($Message)
  
    Write-Output "ERROR -- $($Message)"
    Write-Output "";
  }
  
  function LogStep {
    param ($Message)
  
    Write-Output "[x] $($Message)"
    Write-Output "";
  }
  

try {
    if (Test-Path -Path venv) {
        LogStep("Removing existing venv")
        Remove-Item -r venv
    }
    LogStep("Creating venv for python")
    py -3 -m venv venv
    venv\Scripts\activate
    pip install Flask
    pip install requests
    pip install pymongo
    .\venv\Scripts\Activate.ps1


} catch {
    LogError("Failed to intialized venv for python")
    exit(1)
}

LogStep("Intialized venv for python")