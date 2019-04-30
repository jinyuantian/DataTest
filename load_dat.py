def get_data(df):
    df1 = df.drop(['currentExpDate', 'dateOfLastAddressChange', 'accountNumber', 'cardCVV', 'cardLast4Digits', 'enteredCVV', 'currentBalance', 'merchantCountryCode', 'transactionDateTime'], axis=1)
    df1['CVV_ind'] = (df['enteredCVV'] == df['cardCVV'])
    df1['CVV_ind'] = df1['CVV_ind'].astype(int)
    df1['Country_ind'] = (df['acqCountry'] == df['merchantCountryCode'])
    df1['Country_ind'] = df1['Country_ind'].astype(int)
    df1['OTB_sign'] = df['availableMoney'] >= 0
    df1['OTB_sign'] = df1['OTB_sign'].astype(int)
    df1['OTB_ratio'] = df['availableMoney'] / df['creditLimit']
    df1['transaction_ratio'] = df['transactionAmount'] / df['availableMoney']
    df1 = pd.get_dummies(df1, columns=['acqCountry', 'cardPresent', 'expirationDateKeyInMatch', 'transactionType', 'posConditionCode', 'posEntryMode', 'merchantCategoryCode'])
#     m1 = {'cable/phone': '1',
#          'food_delivery': '1',
#          'fuel': '1',
#          'gym': '1',
#          'mobileapps': '1',
#          'online_subscriptions': '1',
#           'airline': '2',
#           'auto': '2',
#           'fastfood': '2',
#           'food': '2',
#           'online_gifts': '2',
#           'health': '2',
#           'online_retail': '2',
#           'rideshare': '2',
#           'hotels': '3',
#           'entertainment': '4',
#           'furniture': '4',
#           'personal care': '4',
#           'subscriptions': '4'
#          }

#     df1['merchantCategoryCode_category'] = df['merchantCategoryCode'].map(m1)
    treshold = 0.04
    mct_df = pd.DataFrame(df.groupby('merchantName').apply(lambda x: sum(x.isFraud == 1) / len(x)))
    mct_df.reset_index(inplace=True)
    mct_df.columns = ['merchantName', 'ratio']

    s1 = set(mct_df.loc[mct_df['ratio'] < 0.000001, 'merchantName'])
    s2 = set(mct_df.loc[(mct_df['ratio'] >= 0.000001) & (mct_df['ratio'] < treshold), 'merchantName'])
    s3 = set(mct_df.loc[mct_df['ratio'] >= treshold, 'merchantName'])

    df1['merchantNameCode'] = 0
    df1.loc[df1['merchantName'].isin(s1), 'merchantNameCode'] = 0
    df1.loc[df1['merchantName'].isin(s2), 'merchantNameCode'] = 1
    df1.loc[df1['merchantName'].isin(s3), 'merchantNameCode'] = 2

    df1.drop('merchantName', axis=1, inplace=True)

    df1['tenure'] = df1['accountOpenDate'].apply(lambda x: 2019 - int(x[:4]))
    df1.drop('accountOpenDate', axis=1, inplace=True)

    df1 = pd.get_dummies(df1, columns=['merchantNameCode'])

    return df1
