def format_phone(phone):

    if phone and len(phone) == 11 and phone.startswith("7"):
        return f"+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}"

    return phone