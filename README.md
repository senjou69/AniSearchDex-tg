# How to deploy?
Deploying is pretty much easy (I guess?)
## Installing requirements

- Clone this repo:
```
git clone https://github.com/senjou69/AniSearchDex-tg.git
cd AniSearchDex-tg
```

- Install requirements
```
sudo apt install python3
```

- Install dependencies
```
pip3 install -r requirements.txt
```

## Setting up [config.py](https://github.com/senjou69/AniSearchDex-tg/blob/main/anisearchdex/config.py)

Fill up rest of the fields. Meaning of each fields are discussed below:
- **BOT_TOKEN** : The telegram bot token that you get from @BotFather
- **OWNER_ID** : The Telegram user ID (not username) of the owner of the bot
- **SERVICE_ACCOUNT_FILE**: Full path of the SA file. (read about the SA file generation from [here](https://support.google.com/a/answer/7378726))
- **USERNAME** : The username of the bot (excluding @)


## Starting up the bot
If you have set up the config file correctly, your bot now should run correctly.

```
python3 -m anisearchdex
```
