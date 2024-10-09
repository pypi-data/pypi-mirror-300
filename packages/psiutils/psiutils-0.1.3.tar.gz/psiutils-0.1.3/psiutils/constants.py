"""Constants for the tkinter psiutils."""
if __name__ == 'main':
    from utilities import invert
else:
    from .utilities import invert

DIALOG_STATUS = {
#DIALOG_STATUS: dict[int, str] | dict[str, int] | dict[bool, str] | dict[str, bool] = {
    'yes': True,
    'no': False,
    'cancel': None,
    'null': 0,
    'exit': 1,
    'ok': 2,
    'updated': 3,
    'error': 4,
}
DIALOG_STATUS = invert(DIALOG_STATUS)

# GUI
PAD = 5
PADR = (0, PAD)
PADT = (PAD, 0)
PADB = (0, PAD)
LARGE_FONT = ('Arial', 16)

# Geometry is WxH
