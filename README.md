# http-w3c-log-monitor
![N|Solid](https://raw.githubusercontent.com/haagor/http-w3c-log-monitor/master/img/banner.png)

* Write a simple program to monitor a given HTTP access log file and provide alerting and monitoring.
* The program will consume an actively written-to w3c-formatted HTTP access log. It should default to reading `/var/log/access.log` and be **overridable**.
* Display stats every 10s about the traffic during those 10s:
* * the sections of the web site with the most hits, as well as interesting summary statistics on the traffic as a whole.
* * a section is defined as being what's before the second / in the path. For example, the section for http://my.site.com/pages/create is http://my.site.com/pages.
* Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that: "High traffic generated an alert - hits = {value} , triggered at {time} ".
* The default threshold should be 10 requests per second and should be **overridable**.
* Whenever the total traffic drops again below that value on average for the past 2 minutes, print or displays another message detailing when the alert recovered.

## Getting Started
* First you have to edit `config.ini` with your own absolute path.
* Then you can run `/src/log_generator$ python3 log_generator.py` in order to generate log into `/var/log/access.log`
* Next run `/src/handler_generator$ python3 main.py`

For execute the tests you can run `python3 -m unittest tests/test_log_reader.py`

## Details

### Naming convention
My naming convention that I use is, if we take the variable "hello" for example :

* `g_hello` global variable
* `l_hello` local variable
* `c_hello` loop variable
* `p_hello` parameter

### Log generator
I didn't wanted to spend too much time on the log generator. For me it's necessary for the the POC, but this code don't have to persist. That's why I choose to don't write unit test.
The error handling isn't present.
I have isolate this code in another package because it's coherent alone and could be easily removed in the future.

### Log handler
The package `log handler` contains the main part of the project. You have :

- A log reader
- An information displayer relative to the log
- An alerter

![N|Solid](https://raw.githubusercontent.com/haagor/http-w3c-log-monitor/master/img/projectStructur.png)

The log reader provide the parsed log, but also metrics. It provides these through two differents queues. It's a good point to isolate logs and metrics in order to facilitate the maintenance and code evolve.
A good evolve here could be to replace Python queue by a similar tool like Kafka. It will be more easier to isolate responsibility of log reader, and the other logic based on it. We can also use ElasticSearch to provide the data to these services. The main point here is to separate responsibilities and create different services to handle it. And use dedicated tools to be more performante rapidly. 

### Next steps

* To choose beetween Kafka, ES or MongoDB to replace the Python queue, and to separate services in log handler
* Initially, I didn't wanted to start this projet with object programmation, but at this point structure become more and more necessary for continue to evolve
* To implement more unit test and integration test
* To implement error handling
* In this use case it's often important to customize metrics and alerting. For now the code doesn't facilitate that and it could
* Most important, play alert sound for each alert rise


## Authors

* **Paris Simon** 
