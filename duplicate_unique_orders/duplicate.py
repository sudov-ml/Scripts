import sys
import subprocess


subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'pandas'])


import pandas as pd

def getdate(raw):
    d,_=raw.split('T')
    d=d.replace('-','')
    return int(d)
def backdate(date):
    date=str(date)
    return date[:4]+'-'+date[4:6]+'-'+date[6:]


path=input('enter path/name of input csv:')
data=pd.read_csv(path)
ids=data.user_profile_id
out=data[ids.isin(ids[ids.duplicated()])].sort_values("user_profile_id")

out.order_date=out.order_date.apply(getdate)
groups=out.groupby('name',group_keys=False)
out=groups.apply(lambda x: x.sort_values(by=['order_date']))
out.order_date=out.order_date.apply(backdate)

unique=out.pivot_table(index=['user_profile_id'],aggfunc='size')
unique=pd.DataFrame(unique,columns=['orders'])
unique['user_profile_id']=unique.index
unique=unique.reset_index(drop=True)
new_u=out.drop(['order_date','order_id','payment_id','amount'],axis=1).drop_duplicates()
new_data=pd.merge(new_u,unique,on=['user_profile_id','user_profile_id'])

print('duplicate and unique tables generated !!!')
name=input('enter name for duplicate data file (without extension):')
n=len(out.user_profile_id.unique())
name2=input('enter name for unique data file (without extension):')
print(f'data of {n} unique records saved !')
out.to_csv(f'{name}.csv')
new_data.to_csv(f'{name2}.csv')
