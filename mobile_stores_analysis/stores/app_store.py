import requests
from fake_useragent import UserAgent
import urllib3
import datetime
from openpyxl.comments import Comment
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def app_store_analysis(driver, logger, timeout):
    # Spawn Chrome browser waiting for the user login to App Store Connect
    logger.info("Login phase starting...")
    driver.get('https://appstoreconnect.apple.com/login?targetUrl=%2Fapps')

    try:
        # Wait for the HTTP request to https://appstoreconnect.apple.com/apps
        WebDriverWait(driver, timeout).until(EC.url_to_be("https://appstoreconnect.apple.com/apps"))
        logger.info("Completed login phase.")

    except TimeoutException:
        print("NO APP LIST")

    # Take the "myacinfo" cookie from Selenium  
    cookie = driver.get_cookie("myacinfo")
    cookies = {"myacinfo":cookie['value']}
    logger.info("Retrieving cookies...")
    logger.info(cookies)
    logger.info("Cookie retrieved.")

    # Retrieve JSON with apps list and related information
    logger.info("Retrieving apps information...")
    URL = "https://appstoreconnect.apple.com/iris/v1/apps?include=displayableVersions&limit=200&limit[displayableVersions]=20"
    logger.info(URL)

    # Random User-Agent
    ua = UserAgent(browsers=['edge', 'chrome'])
    # Make the request
    response = requests.get(URL, cookies=cookies, headers={'User-Agent':ua.random, "Accept":"application/vnd.api+json"})
    json_body = response.json()
    logger.info(json_body)

    # Current date for CSV filename
    date = datetime.datetime.now().strftime("%Y%m%d")
    apps_info={}

    # Write App information in the CSV file and read Response body (JSON)
    with open(f"{date}_AppStore.csv", "w") as f:
        logger.info(f"New file created: {date}_AppStore.csv")
        # CSV Headers
        f.write("App Name,Bundle ID,App ID,Version,Status,Is Watch Only?,Downlodable,Date,Is public?,Release History URL,App Store URL\n")

        # Read JSON response content
        for x in json_body['data']:
            # Application number ID
            app_id = x['id']
            # Bundle ID
            bundle_id = x['attributes']['bundleId']
            # Application common name
            name = x['attributes']['name']
            # GET request for JSON content with details about App versions
            version_url = x['relationships']['appStoreVersions']['links']['related']
            response = requests.get(version_url, cookies=cookies, headers={'User-Agent':ua.random, "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8"}, verify=False)
            json_body2 = response.json()
            logger.info(json_body2)
            # Current Application version
            version = json_body2['data'][0]['attributes']['versionString']
            # Current version status
            version_state = json_body2['data'][0]['attributes']['appVersionState']
            # Is the application only for watches?
            is_watch_only = json_body2['data'][0]['attributes']['isWatchOnly']
            # Is the application downloadable?
            downlodable = json_body2['data'][0]['attributes']['downloadable']
            # Creation date of the last application version
            createdDate = json_body2['data'][0]['attributes']['createdDate']
            # URL of the release history for an application
            release_history_url = f"https://appstoreconnect.apple.com/apps/{app_id}/distribution/activity/ios/versions"

            # URL of the application on the public App Store
            store_url = f"https://apps.apple.com/app/id{app_id}"
            # GET request to verify if the application is on the public store
            response = requests.get(store_url, allow_redirects=True)
            # Is the application publicly available on App Store to users?
            is_public = (response.status_code == 200)

            # No URL of the application on the public App Store
            if not is_public:
                store_url=''

            # Write information in the file
            f.write(f"{name},{bundle_id},{app_id},{version},{version_state},{is_watch_only},{downlodable},{createdDate},{is_public},{release_history_url},{store_url}\n")
            logger.info(f"Analysed and written: {bundle_id}")

    logger.info(f"Completed - Retrieving apps information.")    
    logger.info(f"File saved: {date}_AppStore.csv")