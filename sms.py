import logging
import re
import requests

SMS_API_URL = "https://api.smsagent.rs/v1/sms/bulk"
SMS_API_KEY = "0LXkwBwCOX7UgdOdyP5v6kjm7PdDJ4FzzycFDIWvY4jg8VaoKlDvSmxZXaauYL3eP6Q71Qpq10Es94vUMUznXJVIOjI26YhzC3RcG7vBVXCAsPq5Cx6LJW2cu3eJ20ha"


def format_phone_number(phone_num):
    """
    Formats a phone number by removing all non-digit characters and adding a country code if necessary.

    Args:
        phone_num (str or int): The phone number to format.

    Raises:
        ValueError: If the input phone number is invalid (i.e. has less than 7 digits).

    Returns:
        str: The formatted phone number.
    """
    # Remove all non-digit characters
    phone_num = re.sub(r'\D', '', str(phone_num))

    # Add the country code if necessary
    if phone_num.startswith('0'):
        phone_num = '+381' + phone_num[1:]

    # Validate the phone number
    if len(phone_num) < 7:
        raise ValueError('Invalid phone number')

    return phone_num


def send_sms_messages(recipient_list):
    """
    Sends SMS messages to a list of recipients using the SMSAgent API.

    Args:
        recipient_list (list[str]): List of phone numbers to send SMS messages to.

    Returns:
        bool: True if messages were sent successfully, False otherwise.
    """

    # TODO: remove in production
    recipient_list = [phone_num for phone_num in recipient_list if phone_num == '+381677019917']

    # Create payload with recipient list and message content
    payload = {
        "to": recipient_list,
        "message": "Proslavite sa nama svoj NAJBOLJI SPORTSKI ROĐENDAN prilagođen uzrastu uz sportske igre, survivor poligone i Pena-žurku! \n\n+381642748571 \nwww.activitycentar.com",
        "from": "SMSAgent",
        "type": "INFO"
    }

    # Set headers with API key and content type
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SMS_API_KEY}"
    }

    # Send POST request to SMSAgent API and handle errors using logging
    response = requests.request("POST", SMS_API_URL, json=payload, headers=headers)
    if not (200 <= response.status_code < 300):
        logging.error(f"Error sending SMS messages to {recipient_list}: {response.status_code} - {response.text}")
        return False

    # Log successful API calls
    logging.info(f"Successfully sent SMS messages to {recipient_list}")
    return True
