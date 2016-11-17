# -*- coding: utf-8 -*-

'''
Simple python script that takes a list of Chinese characters and translate them to English using the Google Cloud Translation API
'''

import requests
import json
import pandas
import csv
import io


def translate(api_key, source, target, text):

    httpurl = "https://translation.googleapis.com/language/translate/v2?key={0}&source={1}&target={2}&q={3}".format(api_key, source, target, text)
    r = requests.get(httpurl)

    result = json.loads(r.content)

    return [x['translatedText'] for x in result["data"]["translations"]]


if __name__ == '__main__':

    PATH = "/Users/palermospenano/Desktop/Dropbox/temporary/nicolai_py"
    varlist = "{0}/vars2test.csv".format(PATH)

    # load api key from secret json file
    with io.open('{0}/config_secret.json'.format(PATH)) as cred:
        creds = json.load(cred)
    api_key = creds['api_key']

    source = "zh"
    target = "en"

    ##################################
    # PART 1: import csv into pandas #
    ##################################

    df = pandas.read_csv(varlist)

    varid = 'id'
    varname = 'varname'

    # print df.head()

    varid_col = df[varid]
    varname_col = df[varname]

    #####################
    # PART 2: translate #
    #####################

    out_csv = "{0}/vartrans.csv".format(PATH)
    header = [varid, varname, 'varname_en']

    with open(out_csv, 'wb') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(header)

        for id_code, varname in zip(varid_col, varname_col):

            # print id_code, varname, type(varname)
            translation_list = translate(api_key, source, target, varname)

            for t in translation_list:
                print t
                row_data = [id_code, varname, t]
                writer.writerow(row_data)
