#!/usr/bin/python
import os
import csv
import datetime
import time
import twitter


def test():
    # run speedtest-cli
    a = os.popen("python env/bin/speedtest-cli --simple").read()
    # split the 3 line result (ping,down,up)
    lines = a.split('\n')
    ts = time.time()
    date =datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # if speedtest could not connect set the speeds to 0
    print(lines)
    if "Cannot" in a:
            p = 100
            d = 0
            u = 0
    # extract the values for ping down and up values
    else:
            p = lines[0][6:11]
            d = lines[1][10:14]
            u = lines[2][8:12]
    # save the data to file for local network plotting
    if os.path.exists("data.csv"):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not

    out_file = open('data.csv', append_write)
    writer = csv.writer(out_file)
    writer.writerow((ts*1000,p,d,u))
    out_file.close()

    # connect to twitter
    TOKEN=os.getenv("TOKEN", "")
    TOKEN_KEY=os.getenv("TOKEN_KEY", "")
    CON_SEC=os.getenv("CON_SEC", "")
    CON_SEC_KEY=os.getenv("CON_SEC_KEY", "")

    my_auth = twitter.OAuth(TOKEN, TOKEN_KEY, CON_SEC, CON_SEC_KEY)
    twit = twitter.Twitter(auth=my_auth)

    # try to tweet if speedtest couldnt even connet. Probably wont work if the internet is down
    if "Cannot" in a:
            try:
                    tweet = f"Hey @Mediacom @MediacomSupport  why is my internet down? I pay for 1000down\\50up in Springfield MO? #mediacomoutage {date}"
                    twit.statuses.update(status=tweet)
            except:
                    pass

    # tweet if down speed is less than whatever I set
    elif eval(d)<50:
            print("trying to tweet")
            try:
                    # i know there must be a better way than to do (str(int(eval())))
                    tweet=f"Hey @Mediacom why is my internet speed {d}down\\{u}up when I pay for 1000down\\50up in Springfield MO? #mediacomoutage #speedtest"
                    twit.statuses.update(status=tweet)
            except Exception as e:
                    print(str(e))
                    pass
    return

if __name__ == '__main__':
        test()
        print('completed')
