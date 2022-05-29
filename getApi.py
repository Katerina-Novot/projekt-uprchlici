import datetime
import pandas as pd
import requests

def get_tweets_for_period(period):
  url = 'https://www.hlidacstatu.cz/api/v2/datasety/vyjadreni-politiku/hledat?'
  headers = {'Authorization' : API_KEY}
  input = f'server:Twitter AND datum:[{period}]'
  params = {'dotaz' : input}
  
  output = []
  page = 1
  while True:
    print(f"Getting page {page}.")
    params['strana'] = page
    response = requests.get(url=url, headers=headers, params=params)
    out = response.json()['results']

    if out and page < 200:
      output.extend(out)
      page += 1
    else:
      break
      
  return output


def export_tweets_to_csv(base_dict):
  df = pd.DataFrame(columns = ['osobaid', 'datum', 'text'])

  result = []

  base = datetime.date(year=base_dict['year'], month=base_dict['month'], day=base_dict['day'])
  for i in range(365):
    date_from = base + datetime.timedelta(days=i)
    date_to = base + datetime.timedelta(days=i+1)
    period = "%s TO %s" % (date_from.strftime('%Y-%m-%d'), date_to.strftime('%Y-%m-%d'))

    if date_from < datetime.date.today():
      print('Getting ' + period)
      result = get_tweets_for_period(period=period)
      result.extend(result)
    else:
      break

  for x in result:
    osobaid = x['osobaid']
    datum = x['datum']
    text = x['text']

    df = df.append({"osobaid" : osobaid, "datum": datum, "text": text}, ignore_index=True)

  path = f"{PROJ_DIR}/Main/Tweets{base_dict['year']}.csv"
  df.to_csv(path)

  print("All exported!")

  return None


def main():
  export_tweets_to_csv(base_dict={'year': 2015, 'month': 1, 'day': 1})
  # export_tweets_to_csv(base_dict={'year': 2022, 'month': 2, 'day': 1})


main()