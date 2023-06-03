:: Build script ::

:: Turn off command echo and clear screen
@echo OFF 
cls 

:: Build main exe
pyinstaller -F --paths=venv\Lib\site-packages --version-file=version.txt --icon=vsc.ico main.pyw 

:: Build supporting DOS program
pyinstaller -F --paths=venv\Lib\site-packages --version-file=version_vsct.txt vsct.py

:: Check if main build was successful
if exist dist\main.exe (
    :: Rename exe 
    move /Y dist\main.exe dist\VsCodeTelemetry.exe
    
    echo. && echo.
    echo VsCodeTelemetry.exe build successful!
    echo. 
) else (
    echo. && echo.
    echo VsCodeTelemetry.exe build failed!
    echo. && echo.
    exit
)

:: Check if vsct build was successful
if exist dist\vsct.exe (
    :: Copy to C:\\bin
    copy dist\vsct.exe C:\\bin\\vsct.exe

    echo. && echo.
    echo vsct.exe build successful!
    echo. && echo.

) else (
    echo. && echo.
    echo vsct.exe build failed!
    echo. && echo.
)

:: If all builds were successful, move VsCodeTelemetry.exe to startup
copy /Y dist\VsCodeTelemetry.exe "%AppData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"

if exist "%AppData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\VsCodeTelemetry.exe" (
    echo. && echo.
    echo VsCodeTelemetry.exe moved to startup!
    echo. && echo.
) else (
    echo. && echo.
    echo VsCodeTelemetry.exe failed to move to startup!
    echo. && echo.
)

:: Remove build files
del main.spec
del vsct.spec

:: Remove build folders
rmdir /S /Q build

echo. && echo.
echo Build complete!