# Backuper
Personal backup script

TBA

## Development
### Install
```
pip install poetry==1.8.3
poetry config virtualenvs.create false
poetry install
pre-commit install
```


```
adb shell ls sdcard/DCIM/Camera/PXL_202406* | foreach {adb pull -a -p "$_" "D:\Pixel 8 Pro\Camera\12024-06"}
```

### Run
```
backuper config.yml
echo "<config>" | backuper -
```
