# Runpod Training serverless API for LoRA Dreambooth on Aurawave

##### 📢 Info: The most of code in this repository is from [Simpletuner](https://github.com/bghira/SimpleTuner). Thanks for [bghira](https://github.com/bghira)'s contribution. Refer original Simpletuner's [README.md](README.simpletuner.md)

## Key dependencies

#### NVIDIA RTX A6000 or greater

#### Python 3.10 and 3.11

#### Cuda 11.8

## How to run

### Rename .env.example to .env and set up values

### Test on local

```bash
$ sudo nano test_input.json
```

#### Example test data

```
{
  "input": {
    "s3_dataset_bucket": "aurawave-users-portraits",
    "s3_dataset_folder": "Joshua-1731319691495"
  }
}
```

```bash
$ python index.py
```

### Deploy to runpod

- Edit configuration at [config/config.env](config/config.env) and [config/multidatabackend.json](config/multidatabackend.json)

- Build docker image and push to docker hub.

- Set up docker credential on runpod if you pushed to private docker repo.

- Create a new runpod template with your docker repo.

- Enjoy your training with runpod webhook api.
