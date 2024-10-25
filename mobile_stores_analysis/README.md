﻿# Mobile Stores Analysis
The script will retrieve the list of all the mobile applications having access to mobile stores developer console.

Having valid App Store Connect credentials, the script will retrieve all the information about the apps:
- _**App Name:**_ Application common name
- _**Bundle ID:**_ Application bundle ID
- _**App ID:**_ Application number ID 
- _**Version:**_ Application version 
- _**Status:**_ Application development status
- _**Is Watch Only:**_ Is the application only for watches?
- _**Downlodable:**_ Is the application downloadable?
- _**Date:**_ Creation date of the last application version
- _**Is public?:**_ Is the application publicly available on App Store to users?
- _**Release History URL:**_ URL of the release history for an application
- _**App Store URL:**_ URL of the application on the public App Store

Having valid Play Store Console credentials, the script will retrieve all the information about the apps:
- _**Account ID:**_ Account ID of the user used to access the Developer Console
- _**Web ID:**_ Application number ID used in Developer Console
- _**App Name:**_ Application common name 
- _**App ID:**_ Application ID 
- _**Status:**_ Application development status
- _**Date:**_ Creation date of the last application version
- _**Is public?:**_ Is the application publicly available on Play Store to users?
- _**Release History URL:**_ URL of the release history for the an application
- _**Play Store URL:**_ URL of the application on the public Play Store

---

## Installation
```bash
pip install -r requirements.txt
```

---

## Execution
```bash
python3 main.py [--apple] [--google] [--timeout <seconds>] [--debug] [--help]
```
You can specify two modalities:
- `--apple`: to retrieve information about mobile application from the App Store Connect account
- `--google`: to retrieve information about mobile application from the Play Store Console account

Other options:
- `--timeout <seconds>`: to specify timeout in seconds for the login phase (default: 60s)
- `--debug`: debug mode
- `--help`: help command

### App Store Connect
If you specify `--apple` a new Chrome Window will be open using Selenium and you have 60 seconds to login into the App Store Connect using valid credentials.
![App Store Login](.img/app_login.png)
![App Store OTP](.img/app_otp.png)
![App Store Trust](.img/app_trust.png)
![App Store OTP](.img/app_store_connect.png)


Then the script will retreive information of the apps that the account can access to in its console and will output in a CSV file (`YYYYMMDD__AppStore.csv`).

### Play Store Console
If you specify `--google` a new Chrome Window will be open using Selenium and you have 60 seconds to login into the Play Store Developer Console using valid credentials.
![Play Store Login](.img/play_login.png)
![Play Store Company](.img/play_company.png)
![Play Store Developer Console](.img/play_developer_console.png)


Then the script will retreive information of the apps that the account can access to in its console and will output in a CSV file (`YYYYMMDD__PlayStore.csv`).
