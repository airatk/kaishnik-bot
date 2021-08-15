from logging import basicConfig
from logging import NOTSET

from bot.utilities.database.helpers import setup_database_tables


if __name__ == "__main__":
    # Logger setup
    basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=NOTSET)
    
    # Database setup
    setup_database_tables()
    
    # Launching bot on all platforms
    # TODO: Implementing simultaneous launch on all platforms. 
    # from bot.platforms.telegram import launch
    # from bot.platforms.vk import launch
