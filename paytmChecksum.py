from fastapi import FastAPI, Request
import json
from paytmchecksum import PaytmChecksum

app = FastAPI()

# creating path. POST method
@app.post("/PayTmCheckSum")


async def mainFunc(request: Request):
    reqBody = await request.body()
    data = json.loads(reqBody)

    # data of the body
    mode = data["mode"]             # mode - send Request / Check status

    merchant_key = data["merchant_key"]
    paytmTid = data["paytmTid"]
    transactionDateTime = data["transactionDateTime"]
    if mode == "0": transactionAmount = data["transactionAmount"]
    merchantTransactionId = data["merchantTransactionId"]
    paytmMid = data["paytmMid"]
    if mode == "0": autoAccept = data["autoAccept"]

    # creating a json to pass to the checksum generator
    BodyReq = {}
    BodyReq["paytmTid"] = paytmTid
    BodyReq["transactionDateTime"] = transactionDateTime
    if mode == "0": BodyReq["transactionAmount"] = transactionAmount
    BodyReq["merchantTransactionId"] = merchantTransactionId
    BodyReq["paytmMid"] = paytmMid
    if mode == "0": BodyReq["autoAccept"] = autoAccept
    if mode == "0": payMode = data["payMode"]
    if mode == "0": BodyReq["paymentMode"] = payMode


    # calling checksum function
    paytmchecksum = genCheckSum(BodyReq, merchant_key)

    # adding merchantExtendedInfo object
    # if mode == "0":
     #   merchantExtendedInfo = {}
     #   merchantExtendedInfo["paymentMode"] = payMode
     #   merchantExtendedInfo["autoAccept"] = "true"
     #   BodyReq["merchantExtendedInfo"] = merchantExtendedInfo

    if mode == "0":
        merchantExtendedInfo={"autoAccept": "true","paymentMode":payMode}
        BodyReq["merchantExtendedInfo"]=merchantExtendedInfo

    print(BodyReq)

    return {"checksum": paytmchecksum, "reqBody": BodyReq, "merchant_key": merchant_key}


def genCheckSum(body, merchant_key):
    payTMchecksum = PaytmChecksum.generateSignature(body, merchant_key)   # generating checksum
    return payTMchecksum

# uvicorn main:app --host 172.22.1.185 --port 1000 --reload     -- run this

# nohup uvicorn main:app --host 172.22.1.185 --port 1000