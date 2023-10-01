# awsiot-laptop-soc
This repo is a demo to upload the charging state of my Linux machine
to AWS using Greengrass on my PC. Greengrass is an IoT Linux application
to interact with AWS IoT infrastructure.

## Components Used
- aws.greengrass.Nucleus
- aws.greengrass.clientdevices.mqtt.Bridge
- PCstats4 (custom component)

## Minimal Configurations
It's assumed you have an AWS account.

### PCstats4 Reciepe on Component Creation
```
{
  "RecipeFormatVersion": "2020-01-25",
  "ComponentName": "<YOUR CUSTOM NAME>",
  "ComponentVersion": "1.0.0",
  "ComponentType": "aws.greengrass.generic",
  "ComponentDescription": "<EDIT ME>",
  "ComponentPublisher": "<EDIT ME>",
  "ComponentConfiguration": {
    "DefaultConfiguration": {
      "Message": "<NOT USED>",
      "accessControl": {
        "aws.greengrass.ipc.access": {
          "com.PCstats4": {
            "policyDescription": "Allows access to publish to HP/eyi/telemetry.",
            "operations": [
              "aws.greengrass#PublishToTopic",
              "aws.greengrass#PublishToIoTCore"
            ],
            "resources": [
              "HP/eyi/telemetry"
            ]
          }
      }
    }
  },
  "ComponentDependencies": {
    "aws.greengrass.TokenExchangeService": {
      "VersionRequirement": ">=2.0.0 <3.0.0",
      "DependencyType": "HARD"
    }
  },
  "Manifests": [
    {
      "Platform": {
        "os": "linux"
      },
      "Name": "Linux",
      "Lifecycle": {
        "Run": "python3 {artifacts:path}/<FILE NAME OF YOUR CODE IN AMAZON S3>"
      },
      "Artifacts": [
        {
          "Uri": "<URI OF YOUR CODE IN AMAZON S3>"
        }
       ]
    }
   ]
}
```

### aws.greengrass.Nucleus configuration
```
{
  "reset": [],
  "merge": {
    "iotRoleAlias": "GreengrassV2TokenExchangeRoleAlias",
    "awsRegion": "us-east-1",
    "iotCredEndpoint": "<YOUR-CREDENTIAL-ENDPOINT>.credentials.iot.us-east-1.amazonaws.com",
    "iotDataEndpoint": "<YOUR-DATA-ENDPOINT>-ats.iot.us-east-1.amazonaws.com",
    "runWithDefault": {
      "posixUser": "ggc_user:ggc_group"
    }
  }
}
```

## aws.greengrass.clientdevices.mqtt.Bridge configuration
```
{
  "reset": [],
  "merge": {
    "mqttTopicMapping": {
      "map1": {
        "topic": "HP/eyi/telemetry",
        "source": "LocalMqtt",
        "target": "IotCore"
      },
      "map2": {
        "topic": "HP/eyi/telemetry",
        "source": "Pubsub",
        "target": "IotCore"
      }
    }
  }
}
```
