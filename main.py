import json
import sys

import leclerc
import receipt_parser

with open('complete_receipts.json', 'r') as file:
    j = json.load(file)
    for receipt in j:
        data = {
            'emitterCode': receipt['noEmetteur'],
            'ticketDate': receipt['date'],
            'ticketId': receipt['identifiant']
        }
        html = leclerc.get_leclerc(data)
        if html is None:
            print(f"Failed to parse ticket n°{receipt['identifiant']} from {receipt['date']}", file=sys.stderr)
            continue
        shopping_list = receipt_parser.parse_ticket(html)

        shopping_list.save()
        print(f"Saved ticket n°{receipt['identifiant']} from {shopping_list.date}")