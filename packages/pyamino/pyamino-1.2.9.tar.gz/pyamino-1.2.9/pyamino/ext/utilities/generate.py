from hmac import new
from hashlib import sha1
from base64 import b64encode
from secrets import token_hex
from typing import Union
import requests
from time import sleep

class Generator:
    def __init__(
        self,
        prefix:        Union[str, int],
        device_key:    str,
        signature_key: str
        ) -> None:
        self.PREFIX = bytes.fromhex(str(prefix))
        self.DEVICE_KEY = bytes.fromhex(device_key)
        self.SIGNATURE_KEY = bytes.fromhex(signature_key)

    def device_id(self) -> str:
        """
        `generate_device_id` Generates a device ID based on a specific string.

        `**Returns**`
        - `str` - Returns a device ID as a string.
        """
        encoded_data = sha1(str(token_hex(20)).encode('utf-8')).hexdigest()

        digest = new(
            self.DEVICE_KEY,
            self.PREFIX + bytes.fromhex(encoded_data),
            sha1).hexdigest()

        return f"{bytes.hex(self.PREFIX)}{encoded_data}{digest}".upper()

    def signature(self, data: str) -> str:
        """
        `signature` Generates a signature based on a specific string.
        
        `**Parameters**`
        - `data` - Data to generate a signature from
        `**Returns**`
        - `str` - Returns a signature as a string.
        """

        signature = [self.PREFIX[0]]  
        signature.extend(new(
            self.SIGNATURE_KEY,
            str(data).encode("utf-8"), sha1).digest())

        return b64encode(bytes(signature)).decode("utf-8")
    
    def update_device(self, device: str) -> str:
        """
        Update a device ID to new prefix.

        :param device: The device ID to update.
        :type device: str
        :return: The updated device ID as a string.
        :rtype: str
        """
        encoded_data = sha1(str(bytes.fromhex(device[2:42])).encode('utf-8')).hexdigest()

        digest = new(
            self.DEVICE_KEY,
            self.PREFIX + bytes.fromhex(encoded_data),
            sha1).hexdigest()

        return f"{bytes.hex(self.PREFIX)}{encoded_data}{digest}".upper()
    
    def NdcMessageSignature(self, KEY: str, data: str, sid: str, deviceid: str) -> Union[str, None]:
        if KEY is None:
            Exception("Missing service key. Please get it on the official Pymino channel. https://t.me/pymino.")
        
        if sid is None or deviceid is None:
            return None
        
        response = requests.post(
            url="https://app.friendify.ninja/api/v1/pymino",
            headers={
                "SID": sid,
                "NDCDEVICEID": deviceid,
                "KEY": KEY
            },
            data=str(data).encode("utf-8")
        )
        if response.status_code == 200:
            return response.text
        if response.status_code == 403:
            return self.NdcMessageSignature(
                data=data,
                sid=sid,
                deviceid=deviceid,
                KEY=KEY
            )
        if response.status_code == 503:
            print(response.text)
            sleep(3)
            return self.NdcMessageSignature(
                data=data,
                sid=sid,
                deviceid=deviceid
            )
        else:
            raise Exception(
                response.text
            )