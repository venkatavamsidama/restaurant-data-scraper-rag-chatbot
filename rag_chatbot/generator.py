import re

class Generator:
    def __init__(self):
        pass  # No LLM needed for price lookup!

    def generate(self, query: str, context: str = "") -> str:
        query = query.lower()

        # Extract menu items from context
        menu_items = self.parse_menu(context)

        # Try to find the matching item
        for item_name, price in menu_items.items():
            if all(word in item_name.lower() for word in query.split()):
                return f"The price of {item_name} is ₹{price}"

        return "Sorry, I couldn't find the price for that item."

    def parse_menu(self, context: str):
        """
        Parses the menu into a dict: { item_name: price }
        Example:
          "Veggie Wrap: 549 Aloo Paratha: 129" --> { "Veggie Wrap": 549, "Aloo Paratha": 129 }
        """
        menu = {}
        pattern = r'([A-Za-z ]+): (\d+)'
        matches = re.findall(pattern, context)

        for name, price in matches:
            menu[name.strip()] = int(price)

        return menu
