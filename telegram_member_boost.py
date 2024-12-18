import asyncio
import accounts_manager
import consts
import groups_manager
import logger_config
import utils
import random

from telethon import TelegramClient, errors
from telethon.tl.functions.channels import InviteToChannelRequest


logger = logger_config.get_logger()

def create_client(account_information):
    session_file_path = consts.SESSION_FILE_PATH.format(account_information['session_name'])
        
    client = TelegramClient(
        session_file_path,
        api_id=consts.API_ID,
        api_hash=consts.API_HASH,
    ) 
    
    return client

async def get_members(client:TelegramClient, group_name, filter=consts.FILTER_MODE):
    user_ids = set()
    participants = []
    
    try:
        participants = await client.get_participants(group_name)
    except Exception as e:
        logger.error(f"failed to get_participants from the group_name: {group_name}")
        logger.error(f"error: {e}")
        raise e
    else:
        logger.debug(f"obtained {len(participants)} participants from group '{group_name}'")
        
    for participant in participants:         
        if filter:
            if participant.is_self or participant.deleted or participant.bot or participant.scam or participant.fake:
                continue
            
            if participant.status and hasattr(participant.status, 'was_online'):
                difference_in_seconds = utils.calculate_seconds_between_datetimes(participant.status.was_online)
            
                if difference_in_seconds > consts.MEMBER_MAXIMUM_INACTIVITY_SECONDS:
                    continue                
                
        user_ids.add(participant.id)
    
    if filter:            
        logger.debug(f"obtained {len(user_ids)} participants from group '{group_name}' after applying filters")
              
    return user_ids

async def add_members(client, account_information, group_information, member_ids):
    stop_execution = False
    invitations_counter = 0
    
    member_ids = list(member_ids)
    random.shuffle(member_ids)
    
    while member_ids != []:
        user_id = member_ids.pop()
        
        invitations_counter += 1
        
        account_information['total_invites_sent'] += 1
        
        try:            
            await client(InviteToChannelRequest(
                group_information['group_name'],
                [user_id]
            ))
        except Exception as e:
            account_information['failed_invites'] += 1

            group_information['failed_adds'] += 1
            
            logger.info(f"invitation: {invitations_counter} - the user '{user_id}' cannot be invite to the group '{group_information['group_name']}'")
            logger.info(f"error: {e}")
            
            if isinstance(e, errors.PeerFloodError):
                stop_execution = True
                
                logger.error("the account has received a Peer Flood Error, which means it has been flagged several times and is now restricted. \
                    if you want to check if your account has been limited, simply send a private message to @SpamBot through Telegram itself.")
                
                account_information['last_execution'] = utils.get_future_datetime_str(days_to_add=consts.PEER_FLOOD_ERROR_PAUSE_DAYS)
                
                logger.info(f"the account '{account_information['session_name']}' was blocked for {consts.PEER_FLOOD_ERROR_PAUSE_DAYS} days as a preventive measure.")
                
                break
            
            if isinstance(e, errors.FloodWaitError):
                stop_execution = True
                
                now = utils.get_current_datetime_str()
                
                account_information['flood_wait_count'] += 1
                account_information['last_flood_wait'] += now
                
                group_information['flood_wait_count'] += 1
                group_information['last_flood_wait'] += now
                
                logger.error("the account has received a Flood Wait Error, indicating that the maximum number of requests has \
                    been reached within a certain time frame. To avoid further issues, it is necessary to increase the pause between invites.")
                
                break
        else:
            account_information['successful_invites'] += 1
            
            group_information['total_members_added'] += 1
            group_information['successful_adds'] += 1
                    
            logger.info(f"invitation: {str(invitations_counter).ljust(len(str(consts.INVITATIONS_PER_ACCOUNT)))} - invited to group '{group_information['group_name']}' - user_id: '{user_id}'")
        
        finally:
            group_information['daily_members_added_count'] += 1
            
        if invitations_counter >= consts.INVITATIONS_PER_ACCOUNT:
            logger.debug("max daily invitations per account reached")
            break
                   
        if group_information['daily_members_added_count'] >= consts.MAX_DAILY_INVITATIONS_PER_DESTINATION_GROUP:
            logger.debug("max daily invitations per destination group reached")
            break
        
        await asyncio.sleep(utils.get_random_floating_number(
            consts.MIN_INVITATION_PAUSE_SECONDS,
            consts.MAX_INVITATION_PAUSE_SECONDS
        ))
        
    return account_information, group_information, member_ids, stop_execution

