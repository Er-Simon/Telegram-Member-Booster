import consts
import json
import logger_config
import os
import utils


logger = logger_config.get_logger()

def get_account_information_file_path(session_name):
    return consts.ACCOUNT_FILE_PATH.format(session_name)

def loads_session_names():
    session_names = []
    file_names = os.listdir(consts.SESSIONS_FOLDER_PATH)
    for file_name in file_names:
        name, extension = os.path.splitext(file_name)
        if extension == '.session':
            session_names.append(name)
        else:
            logger.warning(f"file '{file_name}' does not have a valid session name.")
    
    return session_names

def loads_account_information(session_name):
    account_information = None
    account_information_path = get_account_information_file_path(session_name)
    
    if os.path.exists(account_information_path):
        account_information = utils.loads_data(account_information_path)
        
    if not account_information:
        account_information = {
            'session_name': session_name,
            'name': None,
            'username': None,
            'total_executions': 0,  
            'last_execution': utils.get_millennium_datetime_str(), 
            'total_invites_sent': 0,
            'successful_invites': 0,
            'failed_invites': 0,
            'flood_wait_count': 0, 
            'last_flood_wait': None,
            'error': None,
            'error_message': None
        }

    return account_information

def dumps_account_information(account_information):
    account_information_path = get_account_information_file_path(account_information['session_name'])
    utils.dumps_data(account_information_path, account_information)

def get_account():
    account = None
    
    session_names = loads_session_names()
    logger.debug(f"session_names loaded are: {session_names}")
    
    accounts_informations = dict()
    for session_index in range(len(session_names)):
        account_information = loads_account_information(session_names[session_index])
        
        if account_information['error']:
            logger.debug(f"account {session_index} '{account_information['session_name']}' cannot be used, error: {account_information['error_message']}")
            continue
        
        seconds_from_last_execution = utils.calculate_seconds_between_datetimes(account_information["last_execution"])
        
        if  seconds_from_last_execution > consts.ACCOUNT_REUSE_DELAY_SECONDS:
            accounts_informations[session_index] = account_information
        else:
            logger.debug(f"account {session_index} '{account_information['session_name']}' cannot be used, seconds_from_last_execution: {seconds_from_last_execution}")
    
    if not accounts_informations == dict():
        logger.debug(f"accounts_informations loaded are:\n{json.dumps(accounts_informations, indent=2)}\n")
        indexes = sorted(accounts_informations, key=lambda index: utils.parse_str_to_datetime(accounts_informations[index]['last_execution']))
        
        logger.debug(f"account:\n{json.dumps(accounts_informations[indexes[0]], indent=2)}\n")
        account = accounts_informations[indexes[0]]
    
    return account
    