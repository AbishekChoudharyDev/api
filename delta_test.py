import requests

headers = {
    'api-key': 'I1zqwnl3vSizkNIVFf7DRhhECxABUm',
    'api-secret': 'Pfwd2Wf2245wgbymCq7U2sOIgt1BglrXPaFxq5DNkRUuXCPAo9FUfl48nbKs'
}

response = requests.get("https://api.delta.exchange/v2/wallet/balances", headers=headers)

print("Status Code:", response.status_code)
print("Response Text:", response.text)