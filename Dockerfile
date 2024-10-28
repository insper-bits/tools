# Use a lightweight Python base image
FROM prairielearn/grader-python

RUN dnf install -y git
RUN pip install git+https://github.com/insper-bits/tools
