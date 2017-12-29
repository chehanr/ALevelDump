#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A simple script used to scrape A/L results in given range of IDs (by /u/chehanr)."""

import json
import multiprocessing.dummy as mp
import os
import time
from time import gmtime, strftime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CWD = os.getcwd()
TIME = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
PATH = '%s\\dump\\%s\\' % (CWD, TIME)


def merge_files():
    """Merge all txt files into one."""

    with open(PATH + 'dump.txt', 'w') as out_file:
        for txt_file in os.listdir(PATH):
            if txt_file.endswith('.txt'):
                with open(os.path.join(PATH, txt_file)) as in_file:
                    for line in in_file:
                        out_file.write(line)


def check_path(path):
    """Check path, if not create it."""

    directory = os.path.dirname(path)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as err:
        print(err)


def dump_to_txt(dict_data, number_chunk):
    """Write the dictionary data as json to txt file."""

    check_path(PATH)
    file_name = 'dump_%s-%s.txt' % (min(number_chunk), max(number_chunk))
    try:
        with open(PATH + file_name, 'a+') as txt_file:
            json.dump(dict_data, txt_file)
            txt_file.write('\n')
    except Exception as err:
        print(err)


def main(number_chunk):
    """Scrape data into nested dictionary."""

    DRIVER = webdriver.PhantomJS()
    DRIVER.get('http://www.doenets.lk/result/alresult.jsf')

    for i in number_chunk:
        student_id = '72%s' % (str(i).zfill(5))

        submit_box = DRIVER.find_element_by_id('frm:username')
        submit_box.clear()
        submit_box.send_keys(student_id)

        submit_button = DRIVER.find_element_by_id('frm:btnSubmit')
        submit_button.click()

        delay = 0  # seconds
        try:
            result_form = WebDriverWait(DRIVER, delay).until(
                EC.presence_of_element_located((By.ID, 'j_idt16')))

            print('scraping id %s' % (student_id))

            student_info = []
            student_results = []

            info = {
                'examination': result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt19_data']/tr[1]/td[2]").text.strip(),
                'year ': result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt19_data']/tr[2]/td[2]").text.strip(),
                'name': result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt19_data']/tr[3]/td[2]").text.strip(),
                'index_number': result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt19_data']/tr[4]/td[2]").text.strip(),
                'district_rank': result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt19_data']/tr[5]/td[2]").text.strip(),
                'island_rank': result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt19_data']/tr[6]/td[2]").text.strip(),
                'z_score': result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt19_data']/tr[7]/td[2]").text.strip(),
                'subject_stream': result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt19_data']/tr[8]/td[2]").text.strip()
            }

            student_info.append(info)

            # row_count = len(DRIVER.find_elements_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr"))
            # for i in [x for x in range(row_count) if x != 0]:
            #     xpath_1 = "//tbody[@id='j_idt16:j_idt26_data']/tr[%s]/td[1]" % (i)
            #     xpath_2 = "//tbody[@id='j_idt16:j_idt26_data']/tr[%s]/td[2]" % (i)
            #
            #     results = {
            #         result_form.find_element_by_xpath(xpath_1).text.strip(): result_form.find_element_by_xpath(xpath_2).text.strip()
            #     }
            #
            #     student_results.append(results)

            results = {
                result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[1]/td[1]").text.strip(): result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[1]/td[2]").text.strip(),
                result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[2]/td[1]").text.strip(): result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[2]/td[2]").text.strip(),
                result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[3]/td[1]").text.strip(): result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[3]/td[2]").text.strip(),
                result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[4]/td[1]").text.strip(): result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[4]/td[2]").text.strip(),
                result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[5]/td[1]").text.strip(): result_form.find_element_by_xpath("//tbody[@id='j_idt16:j_idt26_data']/tr[5]/td[2]").text.strip()
            }

            student_results.append(results)

            student = {
                'student_info': student_info,
                'student_results': student_results
            }

            dump_to_txt(student, number_chunk)

        except TimeoutException:
            pass


def chunk_it(range_limit, number):
    """Generate number pairs."""

    for i in range(0, len(range_limit), number):
        yield range_limit[i:i + number]


if __name__ == '__main__':
    UPPER_LIMIT = 100000
    PROCESS_NUMBER = UPPER_LIMIT // 10
    CHUNKS = list(chunk_it(range(UPPER_LIMIT), PROCESS_NUMBER))

    START_TIME = time.time()

    try:
        print('dumping %s IDs with %s processes' %
              (UPPER_LIMIT - 1, len(CHUNKS)))
        POOL = mp.Pool(PROCESS_NUMBER)
        POOL.map(main, CHUNKS)
        POOL.close()
        POOL.join()
    except KeyboardInterrupt:
        merge_files()
    else:
        merge_files()

    END_TIME = time.time()

    print('\ntook %s seconds' % (END_TIME - START_TIME))
