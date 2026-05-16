#sample logs for training
SSH_SAMPLE = """Jan 10 03:45:22 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jan 10 03:45:23 server sshd[1235]: Failed password for root from 192.168.1.105 port 22
Jan 10 03:45:24 server sshd[1236]: Failed password for root from 192.168.1.105 port 22
Jan 10 03:46:10 server sshd[1237]: Accepted password for john from 10.0.0.2 port 22
Jan 10 04:12:33 server sshd[1238]: Failed password for admin from 203.0.113.42 port 22
Jan 10 04:12:35 server sshd[1239]: Failed password for admin from 203.0.113.42 port 22"""

APACHE_SAMPLE = """192.168.1.105 - - [10/Jan/2024:03:45:22 +0000] "GET /login HTTP/1.1" 200 512
192.168.1.105 - - [10/Jan/2024:03:45:23 +0000] "GET /admin HTTP/1.1" 404 128
192.168.1.105 - - [10/Jan/2024:03:45:24 +0000] "GET /admin HTTP/1.1" 404 128
192.168.1.105 - - [10/Jan/2024:03:45:25 +0000] "GET /admin HTTP/1.1" 404 128
203.0.113.42  - - [10/Jan/2024:04:12:33 +0000] "POST /login HTTP/1.1" 200 256
10.0.0.2      - - [10/Jan/2024:04:15:10 +0000] "GET /index HTTP/1.1" 500 64"""

WINDOWS_SAMPLE = """EventID: 4625 | Time: 2024-01-10 03:45:22 | User: Administrator | IP: 192.168.1.105 | Status: Failure
EventID: 4625 | Time: 2024-01-10 03:45:23 | User: Administrator | IP: 192.168.1.105 | Status: Failure
EventID: 4625 | Time: 2024-01-10 03:45:24 | User: Administrator | IP: 192.168.1.105 | Status: Failure
EventID: 4624 | Time: 2024-01-10 03:46:10 | User: john | IP: 10.0.0.2 | Status: Success
EventID: 4625 | Time: 2024-01-10 04:12:33 | User: admin | IP: 203.0.113.42 | Status: Failure
EventID: 4634 | Time: 2024-01-10 04:13:00 | User: john | IP: 10.0.0.2 | Status: Logout"""
