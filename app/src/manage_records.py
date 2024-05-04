import requests
import logging
import time
import json

logger = logging.getLogger(__name__)


def update_records(ipaddr: str, id: str, ip6addr: str, id6: str, zone: str, token: str, ttl: str=60):
    try:
        response = requests.put(
            url=f"https://dns.hetzner.com/api/v1/records/bulk",
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": f"{token}",
            },
            data=json.dumps({
                "records": [
                    {
                        "id": f"{id}",
                        "value": f"{ipaddr}",
                        "ttl": 60,
                        "type": "A",
                        "name": "*",
                        "zone_id": f"{zone}"
                    },
                    {
                        "id": f"{id6}",
                        "value": f"{ip6addr}",
                        "ttl": 60,
                        "type": "AAAA",
                        "name": "*",
                        "zone_id": f"{zone}"
                    }
                ]
            })
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making API request to {url}: {e}")
        # Retry logic
        retries = 3
        for attempt in range(retries):
            try:
                logger.info(f"Retrying API request (attempt {attempt + 1}/{retries})...")
                response = requests.put(
                    url=f"https://dns.hetzner.com/api/v1/records/bulk",
                    headers={
                        "Content-Type": "application/json",
                        "Auth-API-Token": f"{token}",
                    },
                    data=json.dumps({
                        "records": [
                            {
                                "id": f"{id}",
                                "value": f"{ipaddr}",
                                "ttl": f"{ttl}",
                                "type": "A",
                                "name": "*",
                                "zone_id": f"{zone}"
                            },
                            {
                                "id": f"{id6}",
                                "value": f"{ip6addr}",
                                "ttl": f"{ttl}",
                                "type": "AAAA",
                                "name": "*",
                                "zone_id": f"{zone}"
                            }
                        ]
                    })
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Retry attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    # Exponential backoff: Wait before retrying
                    wait_time = 2 ** attempt
                    logger.info(f"Waiting {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                else:
                    raise  # Retry limit reached, propagate the exception