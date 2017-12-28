#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A simple script used to scrape A/L results in given range of IDs (by /u/chehanr)."""

import json
from time import gmtime, strftime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIME = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

DRIVER = webdriver.Firefox()
DRIVER.get('http://www.doenets.lk/result/alresult.jsf')


def dump_to_txt(dict_data):
    """Write the dictionary data as json to txt file."""
    file_name = 'dump_%s.txt' % (TIME)
    try:
        with open(file_name, 'a+') as f:
            json.dump(dict_data, f)
            f.write('\n')
    except Exception as err:
        print(err)


def main(student_id):
    """Scrape data into nested dictionary."""

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

        dump_to_txt(student)

    except TimeoutException:
        pass


if __name__ == '__main__':
    for i in range(1000):
        i = str(i)
        id = '7259%s' % (i.zfill(3))
        main(id)
