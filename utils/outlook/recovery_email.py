# %%
import imaplib, re, email, pytz
from datetime import datetime, timedelta
from dateutil.parser import parse
from dotenv import dotenv_values


# %%
def get_recovery_vericode():
    new_recovery_email = dotenv_values()['NEW_RECOVERY_EMAIL']
    default_okx_psw = dotenv_values()['DEFAULT_OKX_PASSWORD']

    M = imaplib.IMAP4_SSL(host='outlook.office365.com', port=993)
    M.login(new_recovery_email, default_okx_psw)
    M.list()
    M.select()

    for _ in range(10):
        typ, data = M.search(None, 'ALL')
        if typ == 'OK':
            typ, mail = M.fetch(data[0].split()[-1], '(RFC822)')
            text = mail[0][1].decode()

            if typ == 'OK':
                mail_time = email.message_from_bytes(mail[0][1])['date']

                if datetime.now().astimezone(pytz.utc) - parse(
                        mail_time).astimezone(pytz.utc) > timedelta(minutes=1):
                    return False, (text, mail_time)

                vericode_tile = re.search('>+[0-9]{6}<+', text)
                if vericode_tile is None:
                    vericode_tile = re.search(
                        '[^0-9a-zA-Z]+[0-9]{6}[^0-9a-zA-Z]+', text).group()
                else:
                    vericode_tile = vericode_tile.group()
                return True, re.search('[0-9]{6}', vericode_tile).group()

    raise Exception('connect to or fetch outlook error')
