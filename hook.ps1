function global:Prompt {

    # Detect failure:
    $failed =
        ($LASTEXITCODE -ne 0) -or
        ($Error.Count -gt 0 -and $Error[0].InvocationInfo)

    if ($failed) {

        # Get last executed command
        $lastCommand = (Get-History -Count 1).CommandLine

        # Get error message (PowerShell error or fallback)
        $errorMessage = if ($Error.Count -gt 0) {
            $Error[0].Exception.Message
        } else {
            "Exit code $LASTEXITCODE"
        }

        $log = @{
            timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
            command   = $lastCommand
            error     = $errorMessage
            exit_code = $LASTEXITCODE
            shell     = "PowerShell"
        }

        ($log | ConvertTo-Json -Compress) |
            Add-Content 'C:\Projects\CLI-error-assist\errors.jsonl'

        # Clear error so we don’t log repeatedly
        $Error.Clear()
    }

    "PS $($executionContext.SessionState.Path.CurrentLocation)> "
}
