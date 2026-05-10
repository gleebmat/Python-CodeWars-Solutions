def calculate (quantity, price):
    """Calculate total price for given quantity and price."""
    return quantity * price

def format_currency(amount):
    """Format a number as currency."""
    return f"${amount:,.2f}"