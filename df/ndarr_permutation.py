import pandas as pd
import numpy as np
from itertools import permutations


def arr_permutation(input_arr, permutation_column_index='0', label_index='1'):
    permutation_df = pd.concat(
        [pd.DataFrame(list(map(''.join, permutations(input_arr[permutation_column_index].values.tolist(), num+1))),
                      columns=['permutations'])
         for num in range(len(input_arr.index))]
    )

    permutation_df['label'] = permutation_df.apply(
        lambda x: label_gen(x['permutations'], input_arr, permutation_column_index, label_index), axis=1
    )

    return permutation_df


def label_gen(input_txt, ori_df, permutation_column_index='0', label_index='1'):
    ori_dic = {ori_df.loc[i, permutation_column_index]: ori_df.loc[i, label_index] for i in ori_df.index}

    index_list = [ori_dic[item] + ':' + str(input_txt.find(item)) + ':' + str(len(item)) for item in ori_dic.keys() if input_txt.find(item) > -1]

    index_list.sort(key=lambda x: int(x.split(':')[1]))
    index_list.sort(key=lambda x: int(x.split(':')[2]), reverse=True)

    final_list = [x.split(':')[0] for x in index_list]

    return max(final_list, key=lambda x: index_list.count(x))


if __name__ == "__main__":
    # sample = pd.DataFrame([['AB', '0'], ['CD', '1'], ['EFG', '1'], ['HIJK', '0'], ['LMN', '1']])
    sample = pd.read_csv('../poc/data_result/merged_final.csv')[['명칭', 'label']][50:62].drop_duplicates()
    print(sample)
    per_sample = arr_permutation(sample, '명칭', 'label')

    per_sample.to_csv('../poc/data_result/permutation_sample.csv', index=False)
