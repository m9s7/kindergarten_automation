def convert_phone_num_to_valid_format(phone_num):
    phone_num = [c for c in phone_num if str.isdigit(c)]

    if phone_num[0] == '0':
        phone_num[0] = '+381'

    return "".join(phone_num)


def send_sms_messages(recipient_list):
    import requests

    url = "https://api.smsagent.rs/v1/sms/bulk"

    # TODO: remove in production
    recipient_list = [phone_num for phone_num in recipient_list if phone_num == '+381677019917' or phone_num == '+381652248294']

    payload = {
        "to": recipient_list,
        "message": "hello",
        "from": "SMSAgent",
        "type": "INFO"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 0LXkwBwCOX7UgdOdyP5v6kjm7PdDJ4FzzycFDIWvY4jg8VaoKlDvSmxZXaauYL3eP6Q71Qpq10Es94vUMUznXJVIOjI26YhzC3RcG7vBVXCAsPq5Cx6LJW2cu3eJ20ha"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    if not (200 <= response.status_code < 300):
        print("Poruke za sledecu grupu nisu poslate: ")
        print(recipient_list)
        print(response.status_code, response.text)
