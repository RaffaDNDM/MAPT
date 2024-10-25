import undetected_chromedriver as uc
from auto_download_undetected_chromedriver import download_undetected_chromedriver
from stores.app_store import app_store_analysis
from stores.play_store import play_store_analysis
import argparse
from termcolor import colored
import logging
import os
import sys

# Folder where the script will install the driver applying patches to make it undetectable
DRIVER_PATH = "c:/Download_ChromeDriver"

# Disable OUTPUT
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore OUTPUT
def enablePrint():
    sys.stdout = sys.__stdout__

def arg_parser():
    '''
    Parser of command line arguments
    '''
    #Parser of command line arguments
    parser = argparse.ArgumentParser(allow_abbrev=False)
    #Initialization of needed arguments
    parser.add_argument("--apple", "--appstore", dest="appstore", action='store_true', help="List the App Store apps.")
    parser.add_argument("--google", "--playstore", dest="playstore", action='store_true', help="List the Play Store apps.")
    parser.add_argument("--debug", "-d", dest="debug", action='store_true', help="Debug mode.")
    parser.add_argument("--timeout", "-t", dest="timeout", type=int, help="Timeout in seconds (default: 60s) for login phase.", default=60)
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.appstore and not args.playstore:
        parser.print_help()
        exit(1)

    return args.appstore, args.playstore, args.debug, args.timeout

def main():
    global DRIVER_PATH
    # Define logger
    logging.basicConfig(level=logging.CRITICAL, force=True)
    logger = logging.getLogger()
    
    # Arg Parser
    appstore, playstore, debug, timeout = arg_parser()
    
    if debug: 
        logging.basicConfig(level=logging.INFO, force=True)
        logger = logging.getLogger()

    # Driver installation
    if not debug:
        blockPrint()

    logger.info(colored("-----------------------------------------------", 'green'))
    logger.info(colored("|             DRIVER INSTALLATION             |", 'green'))
    logger.info(colored("-----------------------------------------------", 'green'))
    chrome_driver_path = download_undetected_chromedriver(DRIVER_PATH, undetected=True, arm=False, force_update=True)
    logger.info(colored("-----------------------------------------------", 'green'))

    if not debug:
        enablePrint()

    # Define Chrome Options for logging of every requests
    options = uc.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    # Chrome driver for Selenium with options previously defined
    driver = uc.Chrome(driver_executable_path=chrome_driver_path, options=options)

    # App Store

    if appstore:
        logger.info(colored("-----------------------------------------------", 'yellow'))
        logger.info(colored("|                 APPLE STORE                 |", 'yellow'))
        logger.info(colored("-----------------------------------------------", 'yellow'))
        app_store_analysis(driver, logger, timeout)
        logger.info(colored("-----------------------------------------------", 'yellow'))
    
    if playstore:
        logger.info(colored("-----------------------------------------------", 'yellow'))
        logger.info(colored("|                  PLAY STORE                 |", 'yellow'))
        logger.info(colored("-----------------------------------------------", 'yellow'))
        play_store_analysis(driver, logger, timeout)
        logger.info(colored("-----------------------------------------------", 'yellow'))

if __name__=="__main__":
    main()