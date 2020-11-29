[前言]
Apache Bench 是 Apache 服务器的一个web压力测试工具，简称ab
ab也是一个命令行工具，对发起负载的本机要求很低，根据ab命令可以创建很多的并发访问线程，模拟多个访问者同时对某一个URL地址进行访问，
因此可以用来测试目标服务器的负载压力。总体来说，ab工具小巧简单，上手学习较快，可以提供需要的基本性能指标；
但是缺点就是没有图形化结果，不能监控。

[使用方法]
windows下
    1. cd 到ab的bin目录
    2.一定要在需要测试的url末尾加一个path，否则测试时会认为url非法。
        例：ab -n 1000 -c 30 http://www.baidu.com/path

[返回结果解析]

**Concurrency Level**: 并发量。（500）

**Time taken for tests**: 整个测试所用的时间。（34.809 s）

**Complete requests**: 完成的请求数。（1000）

**Failed requests**: 失败的请求数。（0）

**Non-2xx responses**: 如果接收到的HTTP响应数据的头信息中含有2XX以外的状态码，
  则会在测试结果中显示另一个名为“Non-2xx responses”的统计项，用于统计这部分请求数（这些请求并不算在失败的请求中）。（1000）

**Total transferred**: 表示所有请求的响应数据长度总和，包括每个HTTP响应数据的头信息和正文数据的长度。（502000 bytes）

**HTML transferred**: 表示所有请求的响应数据中正文数据的总和，也就是减去了Total transferred中HTTP响应数据中的头信息的长度。（222000 bytes）

**Requests per second(RPS)**: 吞吐率。要清楚吞吐率是与并发数相关的，即使请求总数相同，但如果并发数不一样，
  吞吐率还是很可能有很大差异的。 （28.73【#/second】）
  计算公式：Complete requests/Time taken for tests

**Time per request(mean)**: 用户平均请求等待时间。也就是一次并发总的时间。 （17404.500 ms） 
  计算公式：Time token for tests/（Complete requests/Concurrency Level）。

**Time per request**(mean, across all concurrent requests): 服务器平均请求等待时间。
  也就是一次请求（在本例中也就是500中的平均每一次）所需时间。 （34.809 ms）
  计算公式：Time taken for tests/Complete requests  ; 也可以这么统计：Time per request/Concurrency Level。

**Transfer rate**: 表示这些请求在单位时间内从服务器获取的数据长度。 （14.08 Kbytes/sec）
  计算公式：Total trnasferred/ Time taken for tests 
  这个统计很好的说明服务器的处理能力达到极限时，其出口宽带的需求量。

**Percentage of requests served within a certain time** (ms) : 这部分数据用于描述每个请求处理时间的分布情况，比如以上测试，
  80%的请求处理时间都不超过6ms，这个处理时间是指前面的Time per request，即对于单个用户而言，平均每个请求的处理时间。

[常用命令]
-n requests Number of requests to perform //本次测试发起的总请求数

-c concurrency Number of multiple requests to make　　 //一次产生的请求数（或并发数）

-t timelimit Seconds to max. wait for responses　　　　//测试所进行的最大秒数，默认没有时间限制。

-r Don't exit on socket receive errors.    // 抛出异常继续执行测试任务

-p postfile File containing data to POST　　//包含了需要POST的数据的文件，文件格式如“p1=1&p2=2”.使用方法是 -p 111.txt

-T content-type Content-type header for POSTing

//POST数据所使用的Content-type头信息，如 -T “application/x-www-form-urlencoded” 。 （配合-p）

-v verbosity How much troubleshooting info to print

//设置显示信息的详细程度 – 4或更大值会显示头信息， 3或更大值可以显示响应代码(404, 200等), 2或更大值可以显示警告和其他信息。 -V 显示版本号并退出。

-C attribute Add cookie, eg. -C “c1=1234,c2=2,c3=3” (repeatable)
//-C cookie-name=value 对请求附加一个Cookie:行。 其典型形式是name=value的一个参数对。此参数可以重复，用逗号分割。
提示：可以借助session实现原理传递 JSESSIONID参数， 实现保持会话的功能，如-C ” c1=1234,c2=2,c3=3, JSESSIONID=FF056CD16DA9D71CB131C1D56F0319F8″ 。

-w Print out results in HTML tables　　//以HTML表的格式输出结果。默认时，它是白色背景的两列宽度的一张表。
