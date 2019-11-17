runner = BotsRunner([792414733]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Hawkeye", bot)
runner.set_main_bot(bot)
print('Hawkeye works!')
runner.run()
