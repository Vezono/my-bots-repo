from manybotslib import BotsRunner




runner = BotsRunner() # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Veganvirt", bot)
runner.set_main_bot(bot)
runner.run()
