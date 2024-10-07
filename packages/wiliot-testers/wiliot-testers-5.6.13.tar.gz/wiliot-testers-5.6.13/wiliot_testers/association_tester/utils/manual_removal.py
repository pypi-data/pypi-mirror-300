#  """
#    Copyright (c) 2016- 2024, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """
import os
import time

import pandas as pd
import PySimpleGUI as Sg


def get_files_path():
    """
    opens GUI for selecting a file and returns it
    """
    # Define the window's contents
    layout = [[Sg.Text('select file for maunal removal:'), Sg.Input(key='file_path_str'),
               Sg.FileBrowse(key='file_path')],
              [Sg.Button('Select')]
              ]

    # Create the window
    window = Sg.Window('Manual Removal Tool', layout)
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == 'Select' and (values['file_path'] != '' or values['file_path_str'] != ''):
            values['file_path'] = values['file_path_str']
            if not os.path.isfile(values['file_path']):
                raise Exception(f'file: {values["file_path"]} does not exist')
            loc_df = pd.read_csv(values['file_path'])
            window.close()
            return loc_df
        else:
            window.close()
            exit(-1)


def print_tags_to_remove(msg_to_print):
    ind = 0
    layout = [[Sg.Text(msg_to_print[ind], key='msg', font=("Helvetica", 14))],
              [Sg.Button('Previous'), Sg.Button('Next')]
              ]

    # Create the window
    window = Sg.Window('Manual Removal Tool', layout)
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == 'Next' or event == 'Previous':
            if event == 'Next':
                ind += 1
            else:
                ind -= 1 if ind > 0 else 0
            if ind >= len(msg_to_print):
                print('end of run')
                window.close()
                time.sleep(1)
                return
            window['msg'].update(msg_to_print[ind])
        else:
            print('app was closed during run!!!')
            return


def extract_user_msg(df):
    """

    @param df:
    @type df: pd.DateFrame
    @return:
    @rtype:
    """
    df.sort_values(by='location', ascending=False, inplace=True)
    df = df[~((df["asset_code"].isna()) & (df["wiliot_code"].isnull()))]
    df.reset_index(inplace=True)
    msg_out = [f'First Label should be: {df["asset_code"].iloc[0]}, {df["wiliot_code"].iloc[0]}']
    last_good_label = ''
    bads_label = []
    n_bad_labels = 0
    for ind_num, row in df.iterrows():
        if row['is_success']:
            if bads_label:
                if len(bads_label) == 1:
                    bads_label_list = f'{bads_label[0]["asset_code"]}, {bads_label[0]["wiliot_code"]}\n'
                else:
                    bads_label_list = f'from: {bads_label[0]["asset_code"]}, {bads_label[0]["wiliot_code"]}\n' \
                                      f'till: {bads_label[-1]["asset_code"]}, {bads_label[-1]["wiliot_code"]}'

                msg_out.append(f'good label BEFORE: {last_good_label}\n\n'
                               f'Please remove the following ({len(bads_label)} tags):\n'
                               f'{bads_label_list}\n\n'
                               f'good label AFTER: {row["asset_code"]}, {row["wiliot_code"]}\n\n')

            last_good_label = f'{row["asset_code"]}, {row["wiliot_code"]}'
            bads_label = []
            continue
        # bad tag
        bads_label.append(row[['asset_code', 'wiliot_code']])
        n_bad_labels += 1

    msg_out.append(f'Last Label should be: {df["asset_code"].iloc[-1]}, {df["wiliot_code"].iloc[-1]}')
    return msg_out, n_bad_labels


if __name__ == '__main__':
    location_df = get_files_path()
    user_msgs, n_bad_labels = extract_user_msg(location_df)
    print(f'number of tag to remove: {n_bad_labels}')
    print_tags_to_remove(user_msgs)
    print('done')
