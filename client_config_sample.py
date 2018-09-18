from kmip.pie.client import ProxyKmipClient

# Setup a client
client = ProxyKmipClient(
    hostname = 'kmip_server_name',
    port = 5696,
    cert = 'ssl/client.crt',
    key = 'ssl/client.key',
    ca = 'ssl/ca-chain.crt',
    config = 'client'
)

