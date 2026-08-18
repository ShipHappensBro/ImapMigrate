import re

# Регулярное выражение для разбора ответа IMAP LIST:
# flags, separator и name.
LIST_PATTERN = re.compile(
    rb"^\((?P<flags>.*?)\)\s+"
    rb"(?P<separator>\".*?\"|NIL)\s+"
    rb"(?P<name>.*)$"
)