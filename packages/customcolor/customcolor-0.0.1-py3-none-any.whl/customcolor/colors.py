from enum import Enum

class TextColor(Enum):
	RED = "\u001b[31m"
	GREEN = "\u001b[32m"
	YELLOW = "\u001b[33m"
	RESET = "\u001b[0m"


def _color_text(text: str, color: TextColor):
	return color.value + text + TextColor.RESET.value

def red(text: str):
	return _color_text(text, TextColor.RED)

def green(text: str):
	return _color_text(text, TextColor.GREEN)

def yellow(text: str):
	return _color_text(text, TextColor.YELLOW)
