
import consts
import json
import logger_config
import os
import utils


logger = logger_config.get_logger()

def get_group_information_file_path(group_name):
    return consts.GROUP_FILE_PATH.format(group_name)

def loads_group_information():
    group_information = None
    
    group_name = consts.GROUP_DESTINATION
    targets = consts.GROUP_TARGETS
    
    targets_changed = False
    group_information_path = get_group_information_file_path(group_name)
    
    if os.path.exists(group_information_path):
        group_information = utils.loads_data(group_information_path)
        
        if not group_information['group_targets'] == targets:
            targets_changed = True
        
    if not group_information:
        group_information = {
            'group_name': group_name,
            'group_targets': targets,
            'effective_targets': targets,
            'last_execution_day': utils.get_epoch_timestamp(), 
            'daily_members_added_count': 0,
            'total_executions': 0,  
            'last_execution': utils.get_epoch_timestamp(), 
            'total_members_added': 0,
            'successful_adds': 0,
            'failed_adds': 0,
            'flood_wait_count': 0, 
            'last_flood_wait': None,
            'data': {
                'group_members': [],
                'members_added': [],
                'extracted_members': dict()
            }
        }
    else:
        if targets_changed:
            group_information['group_targets'] = targets
            group_information['effective_targets'] = targets
            group_information['data']['extracted_members'] = dict()

    return group_information

def dumps_group_information(group_information):
    group_information_path = get_group_information_file_path(group_information['group_name'])
    utils.dumps_data(group_information_path, group_information)

def check_and_update_group_information(group_information):
    current_day = utils.get_current_day_str()
    
    if not current_day == group_information['last_execution_day']:
        group_information['last_execution_day'] = current_day
        group_information['daily_members_added_count'] = 0
        
    elif group_information['daily_members_added_count'] >= consts.MAX_DAILY_INVITATIONS_PER_DESTINATION_GROUP:
        group_information = None
        
        logger.info(f"group '{group_information['group_name']}' reached the maximum number of daily invitations")
    
    return group_information
        
def get_group():
    group_information = loads_group_information()    
    group_information = check_and_update_group_information(group_information)
    return group_information
    
    