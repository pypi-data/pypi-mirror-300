import json
import requests
import subprocess


DUYO_USER_KEY = "df2d8853-2e0f-48dd-b167-10183c491e72"

def validate_license_by_key(license_key, product_id):
    res = requests.post(
        f"https://api.keygen.sh/v1/accounts/{DUYO_USER_KEY}/licenses/actions/validate-key",
        headers={
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
        },
        data=json.dumps({
            "meta": {
                "key": license_key,
                "scope": {
                    "product": product_id
                }
            }
        })
    ).json()

    if res["meta"]["code"] == "VALID":
        return res["data"]["id"]
    elif res["meta"]["code"] in ["PRODUCT_SCOPE_MISMATCH", "NOT_FOUND", "EXPIRED"]:
        raise Exception(res["meta"]["code"])
    else :
        raise Exception("UNKNOWN_ERROR") 

def retrieve_machine(license_key, machine_id):
    res = requests.get(
        f"https://api.keygen.sh/v1/accounts/{DUYO_USER_KEY}/machines/{machine_id}",
        headers={
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"License {license_key}" # by license authentication
        }
    )
    print('retrieve_machine')
    print(res)
    if res.status_code == 200 :
        return True
    else :
        return False

def validate_license_with_machine_id(license_key, product_id, machine_id):
    res = requests.post(
        f"https://api.keygen.sh/v1/accounts/{DUYO_USER_KEY}/licenses/actions/validate-key",
        headers={
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
        },
        data=json.dumps({
            "meta": {
                "key": license_key,
                "scope": {
                    "product": product_id,
                    "fingerprint": machine_id
                }
            }
        })
    ).json()

    if res["meta"]["code"] == "VALID":
        return res
    elif res["meta"]["code"] in ["FINGERPRINT_SCOPE_MISMATCH", "NOT_FOUND", "PRODUCT_SCOPE_MISMATCH"]:
        raise Exception(res["meta"]["code"])
    else :
        raise Exception("UNKNOWN_ERROR")

def create_machine(license_key, license_id, machine_id):
    res = requests.post(
        f"https://api.keygen.sh/v1/accounts/{DUYO_USER_KEY}/machines",
        headers={
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "Authorization": f"License {license_key}" # by license authentication
        },
        data=json.dumps({
            "data": {
                "type": "machines",
                "attributes": {
                    "fingerprint": machine_id
                },
                "relationships": {
                    "license": {
                        "data": {
                            "type": "licenses",
                            "id": license_id
                        }
                    }
                }
            }
        })
    )

    if res.status_code == 201:
        return True
    else:
        raise Exception(res.json()["errors"][0]["code"])

def check_license(license_key="", product_id=""):
    if license_key == "":
        return {
            "valid": False,
            "code": "EMPTY_LICENSE_KEY",
        }
    if product_id == "":
        return {
            "valid": False,
            "code": "EMPTY_PRODUCT_ID",
        }

    def get_windows_machine_id():
        command = "wmic csproduct get uuid"
        output = subprocess.check_output(command, shell=True).decode()
        uuid = output.split('\n')[1].strip()
        return uuid
    machine_id = get_windows_machine_id()

    try:
        license_id = validate_license_by_key(license_key, product_id)
    except Exception as e:
        return {
            "valid": False,
            "code": e,
        }
    
    # if machine already exists (already verfied)
    if retrieve_machine(license_key, machine_id):
        try :
            license = validate_license_with_machine_id(license_key, product_id, machine_id)
            return {
                "valid": True,
                "code": "EXISTING_MACHINE_VALIDATED",
                "key": license["data"]["attributes"]["key"],
                "product_id": license["data"]["relationships"]["product"]["data"]["id"],
                "expiry": license["data"]["attributes"]["expiry"],
                "status": license["data"]["attributes"]["status"],
                "maxMachines": license["data"]["attributes"]["maxMachines"],
                "currentMachines": license["data"]["relationships"]["machines"]["meta"]["count"],
                "created": license["data"]["attributes"]["created"],
                "userName": license["data"]["attributes"]["name"],
            }
        except Exception as e:
            return {
                "valid": False,
                "code": e,
                "key": license_key,
                "product_id": product_id,
            }
    # machine does not exist (initial verification) 
    else :
        try :
            create_machine(license_key, license_id, machine_id)
            return {
                "valid": True,
                "code": "NEW_MACHINE_VALIDATED",
                "key": license["data"]["attributes"]["key"],
                "product_id": license["data"]["relationships"]["product"]["data"]["id"],
                "expiry": license["data"]["attributes"]["expiry"],
                "status": license["data"]["attributes"]["status"],
                "maxMachines": license["data"]["attributes"]["maxMachines"],
                "currentMachines": license["data"]["relationships"]["machines"]["meta"]["count"],
                "created": license["data"]["attributes"]["created"],
                "userName": license["data"]["attributes"]["name"],
            }
        except Exception as e:
            return {
                "valid": False,
                "code": e,
                "key": license_key,
                "product_id": product_id,
            }