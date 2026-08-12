import re

LIST_PATTERN = re.compile(
    rb"^\((?P<flags>.*?)\)\s+" rb"(?P<separator>\".*?\"|NIL)\s+" rb"(?P<name>.*)$"
)
