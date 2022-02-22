EII DLStreamer Pipeline Server Microservice
===========================================

The EII DLStreamer Pipeline Server Microservice wraps the DLStreamer Pipeline Server
library to provide an EII visual ingestion and analytics module utilizing the
features and functionality of the library.

## Building

The Docker container for this service cannot be built by itself. It must be
built in the context of the EII multi-repo project. Follow the instructions
[here](https://github.com/open-edge-insights/eii-manifests).

Since the model files are large in size, they are not part of the repo.
Download the required model files to be used for the pipeline mentioned in
[config](./config.json) by referring https://github.com/dlstreamer/pipeline-server/tree/master/tools/model_downloader.
Please ensure below pre-requisite steps are run to get the example pipelines
working by referring https://github.com/dlstreamer/pipeline-server/blob/master/README.md

```sh
./docker/build.sh

./docker/run.sh -v /tmp:/tmp

./vaclient/vaclient.sh list-pipelines
```

## Running

Please follow the steps mentioned below to run the DLStreamer Pipeline Server service

```sh
cd [WORK_DIR]/IEdgeInsights/build

# Execute the builder.py script
python3 builder.py -f usecases/evas.yml

# Create some necessary items for the service
sudo mkdir -p /opt/intel/eii/models/

# Copy the downloaded model files to /opt/intel/eii
sudo cp -r models /opt/intel/eii/

# Build the docker containers
docker-compose -f docker-compose-build.yml build

# Start the docker containers
docker-compose up -d
```

This repository provides the VA Serving pipeline needed for using a URI source
and sending the ingested frames using the EII MsgBus Publisher. The commands above
which create the, "models/", directory and the, "pipelines/", install needed
directories for the service to run and install the VA Serving pipeline.

## Configuration

Please see the `config.json` file for the configuration of the service. The
default configuration will start the object_detection demo for EII.

The table below describes each of the configuration attributes currently
supported.

> **TODO:** Need to document these parameters much more.

|      Parameter      |                                                     Description                                                |
| :-----------------: | -------------------------------------------------------------------------------------------------------------- |
| `source`            | Source of the frames, must be `"gstreamer"` or `"msgbus"`.                                                    |
| `source_parameters` | The parameters for the source element. The provided object is the typical parameters.                          |
| `pipeline`          | The name of the VA Serving pipeline to use (should correspond to a directory in the pipelines directory).      |
| `pipeline_version`  | The version of the pipeline to use. This typically is a subdirectory of a pipeline in the pipelines directory. |
| `publish_frame`     | Boolean flag for whether to publish the meta-data and the analyzed frame, or just the meta-data.               |
| `model_parameters`  | Provides the parameters for the model if DL streamer is being used in the VA Serving pipeline.                 |

### Configuring the Interfaces

The service only supports launching a single pipeline and publishing on a
single topic currently. This means, in the configuration file ("config.json"),
the single JSON object in the `Publisher` list is where the configuration
resides for the published data. See the EII documentation for more details on
the structure of this.

### Configuring EII subscriber and publisher

This service also supports subscribing and publishing messages/frames using the
EIIMessageBus.
The endpoint details for the EII service you need to subscribe from is to be
provided in the **Subscribers** section in [config](config.json) and the endpoints
where you need to publish to are to be provided in **Publishers** section in
[config](config.json).

For enabling injection of frames into the GStreamer pipeline obtained from
EIIMessageBus, please ensure the following changes are done:

* The source parameter in [config](config.json) is set to msgbus
 
 ```javascript
    "config": {
        "source": "msgbus"
    }
 ```

* The template of respective pipeline is set to appsrc as source instead of uridecodebin

```javascript
    {
        "type": "GStreamer",
        "template": ["appsrc name=source",
                     " ! rawvideoparse",
                     " ! appsink name=destination"
                    ]
    }
```