async def is_authorized(client:TelegramClient, account_information):
    is_authorized = await client.is_user_authorized()
    
    logger.debug(f"account {account_information['session_name']} authorization status: {is_authorized}")
    
    if not is_authorized:
        logger.info(f"unauthorized account: {account_information['session_name']}")
        
        while True:
            choice = input('authorize the account via phone number? [Y/n] ').strip().lower()
            
            if choice == 'y':
                user_phone_numer = input("insert the user's phone number (with prefix): ")
            
                await client.send_code_request(user_phone_numer)
            
                auth_code = input("insert the received code: ")
                
                try:
                    await client.sign_in(user_phone_numer, auth_code)
                except Exception as e:
                    logger.error(f"the account cannot be authorized, error: {e}")
                else:
                    is_authorized = await client.is_user_authorized()
                
                    if is_authorized:
                        logger.info(f"account authorized: {account_information['session_name']}")
                        break
            else:
                break
            
    return is_authorized
    
async def execute(client:TelegramClient, account_information, group_information):  
            
    try:
        await client.connect()
    except Exception as e:
        logger.error(f"failed to connect to the account: {account_information['session_name']}")
        logger.error(f"error: {e}")
        return
    
    stop_execution = False
    
    account_is_authorized = await is_authorized(client, account_information)
    
    if not account_is_authorized:
        account_information['error'] = True
        account_information['error_message'] = "the account ins't authorized"
    else:
        telegram_user_info = await client.get_me()
                
        account_information['name'] = " ".join([name.strip() for name in [telegram_user_info.first_name, telegram_user_info.last_name] if name])
        account_information['username'] = telegram_user_info.username
        
        account_information['total_executions'] += 1
        account_information['last_execution'] = utils.get_current_datetime_str()
            
        # update destination group members
        try:
            destination_group_members = await get_members(client, group_information['group_name'], filter=False)
        except ValueError:
            return 
        
        logger.info(f"obtained {len(destination_group_members)} participants from the group destination '{group_information['group_name']}'")
        
        group_information['total_executions'] += 1
        group_information['last_execution'] = utils.get_current_datetime_str()

        group_information['data']['group_members'] = list(set(group_information['data']['group_members']) | destination_group_members)

        member_ids = set()
        if not consts.FRESH_MODE:
            member_ids = set(group_information['data']['extracted_members'].get(account_information['session_name'], set()))
            
            if not member_ids == set():
                member_ids = member_ids - set(group_information['data']['group_members'])
                member_ids = member_ids - set(group_information['data']['members_added'])
        
        if consts.INVITATIONS_PER_ACCOUNT > len(member_ids):
            invalid_targets = set()
            
            targets = group_information['effective_targets']
            random.shuffle(targets)
            
            for target in targets:
                try:
                    target_member_ids = await get_members(client, target)
                except ValueError:
                    invalid_targets.add(target)
                    continue
                
                target_member_ids = target_member_ids - set(group_information['data']['group_members']) 
                target_member_ids = target_member_ids - set(group_information['data']['members_added']) 
                
                logger.info(f"obtained {len(target_member_ids)} participants from the group '{target}' after removing of destination group members and added members")

                member_ids = member_ids | target_member_ids
                
                if len(member_ids) >= consts.INVITATIONS_PER_ACCOUNT:
                    break
                    
            if len(invalid_targets) > 0:
                group_information['effective_targets'] = list(set(group_information['effective_targets']) - invalid_targets)
            
        
        if len(member_ids) == 0:
            logger.warning(f'there are no participants to invite')    
        else:
            logger.info(f'total participants available to be added: {len(member_ids)}')    
        
        account_information, group_information, not_added_member_ids, stop_execution = await add_members(client, account_information, group_information, member_ids)  
        
        group_information['data']['members_added'] = list(set(group_information['data']['members_added']) | (member_ids - set(not_added_member_ids)))
        
        group_information['data']['extracted_members'][account_information['session_name']] = \
            list((set(group_information['data']['extracted_members'].get(account_information['session_name'], set())) | set(not_added_member_ids)) - \
                (set(group_information['data']['group_members']) | set(group_information['data']['members_added'])))
        
    accounts_manager.dumps_account_information(account_information)
    groups_manager.dumps_group_information(group_information)
    
    try:
        await client.disconnect()
    except Exception as e:
        logger.warning(f"failed to disconnect to the account: {account_information['session_name']}")
        logger.warning(f"error: {e}")
    
    return account_information, stop_execution
    
def start(account_information, group_information):
    client = create_client(account_information)
    response = client.loop.run_until_complete(execute(client, account_information, group_information))
    return response