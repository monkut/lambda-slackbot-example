# lambda-slackbot-example

This is an example of how to get started with a slackbot with AWS lambda through [zappa](https://github.com/Miserlou/Zappa).

## Prepare local development environment

```
pipenv sync --dev
```

## zappa initial setup

1. create initial zappa_settings file:

    > Populate ${BUCkET_NAME} with a name like, tobor-zappa-SOMERANDOMSTRING 
    > The bucket will be created on deploy.
    > Populate ${SLACK_TOKEN} with token obatined from https://api.slack.com/tokens

    ```
    {
        "dev": {
            "aws_region": "us-west-2",
            "profile_name": "default",
            "project_name": "tobor",
            "runtime": "python3.6",
            "s3_bucket": "${BUCKET_NAME}",
            "apigateway_enabled": false,
            "keep_warm": false,
            "environment_variables": {
                "SLACK_API_TOKEN": "${SLACK_TOKEN}"
            },
            "events": [{
               "function": "tobor.event_handlers.post_random_quote",
               "expression": "cron(0 0 ? * MON,WED,FRI *)"
            }]
        }
    }
    
    ```
    
2. Deploy application for the first time through zappa:

    > NOTE: Your defined profile must have the proper permissions in order to deploy the lambda function and related resources.
    
    ```
    # from the pipenv shell
    zappa deploy
    Calling deploy for stage dev..
    Creating tobor-dev-ZappaLambdaExecutionRole IAM Role..
    Creating zappa-permissions policy on tobor-dev-ZappaLambdaExecutionRole IAM Role.
    Downloading and installing dependencies..
     - sqlite==python36: Using precompiled lambda package
    Packaging project as zip.
    Uploading tobor-dev-1544627201.zip (5.4MiB)..
    100%|████████████████████████████████████████████████████████████████████████████████████████| 5.61M/5.61M [00:04<00:00, 1.22MB/s]
    Scheduling..
    Scheduled tobor-dev-tobor.event_handlers.post_random_quote with expression cron(0 0 ? * MON,WED,FRI *)!
    Deployment complete!
    ```


