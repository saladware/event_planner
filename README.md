# event_planner

Web application for assigning events and mentioning them to the user in telegram. Developed during the Rosatom Labs

<!-- TOC -->
* [event_planner](#event_planner)
  * [How to configure](#how-to-configure)
  * [How to run](#how-to-run)
  * [How to start](#how-to-start)
    * [Create user](#create-user)
    * [Create Event](#create-event)
<!-- TOC -->

## How to configure
To start a project, you need to configure it. To do this, you need to define these environment variables:

| Variable name       | Description                             | Value                                                                           |
|---------------------|-----------------------------------------|---------------------------------------------------------------------------------|
| `POSTGRES_USER`     | database user name                      | like `postgres`                                                                 |
| `POSTGRES_PASSWORD` | database user password                  | not like `qwerty1234`                                                           |
| `POSTGRES_DB`       | database name                           | any reasonable                                                                  |
| `DB_HOST`           | database host (in docker container )    | recommend `db`                                                                  |
| `DB_PORT`           | database port (in docker container )    | recommend `5432`                                                                |
| `SECRET_KEY`        | secret key for generation user tokens   | copy from `openssl rand -hex 32` and paste                                      |
| `BOT_TOKEN`         | telegram bot token                      | create telegram bot at [@BotFather](https://t.me/BotFather) and paste its token |
Of course there is support .env files. You can just rename the .env.example file to .env and edit it with your data (it's better not to check what will happen if you don't change this file)

## How to run
After configuration, you can run the app together with its environment in docker. To do this, clone the project, go to the root directory and up the containers (at the first launch, the application may display errors about problems with connecting to the database. do not worry, this is due to the fact that the database does not have time to initialize)

```commandline
git clone https://github.com/saladware/event_planner.git
cd event_planner
docker-compose up --build
```

## How to start

### Create user
To start working with the API, you need to create a user. we will send a post request to /users with a username and password. The username must be @username of your telegram accaunt
> To understand the actual use of the api, python examples will be used below, but for convenience you can perform all the same actions from swagger at http:
> //127.0.0.1:8000/docs
```python
import requests
import json

data = {
    'username': 'my_telegram_username',
    'password': 'super secret'
}

r = requests.post('http://127.0.0.1:8000/user/', json.dumps(data))

print(r.json())
```
and we received a response from the server:
```json
{
  "username": "my_telegram_username",
  "telegram_id": 0,
  "hashed_password": "$2b$12$pMvq9Ak9IjR7UzF11yPY2e8FvSAbD2SV8WHyhtZFIn3WQ0JJetoTC"
}
```

Congratulations, we have created a user. The user can interact with API methods only by an oauth token which we will pass on each request. Let's try to get it.

```python
import requests


r = requests.post(
    url='http://127.0.0.1:8000/user/token',
    data=r'username=my_telegram_username&password=super%20secret',
    headers={
      'Content-Type': 'application/x-www-form-urlencoded'
    }
)

print(r.json())
```
And we got an error:
```json
{
  "detail": "Incorrect username or password. Maybe user not verified. Pls register user and verify it at https://t.me/your_bot_name"
}
```
This is because we created a user, but did not verify it. Let's go to the bot and verify our user by /verify command

![](https://media.discordapp.net/attachments/979456571971100762/1041069930331787414/image.png)

After passing the verification, let's try to get the token again

```python
import requests


r = requests.post(
    url='http://127.0.0.1:8000/user/token',
    data=r'username=my_telegram_username&password=super%20secret',
    headers={
      'Content-Type': 'application/x-www-form-urlencoded'
    }
)

print(r.json())
```
Output:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYWxhZHdhcmUiLCJleHAiOjE2NjgyODMxNDJ9.yzhM6qvkgQScEv6cM2VwqAuqubBkORKX7R-qiEpUOH0",
  "token_type": "bearer"
}
```

Yeah! Finally, we get a custom token. Now we can work with api methods by passing the token in the Authorization header. Let's get our current events:
```python
import requests


r = requests.get(
    url='http://127.0.0.1:8000/event/my',
    headers={
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYWxhZHdhcmUiLCJleHAiOjE2NjgyODMxNDJ9.yzhM6qvkgQScEv6cM2VwqAuqubBkORKX7R-qiEpUOH0'
    }
)

print(r.json())
```
Output:
```json
{
  "events": []
}
```


### Create Event

The event is created by a post request to /event. When creating it, you must pass the name, description, date of the event and the date of the notification.
The date of the event and notifications are transmitted in the format: `{year}-{month}-{day}T{hours}:{minutes}:{seconds}+{timezone}`.
Let's create a New Year's event in Moscow. We will set an alert about it an hour before the event (pay attention to the timezone format)

```python
import requests
import json


data = {
        'name': 'new year',
        'description': 'after all, no one will mind celebrating the new year in November?',
        'planned_at': '2022-11-13T00:00:00+03:00',
        'remind_at': '2022-11-12T23:00:00+03:00'
    }

r = requests.post(
    url='http://127.0.0.1:8000/event/',
    data=json.dumps(data),
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYWxhZHdhcmUiLCJleHAiOjE2NjgyODMxNDJ9.yzhM6qvkgQScEv6cM2VwqAuqubBkORKX7R-qiEpUOH0'
    }
)

print(r.json())
```
Result:
```json
{
  "name": "new year",
  "description": "after all, no one will mind celebrating the new year in November?",
  "planned_at": "2022-11-12T21:00:00",
  "remind_at": "2022-11-12T20:00:00",
  "id": 1,
  "author_id": "your_username",
  "created_at": "2022-11-12T19:53:15.065041+00:00",
  "is_happened": false
}
```

If you do not pass the notification time, the event notification will be sent 2 hours before it starts. You will not be able to create an event or alert in the past. Notification after the end of the event will also not work

And here is our notification:

![](https://media.discordapp.net/attachments/979456571971100762/1041083072256409600/2022-11-12_23-04-12.png)
