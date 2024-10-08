import variables
from MrLou_modules.Certificate_Utils.cert_utils import extract_common_name, extract_san_extension
from MrLou_modules.Cyberark.cyberark_api import CyberArkAPI


cyberark_api = CyberArkAPI(variables)
credentials = cyberark_api.get_credentials()

if credentials:
    usr = credentials['Username'].split("\\")[1]
    print(f"Username: {usr}")
    print(f"Password: {credentials['Password']}")
    print(f"Password Change In Process: {credentials['PasswordChangeInProcess']}")

# ca_username = ca_account['UserName'].split("\\")[1]
