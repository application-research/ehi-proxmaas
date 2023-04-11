from maas.client import connect
import configparser
from os.path import expanduser

config = configparser.ConfigParser()
config.read(expanduser("~/.proxmox-maas.cfg"))

client = connect("https://maas.estuary.tech/MAAS", apikey=config["maas_api"]["api_key"])
