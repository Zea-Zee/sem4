@echo off
setlocal

REM Найти устройство камеры
for /f "tokens=2 delims=:" %%i in ('wmic path Win32_PnPEntity where "Service='usbvideo'" get DeviceID /value') do (
    set "CAMERA_ID=%%i"
    goto :found_camera
)

echo No camera found
exit /b 1

:found_camera
REM Установление разрешения и частоты отображения
set RESOLUTION=1280x720
set DISPLAY_FREQUENCY=30

REM Запуск Python-скрипта с параметрами
python script_name.py --cam_name %CAMERA_ID% --resolution %RESOLUTION% --display_frequency %DISPLAY_FREQUENCY%

endlocal
