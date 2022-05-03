from tabulate import tabulate

def createHeaders(headers):
    return [(key, key.replace("_", " ").title()) for key in headers]

def tableView(headers, data, index = False) -> None:
    """
    :param headers: List of header tuples with [name of header, ...]
    :param data: List of dictionary objects containing row data
    :param spaces: Optional argument for defining the ammount of space each column is given
    """
    table = [[row.get(dictKey) for dictKey, printableNames in headers] for row in data]
    print(tabulate(table, headers=[header for _, header in headers], showindex=index, tablefmt="pretty", stralign="center"))



if __name__ == '__main__':
    tableView([("price", "Price"), ("title", "Title"), ("author", "Author")], [{"price": 5.8, "title": "A time to kill", "author": "Grisham"}, {"price": 18.90, "title": "Kid Lawyer", "author": "Grisham"}, {"price": 40, "title": "Helter Skelter", "author": "Gentry"}], index=True)