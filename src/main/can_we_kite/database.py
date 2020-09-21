from influxdb import InfluxDBClient


def get_client():
    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('can_we_kite')
    client.switch_database('can_we_kite')
    return client
