#! /usr/bin/env python

from datetime import datetime

def hello_world(mystery_arg):
	now = datetime.now()
	print(f"Hello world! - {now}\n\tmystery arg: {mystery_arg}")

if __name__ == "__main__":
	hello_world()
