# Video Analytics Service

This project hosts the artifacts to build and use video analytics service used in Edge Insights Vision (Microservices) and Edge Insights Industrial.

## Building the image 

- To build the base image, run the following command
     `docker-compose -f  docker-compose-build.yml  build`

## Running the image


### In EIV context

- Clone this repo.

- Make the following files executable

    `chmod +x tools/model_downloader/model_downloader.sh docker/run.sh`

- Download the required models. From the cloned repo, run the following commands. 

    `./tools/model_downloader/model_downloader.sh  --model-list <Path to model-list.yml>`

- After downloading the models, you will have models directory in the base folder.

```
models/
├── action_recognition
├── audio_detection
├── emotion_recognition
├── face_detection_retail
├── object_classification
└── object_detection
```

- Add the following lines in the docker-compose.yml environment if you are behind a proxy.

```
    - HTTP_PROXY=<IP>:<Port>/
    - HTTPS_PROXY=<IP>:<Port>/
    - NO_PROXY=localhost,127.0.0.1
```

- Run `sudo docker-compose up`.



