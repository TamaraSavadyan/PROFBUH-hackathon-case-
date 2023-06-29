from dataclasses import dataclass
import yaml


@dataclass
class BotConfig:
    token: str


@dataclass
class YoutubeAPIConfig:
    key: str


@dataclass
class GPTAPIConfig:
    key: str


@dataclass
class DatabaseConfig:
    user: str
    password: str
    host: str
    port: int
    db_name: str


@dataclass
class Config:
    bot: BotConfig = None
    youtube_api_key: YoutubeAPIConfig = None
    gpt_api_key: GPTAPIConfig = None
    database: DatabaseConfig = None


def setup_config(config_path: str):
    with open(config_path, 'r') as file:
        raw_config = yaml.safe_load(file)

    return Config(
        bot=BotConfig(
            token=raw_config['bot_token'],
        ),
        youtube_api_key=YoutubeAPIConfig(
            key=raw_config['youtube_api_key'],
        ),
        gpt_api_key=GPTAPIConfig(
            key=raw_config['gpt_api_key'],
        ),
        database=DatabaseConfig(
            user=raw_config['database']['user'],
            password=raw_config['database']['password'],
            host=raw_config['database']['host'],
            port=raw_config['database']['port'],
            db_name=raw_config['database']['db'],
        ),
    )


config = setup_config('config.yaml')


if __name__ == '__main__':
    print(config)
