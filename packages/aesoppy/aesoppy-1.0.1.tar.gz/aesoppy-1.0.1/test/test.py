import aesoppy.gurufocus as gf
from dotenv import load_dotenv
import os


load_dotenv()
gt = os.getenv('guru_token')

x = gf.DividendHistory(token=gt, ticker='txn').div_df()
print(x)