ECHO OFF
ECHO #-#-#-# WetherSporks - Team 19 - 5CM505 #-#-#-#
ECHO SETTING UP PYTHON VIRTUAL ENVIRONMENT

@REM Cannot have spaces when defining variables in batch files
@REM Variables
SET PYTHON_EXECUTABLE=notfound
SET DJANGO_PROJ_NAME=WetherSporks
SET MANAGE_FILE=WetherSporks/manage.py

@REM Finding Machines Python Executable
FOR %%P IN ("python") DO (
    %%~P --version
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_EXECUTABLE=%%~P
        ECHO Python command found: %%~P
        GOTO :start_proj_configuration
    )
)
IF %PYTHON_EXECUTABLE%=notfound (
    ECHO Python is not installed on this machine?
)

@REM Main Setup Function
:start_proj_configuration

@REM Determine if in correct location for execution
IF EXIST %MANAGE_FILE% (
    @REM Create Virtual Environment
    if NOT EXIST v\Scripts\activate.bat (
        ECHO CREATING VIRTUAL ENVIRONMENT
        %PYTHON_EXECUTABLE% -m venv v
    ) ELSE (
        ECHO VIRTUAL ENVIRONMENT ALREADY PRESENT
    )

    @REM Install Django Dependencies
    ECHO INSTALLING REQUIREMENTS
    "v\Scripts\python" -m pip install --upgrade pip
    "v\Scripts\python" -m pip install -r requirements.txt


    @REM Update Django Database
    ECHO Migrating Database 
    "v\Scripts\python" %MANAGE_FILE% makemigrations
    "v\Scripts\python" %MANAGE_FILE% migrate

    @REM Finished
    ECHO:
    ECHO START THE VIRTUAL ENVIRONMENT: "v/Scripts/activate"
    ECHO START APPLICATION: "%PYTHON_EXECUTABLE% %MANAGE_FILE% runserver"

) ELSE (
    ECHO:
    ECHO STOPPING - MISSING "%MANAGE_FILE%"
    ECHO CWD Missing? Or Running this from incorrect location in cmdline?
    
    ECHO ##############################################################################################################################################################
    ECHO RUN THIS FILE FROM ITS LOCATION: %~dp0
    ECHO ##############################################################################################################################################################
)
