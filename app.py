from flask import Flask, render_template, url_for, request, redirect, jsonify, json, session
from paytmkit import Checksum
import requests
app = Flask(__name__)



MERCHANT_KEY='XXXXXXXXXXXX'
MID = 'XXXXXXXXXXXXXXXXXXXX'
@app.route('/generate_checksumhash',methods=['POST'])
def generate_checksumhash():
    try:
        user_id=request.json['user_id']
        # email_id=request.json['email_id']
        # paytm_no=request.json['paytm_no']
        amount=request.json['amount']
        order_id= request.json['order_id']
        CALLBACK_URL= 'https://securegw-stage.paytm.in/theia/paytmCallback?ORDER_ID='
        user_dict={
            'MID':MID,
            'ORDER_ID':str(order_id),
            'TXN_AMOUNT':str(amount),
            'CUST_ID':str(user_id),
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'APPSTAGING',
            'CHANNEL_ID':'WAP',
            'CALLBACK_URL':CALLBACK_URL+order_id,
            }
        print(user_dict)
        user_dict['CHECKSUMHASH']= Checksum.generate_checksum(user_dict,MERCHANT_KEY)
        print(user_dict['CHECKSUMHASH'])
        return jsonify({'status':'success','result':user_dict})
    except Exception as e:
        return jsonify({'status':'fail','result':str(e)})

@app.route('/verify_checksumhash',methods=['POST'])
def verify_checksumhash():
    try:
        MERCHANT_KEY = 'XXXXXXXXXXX'
        paytmChecksum = ""
        paytmParams={}
        for key, value in paytmParams.items():
            print(key)
            print(value if key == 'CHECKSUMHASH' else 'not found')
            if key == 'CHECKSUMHASH':
                paytmChecksum = value
                print(paytmChecksum)
            else:
                paytmParams[key] = value
                print(paytmParams[key])
        isValidChecksum = Checksum.verify_checksum(paytmParams, MERCHANT_KEY, paytmChecksum)
        print(isValidChecksum)
        if isValidChecksum:
            return jsonify({'status':'success','result':'checksum matched'})
        else:
            return jsonify({'status': 'fail', 'result': 'checksum mismatched'})
    except Exception as e:
        return str(e)

@app.route('/check_transaction',methods=['POST'])
def check_transaction():
    MERCHANT_KEY = 'XXXXXXXXXXXX'
    MID = 'XXXXXXXXXXXXXXXX'
    order_id= request.json['order_id']
    paytmparams={}
    paytmparams['MID']=MID
    paytmparams['ORDERID']=order_id
    checksum= Checksum.generate_checksum(paytmparams,MERCHANT_KEY)
    paytmparams['CHECKSUMHASH']=checksum
    postdata= json.dumps(paytmparams)
    url= "https://securegw-stage.paytm.in/merchant-status/getTxnStatus"
    response= requests.post(url,data=postdata, headers={"Content-type":"application/json"}).json()
    return response


if __name__=='__main__':
    app.run(debug=True)