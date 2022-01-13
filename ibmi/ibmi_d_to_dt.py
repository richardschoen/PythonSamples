#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 11:50:59 2022
ibmi_d_to_dt.py ... func to convert IBM i dates to Python datetime
@author: jwoehr
"""

import datetime
import argparse


def ibm_i_date_to_datetime(ibmidate: str) -> datetime.datetime:
    """
    Convert IBM i date CYYMMDDHHMMSS to Python datetime

    Parameters
    ----------
    ibmidate : str
        IBM i date CYYMMDDHHMMSS

    Returns
    -------
    _dd : datetime.datetime
        Python datetime for the converted string

    """
    _cn = 2000 if int(ibmidate[0:1]) == 1 else 1900
    _yr = int(ibmidate[1:3])
    _mo = int(ibmidate[3:5])
    _dt = int(ibmidate[5:7])
    _hr = int(ibmidate[7:9])
    _mi = int(ibmidate[9:11])
    _se = int(ibmidate[11:])
    _dd = datetime.datetime(_cn + _yr, _mo, _dt, _hr, _mi, _se)
    return _dd


if __name__ == "__main__":

    EXPLANATION = """Demos ibm_i_date_to_datetime function. Takes any number of
    IBM i dates of the form CYYMMDDHHMMSS and prints the Python datetime.datetime
    conversion of same. 
    Copyright 2022 Jack Woehr jwoehr@softwoehr.com PO Box 51, Golden, CO 80402-0051.
    Free to all to use no warranty no guarantee !!!
    Apache License, Version 2.0 -- https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    """
    PARSER = argparse.ArgumentParser(description=EXPLANATION)

    PARSER.add_argument(
        "candidates", nargs="*", help="IBM i date(s) in form CYYMMDDHHMMSS"
    )

    ARGS = PARSER.parse_args()
    for candidate in ARGS.candidates:
        print(ibm_i_date_to_datetime(candidate))
