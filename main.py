import json
import sys

import leclerc
import receipt_parser

with open('complete_receipts3.json', 'r') as file:
    j = json.load(file)
    for receipt in j:
        try:
            data = {
                'emitterCode': receipt['noEmetteur'],
                'ticketDate': receipt['date'],
                'ticketId': receipt['identifiant']
            }
            html = leclerc.get_leclerc(data)
            shopping_list = receipt_parser.parse_ticket(html)

            shopping_list.save()
            print(f"Saved ticket n°{receipt['identifiant']} from {shopping_list.date}")
        except Exception as e:
            print(f"Error while saving ticket n°{receipt['identifiant']}: {e}")
