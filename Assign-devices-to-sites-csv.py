# --------Authenticate to DNA, Retrieve or Update Inventory ------
import requests
import json

dnac = ""
username = ""
password = ""


def get_token(username, password):

    # Get API Token from DNAC
    url = f"https://{dnac}/dna/system/api/v1/auth/token"
    headers = {"Content-Type": "application/json"}
    auth = (username, password)
    auth_resp = requests.post(url, auth=auth, headers=headers, verify=False)
    auth_resp.raise_for_status()
    token = auth_resp.json()["Token"]
    return token


def get_inventory(api_path, token):
    headers = {"Content-Type": "application/json", "X-Auth-Token": token}
    get_resp = requests.get(
        f"https://{api_path}/dna/intent/api/v1/network-device", headers=headers, verify=False)

    # raw_output IS A DICTIONARY. TAKE THE VALUE OF response AND ASSIGN TO devices
    raw_output = json.loads(get_resp.text)\
    #print(raw_output)
    devices = raw_output["response"]

    outputFile = open("output.csv", "w+")

    colStr = "Hostname, Management IP, DeviceID, Location, SerialNumber"
    print(colStr)
    outputFile.write(colStr + "\n")

    if get_resp.ok:
        for device in devices:

            rowStr = (str(device["hostname"]) + "," +
                     str(device["managementIpAddress"]) + "," +
                     str(device['id']) + "," +
                     str(device["snmpLocation"]) + "," +
                     str(device["serialNumber"]))
            print(rowStr)
            outputFile.write(rowStr + "\n")
    else:
        print(f"Device collection failed with code {get_resp.status_code}")
        print(f"Failure body: {get_resp.text}")

    outputFile.close()


if __name__ == "__main__":
    dnac = "xx.xx.xx.xx"
    username = "admin"
    password = "yyyy"
    # dnac = input("Please provide Cisco DNA Center target IP Address: ")
    # username = input("Please provide Cisco DNA Center username: ")
    # password = input("Please provide Cisco DNA Center password: ")
    token = get_token(username, password)
    # print(token)
    if token == None:
        print("Token collection failed! \n \n \n Please check connectivity to Cisco DNAC IP, Username and Password and try again ")
        exit()
    else:
        pass

    inventory = get_inventory(dnac, token)
