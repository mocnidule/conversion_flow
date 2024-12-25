import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import os


def measure_page_load_time(url, num_runs):
    load_times = []
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--disable-gpu")
    firefox_options.add_argument("--disable-cache")

    firefox_options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"

    for i in range(num_runs):
        driver = webdriver.Firefox(service=Service(executable_path="/usr/local/bin/geckodriver"),
                                   options=firefox_options)
        driver.get(url)
        load_time = driver.execute_script("return window.performance.getEntriesByType('navigation')[0].duration;")
        load_times.append(load_time)
        driver.quit()
        time.sleep(1)

    load_times = np.array(load_times)
    load_time_stats = {
        'url': url,
        'average_load_time': np.mean(load_times),
        'median_load_time': np.median(load_times),
        'std_dev_load_time': np.std(load_times)
    }

    return load_time_stats


def generate_html_report(results):
    with open("report_template.html", "r") as template_file:
        template_content = template_file.read()

    report_content = template_content
    for i, result in enumerate(results):
        report_content = report_content.replace(f"[[url{i + 1}]]", result['url']) \
            .replace(f"[[avg_load_time{i + 1}]]", str(result['average_load_time'])) \
            .replace(f"[[median_load_time{i + 1}]]", str(result['median_load_time'])) \
            .replace(f"[[std_dev{i + 1}]]", str(result['std_dev_load_time']))

    return report_content


def run_parallel_tests(urls, num_runs=1):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(measure_page_load_time, url, num_runs) for url in urls]
        results = [f.result() for f in futures]

    return results
