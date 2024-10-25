import json
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests

# Process Selenium log
def processLog(driver, log, target_url):
    # Take content of the the log
    message = log["message"]

    # HTTP Response received
    if "Network.responseReceived" in message:
        # Log components
        params = json.loads(message)["message"].get("params")

        if params:
            # Response
            response = params.get("response")
            
            # If HTTP Response has body and the URL contains target_url 
            if response and (target_url in response["url"]):
                # Response body 
                body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': params["requestId"]})
                response_body = body['body']
                return response_body
        
        # No response Body if checks failed
        return None

def play_store_analysis(driver, logger, timeout):
    # Login page for the access to the Developer Console
    logger.info("Login phase starting...")
    driver.get('https://accounts.google.com/ServiceLogin?service=androiddeveloper&passive=true&continue=https%3A%2F%2Fplay.google.com%2Fconsole%2Fdeveloper%2F')

    try:
        # Wait for the HTTP request to
        # https://play.google.com/console/u/0/developers/{account_id}/app-list
        WebDriverWait(driver, timeout).until(EC.url_contains("app-list"))
        logger.info("Completed login phase.")

        # Log all the requests
        logs = driver.get_log("performance")
        app_list_url = driver.current_url
        logger.info(f"App list available at: {app_list_url}")

    except TimeoutException:
        logger.error(f"NO APP LIST AVAILABLE")

    # Parse all HTTP request sent to populate the page
    logger.info("Retrieving apps information...")
    target_url="/appSummaries"
    json_body = None
    for log in logs:
        # Process log to find HTTP response for 
        # https://playconsoleapps-pa.clients6.google.com/v1/developers/{account_id}/appSummaries?$httpHeaders={HEADERS}&pageSize=500&pageToken=
        response_body = processLog(driver, log, target_url)
        if response_body:
            json_body = json.loads(response_body)

    logger.info(json_body)

    # Write Apps list in a CSV file
    date = datetime.now().strftime("%Y%m%d")

    with open(f"{date}_PlayStore.csv", "w") as f:
        logger.info(f"New file created: {date}_PlayStore.csv")
        # CSV Headers
        f.write("Account ID,Web ID,App Name,App ID,Status,Is Public?,Timestamp,Release History URL,Play Store URL\n")

        if "1" in json_body:
            # For each App
            for x in json_body["1"]:
                # Account ID
                account_id = x["1"]["1"]["1"]              
                # App - Web ID
                app_web_id = x["1"]["2"]["1"]
                # App Name
                app_name = x["2"]

                #Public store information                
                is_public = "N/A"
                public_store_url = ''
                # App ID (if available)
                app_id = ''
                if "5" in list(x.keys()): 
                    app_id = x["5"]

                    # Check if the app is available on the public Play Store for the users
                    response = requests.get(f"https://play.google.com/store/apps/details?id={x['5']}")
                    is_public = (response.status_code==200)

                    # If public, store the URL of the application of the public Play Store
                    if is_public:
                        public_store_url=f"https://play.google.com/store/apps/details?id={x['5']}"

                # Status (6 if Production)
                app_status = 'Other'
                if x["4"]["1"][0]==6:
                    app_status = "Production"
                
                # Last Update Date
                created_date=datetime.strftime(datetime.fromtimestamp(int(x["6"]["1"])), "%Y-%m-%d")
                
                # Release Tab for the application
                release_url = f'https://play.google.com/console/u/0/developers/{x["1"]["1"]["1"]}/app/{x["1"]["2"]["1"]}/tracks/production?tab=releases'

                f.write(f"{account_id},{app_web_id},{app_name},{app_id},{app_status},{is_public},{created_date},{release_url},{public_store_url}\n")

    logger.info(f"Completed - Retrieving apps information.")    
    logger.info(f"File saved: {date}_PlayStore.csv")