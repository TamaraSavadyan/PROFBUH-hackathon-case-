from dataclasses import dataclass
import yaml


@dataclass
class BotConfig:
    token: str


@dataclass
class YoutubeAPIConfig:
    key: str


@dataclass
class Config:
    bot: BotConfig = None
    youtube_api_key: YoutubeAPIConfig = None


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
    )


config = setup_config('config.yaml')
