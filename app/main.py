from fastapi import FastAPI
from app.src.manage_records import update_records
from app.src.load_config import get_variable

app = FastAPI()

config_path = 'app/config/.config'

api_key = get_variable(config_path, 'API_KEY')
zone_id = get_variable(config_path, 'ZONE_ID')
id = get_variable(config_path, 'ID')
id6 = get_variable(config_path, 'ID6')

@app.get("/update")
async def update_ip(ipaddr: str, ip6addr: str):
    update_records(ipaddr=ipaddr, id=id,  ip6addr=ip6addr, id6=id6, zone=zone_id, token=api_key)

    return {"ipaddr": ipaddr, "ip6addr": ip6addr}