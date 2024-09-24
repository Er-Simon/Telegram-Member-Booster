import accounts_manager
import consts
import groups_manager
import json
import logger_config
import utils
import time
import telegram_member_boost


logger = logger_config.get_logger()

if __name__ == '__main__':
    
    logger.info(f"start execution - {utils.get_current_datetime_str()}")
    
    while True:
        account_information = accounts_manager.get_account()
        
        if not account_information:
            logger.info("account not available")
            break
        
        logger.info(f"account used '{account_information['session_name']}'")
            
        group_information = groups_manager.get_group()
                
        if not group_information:
            logger.info("group not available")
            break

        logger.info(f"destination group '{group_information['group_name']}'")

        account_information_updated = telegram_member_boost.start(account_information, group_information)
        
        if account_information_updated:
            logger.info(f"account information updated:\n{json.dumps(account_information_updated, indent=2)}\n")
        else:
            break
        
        pause_time = utils.get_random_floating_number(
            consts.MIN_EXECUTION_PAUSE_SECONDS,
            consts.MAX_EXECUTION_PAUSE_SECONDS
        )
        
        logger.info(f"waiting {pause_time} seconds before continuing...")
        
        time.sleep(pause_time)
        
    logger.info(f"end of execution - {utils.get_current_datetime_str()}")   
    
    