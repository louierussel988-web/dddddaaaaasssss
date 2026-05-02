Fork this repo then Settings > Actions > General > Check the read and write permissions under the Workflow permissions section
You need to get your account's API_ID and API_HASH from https://my.telegram.org/auth?to=apps
Go to Settings > Secrets and variables > Actions and make two repository secrets:
      key: API_ID, value: your api_id which looks like 4123213
      key: API_HASH, value: your api_hash which looks like a21bcedeaf44...

Now you need to 
