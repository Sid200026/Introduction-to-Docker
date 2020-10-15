from configparser import RawConfigParser

config = RawConfigParser()
config.read("secret.ini")

TOKEN = config.get("SECRET", "TOKEN")
print(TOKEN)
