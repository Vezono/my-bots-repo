try:
    from tokens import environ
except ImportError:
    import os

    environ = os.environ

com_id = '158702123'
cn_id = '0bc640b0-5b4f-4ec9-a269-35b03e883ec3'
email = 'gbball.trash@gmail.com'
password = environ['amino_password']
mongo_token = environ['database']
brit_id = '6e347e8a-dda4-4cb9-8e0d-01e4062df351'
t_token = environ['assistant']
tg_cn_id = -1001333052188
tg_brit_id = 792414733
