@echo off
setlocal EnableExtensions

set "INPUT_FILE=%~1"
set "PATCH_ARGS="

if not "%~1"=="" (
    shift
)

:parse_args
if "%~1"=="" goto done_args
set "PATCH_ARGS=%PATCH_ARGS% %1"
shift
goto parse_args
:done_args

if "%INPUT_FILE%"=="" (
    set /p "INPUT_FILE=Please drop or enter the ISO/WBFS file path: "
)

if defined INPUT_FILE (
    set "INPUT_FILE=%INPUT_FILE:"=%"
)

if "%INPUT_FILE%"=="" (
    echo Error: No input file specified.
    pause
    exit /b 1
)

if not exist "%INPUT_FILE%" (
    echo Error: File "%INPUT_FILE%" does not exist.
    pause
    exit /b 1
)

echo Extracting DATA partition from "%INPUT_FILE%"...
wit extract --psel DATA --overwrite "%INPUT_FILE%" wbi_extracted
if %ERRORLEVEL% neq 0 (
    echo Error: wit extract failed.
    pause
    exit /b %ERRORLEVEL%
)

echo Patching game files...
python patch.py %PATCH_ARGS%
if %ERRORLEVEL% neq 0 (
    echo Error: patch.py failed.
    pause
    exit /b %ERRORLEVEL%
)

echo Rebuilding WBFS...
wit copy --overwrite wbi_extracted/ wbi_patched.wbfs
if %ERRORLEVEL% neq 0 (
    echo Error: wit copy failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Successfully created wbi_patched.wbfs!
pause
