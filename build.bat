:: Build script ::

:: Turn off command echo and clear screen
@echo OFF 
cls 

:: Build main exe
pyinstaller -F --paths=venv\Lib\site-packages --version-file=version.txt main.pyw 

:: Build supporting DOS program
pyinstaller -F --paths=venv\Lib\site-packages --version-file=version_vsct.txt vsct.py


:: Check if main build was successful
if exist dist/main.exe (
    :: Rename exe 
    copy main dist/VsCodeTelemetry.exe

    :: Remove old exe
    del dist/main.exe
)

if exist dist/VsCodeTelemetry.exe (
    echo. && echo.
    echo VsCodeTelemetry.exe build successful!
    echo. 

    if exist dist/vsct.exe (

        :: Copy to /bin
        copy dist/vsct.exe bin/vsct.exe

        echo. && echo.
        echo vsct.exe build successful!
        echo. && echo.
    )
)