"""Cafeteria menu and daily specials.
Prints the fixed menu with a loop, then asks for a day of the week and uses conditionals to decide which item is the special."""
MENU = [
    ("Tomato Soup", 3.50),
    ("Grilled Cheese Sandwich", 4.25),
    ("Veggie Wrap", 5.00),
    ("Chicken Curry", 6.75),
    ("Fish and Chips", 7.50),
    ("Garden Salad", 4.00),
    ("Apple Pie", 2.25),
]


def menu_lines():
    """Build one text line per menu item, e.g. 'Tomato Soup      $3.50'."""
    lines = []
    for name, price in MENU:
        lines.append(f"{name:<25}${price:.2f}")
    return lines


def print_menu():
    """Print the whole menu, one item per line."""
    print("=== Cafeteria Menu ===")
    for line in menu_lines():
        print(line)


def price_of(item_name):
    """Return the menu price of item_name, or 0.0 if it is not on the menu."""
    for name, price in MENU:
        if name == item_name:
            return price
    return 0.0


def find_special(day):
    """Return (item name, discount) for a day, or (None, 0.0) if there is none.

    The discount is always a float, so 0.20 means 20% off.
    """
    chosen = day.strip().lower()
    if chosen == "monday":
        return ("Tomato Soup", 0.20)
    elif chosen == "tuesday":
        return ("Grilled Cheese Sandwich", 0.10)
    elif chosen == "wednesday":
        return ("Veggie Wrap", 0.15)
    elif chosen == "thursday":
        return ("Chicken Curry", 0.25)
    elif chosen == "friday":
        return ("Fish and Chips", 0.30)
    else:
        return (None, 0.0)


def discounted_price(price, discount):
    return round(price * (1.0 - discount), 2)


def main():
    print_menu()
    day = input("Enter a day of the week: ")

    item, discount = find_special(day)
    if item is None:
        print("No special today.")
    else:
        full_price = price_of(item)
        sale_price = discounted_price(full_price, discount)
        print(f"Today's special: {item}")
        print(f"Was ${full_price:.2f}, now ${sale_price:.2f}")

    print("Discount value:", discount)
    print("Discount type:", type(discount))


if __name__ == "__main__":
    main()
