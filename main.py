#! /usr/bin/env python

from datetime import datetime

def hello_world():
	now = datetime.now()
	print(f"Hello world! - {now}")

if __name__ == "__main__":
	hello_world()
