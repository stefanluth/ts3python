def bb_color(text: str, color: str):
    return f"[color={color}]{text}[/color]"


def bb_b(text: str):
    return f"[b]{text}[/b]"


def get_color(amount: int):
    if amount < 500:
        return 'brown'
    elif amount < 1000:
        return 'darkorange'
    elif amount < 3000:
        return 'forestgreen'
    elif amount < 8000:
        return 'royalblue'
    elif amount < 15000:
        return 'hotpink'
    elif amount >= 15000:
        return 'goldenrod'
    return 'black'
