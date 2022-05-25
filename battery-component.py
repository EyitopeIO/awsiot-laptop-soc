# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

"""
This sample uses AWS IoT Greengrass v2 to publish messages from the device to
the AWS IoT Core MQTT broker.

This example can be deployed as Greengrass v2 component and it will start
publishing telemetry data as MQTT messages in periodic intervals. The IPC
integration with Greegrass v2 allows this code to run without additional IoT
certificates or secrets, because it directly communicates with Greengrass Core
on the device.

"""

import json
import time
import os

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

if __name__ == '__main__':
    ipc_client = awsiot.greengrasscoreipc.connect()

    while True:
    	# _, _, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])

        telemetry_data = {
            "ram": "n/a",
            "soc": open("/sys/class/power_supply/BAT0/status","r").readline().strip(),
            "tnw": int(round(time.time() * 1000))
        }
        
        op = ipc_client.new_publish_to_iot_core()
        op.activate(model.PublishToIoTCoreRequest(
            topic_name="HP/eyi/telemetry",
            qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(telemetry_data).encode(),
        ))
        try:
            result = op.get_response().result(timeout=5.0)
            print("successfully published message:", result)
        except Exception as e:
            print("failed to publish message:", e)

        time.sleep(5)
