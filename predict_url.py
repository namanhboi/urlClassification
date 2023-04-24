import pickle
import config
import sqlite3
from functions import scrape_url

pickle_in = open(config.WORDS_FREQUENCY_PATH, "rb")
words_frequency = pickle.load(pickle_in)


"""
parser = argparse.ArgumentParser(description='URLs for category predictions')
parser.add_argument('-u', '--url', help='Predict custom website')
parser.add_argument('-t', '--text_file_path', help='Predict websites written in text file')

args = parser.parse_args()

if args.url:
    url = args.url
    print(url)
    results = scrape_url(url, words_frequency)
    if results:
        print('Predicted main category:', results[0])
        print('Predicted submain category:', results[2])
elif args.text_file_path:
    file_path = args.text_file_path
    with open(file_path) as f:
        for url in f:
            url = url.replace('\n', '')
            print(url)
            results = scrape_url(url.replace('\n', ''), words_frequency)
            if results:
                print('Predicted main category:', results[0])
                print('Predicted submain category:', results[2])
else:
    parser.error("Please specify websites input type. More about input types you can find 'python predict_url -h'")
"""
if __name__ == '__main__':
    connection =   sqlite3.connect("nblocker.sqlite3")
    cursor = connection.cursor()
    rows = cursor.execute("""select id, domain
                          from domains
                          where category is null  
                          order by last_seen desc 
                          limit 30""").fetchall()

    for i in rows:
        id = i[0]
        url = i[1]
        url = "https://" + url
        results = scrape_url(url.replace('\n', ''), words_frequency)
        category = 'undefined'
        if results:
            category = results[0]
        #print(id, url, category)
        cursor.execute("""update domains
        set CATEGORY = ? WHERE ID = ?""", (category, id))
        connection.commit()
    temp_rows = cursor.execute("""select id, domain, category
    from domains
    order by last_seen desc
    limit 30""").fetchall()
    for i in temp_rows:
        print(i)
    connection.close()

