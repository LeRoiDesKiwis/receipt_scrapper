import re
import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
from datetime import datetime

from model import ShoppingList, Product

from bs4 import BeautifulSoup

def parse_ticket(html1):

    soup = BeautifulSoup(html1, features="lxml")
    html = soup.get_text().replace("\n\n", "")
    #get the first line without using regex
    lines = html.split("\n")
    location = lines[0].replace("E.Leclerc", "").strip()
    #Exemple de ligne Caisse 513-5013 17 octobre 2024 14:58
    #find date using regex
    date = None
    for line in lines:
        if re.search(r"(\d{1,2}\s+[a-zéû]+\s+\d{4}\s+\d{2}:\d{2})", line) is not None:
            date_ = re.search(r"(\d{1,2}\s+[a-zéû]+\s+\d{4}\s+\d{2}:\d{2})", line).group(1)
            date = datetime.strptime(date_, "%d %B %Y %H:%M")
            break
    receipt = html[re.search("(TVA|TTC)", html).end():]
    receipt = receipt[:receipt.find("----")]

    shopping_list = ShoppingList(location, date)

    # Séparation en lignes
    lines = receipt.split('\n')
    current_name = None

    for line in lines:
        line = line.strip()

        # Si la ligne contient X et €, c'est une ligne de prix avec quantité
        if 'X' in line and '€' in line:
            quantity = int(re.search(r'(\d+)\s*X', line).group(1))
            price = float(re.search(r'(\d+[.,]\d+)', line).group(1).replace(',', '.'))

            # Créer quantity instances du produit
            for _ in range(quantity):
                product = Product(
                    name=current_name.strip(),
                    price=price,
                    garantie=False  # ou une valeur par défaut
                )
                shopping_list.products.append(product)

        # Si la ligne contient € mais pas X, c'est un produit unique
        else:
            if line.startswith("("):
                continue
            current_name = line
            price = re.search(r'(\d+[.,]\d+)', line)
            if price is None:
                continue
            price = float(price.group(0).replace(',', '.'))
            real_name = re.search(r'(.+)\d+[.,]\d+', line).group(1)
            product = Product(
                name=real_name,
                price=price,
                garantie=False
            )
            shopping_list.products.append(product)

    return shopping_list