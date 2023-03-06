from secondLevelKeys import getSecondLevelKeys
import pandas as pd
def flat_dict_to_pandas(details):
    rows = []
    keys_set = getSecondLevelKeys(details)
#    keys_set.remove("similarurl")
    all_keys = list(keys_set)
    all_keys.sort()
    unique_key = "url"
    if unique_key in all_keys:
        print(f'Error: unique key {unique_key} is used in second level ditctionary keys')
        exit()
    tofloat={'livingArea':1,'kitchenArea':1,'totalArea':1}
    name_columns = [unique_key] + all_keys
    for kvaritrUrl, ditali in details.items():
        row = [kvaritrUrl]
        for i in range(1,len(name_columns)):
            key=name_columns[i]
            if key in ditali:
                if (key in tofloat) and (ditali[key] is not None):
                    row.append(float(ditali[key]))
                else:
                    row.append(ditali[key])
            else:
                row.append('')
        rows.append(row)
    return pd.DataFrame(rows,columns=name_columns)
