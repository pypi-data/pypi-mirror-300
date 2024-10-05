import os
from datetime import datetime
from .utils import Get_ENV, Load_ENV

class BotSetup:
    def __init__(self, bot, env_path=None):
        self.bot = bot
        Load_ENV(env_path)  # Ensure environment variables are loaded before accessing them
        self.token = Get_ENV(key="TOKEN")
        self.cogs_directory = "./cogs"

    def run_bot(self):
        try:
            if not self.token or self.token == "NO_TOKEN_ADDED":
                print("NO_TOKEN_ADDED. Please add a valid token in environment secrets")
                return
            self.bot.run(self.token)
        except Exception as e:
            print("ERROR: bot.py | bot.run() failed to run the bot. Possible wrong token or invalid token?!")
            raise Exception(e)

    def add_cogs(self):
        try:
            if not os.path.exists(self.cogs_directory):
                print(f"ERROR: bot.py | Cog directory '{self.cogs_directory}' does not exist.")
                return

            for filename in os.listdir(self.cogs_directory):
                if filename.endswith(".py"):
                    try:
                        self.bot.load_extension(f"cogs.{filename[:-3]}")
                        print(">", filename)
                    except Exception as e:
                        print(f"ERROR: bot.py | Failed to load cog '{filename}'. Error: {e}")
                        raise Exception(e)
        except Exception as e:
            print(f"ERROR: bot.py | Cog Support failed to load. Possible /cogs does not exist?! or Duplicate?! Error: \n{e}")
            raise Exception(e)

    def setup_bot(self):
        try:
            print("=====BOT=====")
            print("Loading Cogs:")
            self.add_cogs()
            print("==================================================")
            self.run_bot()
        except Exception as e:
            print(f"ERROR: bot.py | Bot Setup failed to run. Error: \n{e}")
            raise Exception(e)
    
    async def getBotStartupInfo(self):
        version = Get_ENV(key="VERSION")
        launch_time = str(datetime.now())[0:19]
        user = self.bot.user

        launch_message = f"Launched with Version {version} at {launch_time}"+ "\n" + f"Logged in as: {user}" + "\n" + "\n" + "\n" + "Broadcasts:"
        return launch_message