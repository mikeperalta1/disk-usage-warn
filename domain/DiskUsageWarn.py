
"""

Mike's Disk Usage Warner

A simple script to emit warnings out to stderr if a disk's usage surpasses a threshold

Copyright 2019-2024 Mike Peralta; All rights reserved but for following license(s)

Released under the GNU GENERAL PUBLIC LICENSE v3 (See LICENSE file for more)

"""


#
import os
import re
import subprocess
import sys
import yaml


#
class DiskUsageWarn:
	
	def __init__(self):
		
		self.__config_paths = []
		self.__configs = []
		
		self.consume_arguments()
	
	def log(self, s, o=None):
		
		message = "[Disk-Usage-Warn] " + s
		if o:
			message += " " + str(o)
		
		print(message)
		self.execute_command(["logger", message])
	
	def stderr(self, s, o=None):
		
		message = "[Disk-Usage-Warn] " + s
		if o:
			message += " " + str(o)
		
		print(message, file=sys.stderr)
		self.execute_command(["logger", message])
		
	
	def consume_arguments(self):
		
		self.__config_paths = []
		
		for i in range(1, len(sys.argv)):
			
			arg = sys.argv[i]
			
			if arg == "--config":
				i, one_path = self.consume_argument_companion(i)
				self.__config_paths.append(one_path)
				self.log("Found config path argument:", one_path)
	
	@staticmethod
	def consume_argument_companion(arg_index):
		
		companion_index = arg_index + 1
		if companion_index >= len(sys.argv):
			raise Exception("Expected argument after", sys.argv[arg_index])
		
		return companion_index, sys.argv[companion_index]
	
	#
	def consume_configs(self):
		
		#
		self.__configs = []
		
		#
		for path in self.__config_paths:
			
			if os.path.isdir(path):
				
				self.log(path + " is actually a directory; Iterating over contained files (non-recursive)")
				for file_name in os.listdir(path):
					
					one_config_path = os.path.join(path, file_name)
					if re.match(r".+\.yaml$", file_name):
						self.log("Found yaml: " + file_name)
						self.consume_config(one_config_path)
					else:
						self.log("Ignoring non-yaml file: " + file_name)
			
			elif os.path.isfile(path):
				
				self.consume_config(path)
				
			else:
				
				raise Exception("Don't know what to do with config path:" + str(path))
		
		self.log("Consumed " + str(len(self.__configs)) + " configs")
		
	#
	def consume_config(self, path: str):
		
		config = self.load_config(path)
		self.__configs.append(config)
		self.log("Consumed config: " + path)
	
	@staticmethod
	def load_config(path: str):
		
		# Open the file
		f = open(path)
		if not f:
			raise Exception("Unable to open config file: " + path)
		
		# Parse
		config = yaml.safe_load(f)
		
		# Add the config file's own path
		config["path"] = path
		
		return config
	
	def run(self):
		
		self.consume_configs()
		self.do_configs()
	
	def do_configs(self):
	
		for config in self.__configs:
			self.do_config(config)
	
	def do_config(self, config):
		
		# Pull the max usage
		self.assert_config_key(config, "max-usage", [int, str, list])
		max_percent = str(config["max-usage"])
		match = re.match("(?P<integer_percent>[0-9]+)%?", max_percent)
		if not match:
			raise Exception("Unable to parse configuration value for max-usage (integer percent)")
		max_percent = int(match.group("integer_percent"))
		
		# Check each device
		self.assert_config_key(config, "devices", list)
		for device in config["devices"]:
			
			device_usage = self.get_device_usage(device)
			self.log("Device Usage: " + device + " ==> " + str(device_usage) + "%")
			if device_usage > max_percent:
				error_message =	("Device " + str(device) + " is too full"
					+ "; Using " + str(device_usage) + "%"
					+ ", but maximum is " + str(max_percent) + "%"
				)
				self.stderr(error_message)
	
	@staticmethod
	def assert_config_key(config, key, types):
		
		if not isinstance(types, list):
			types = [types]
		if len(types) == 0:
			types = [list]
		
		if key not in config.keys():
			raise Exception("Missing required config key: " + str(key))
		
		for t in types:
			if isinstance(config[key], t):
				return True
		
		raise Exception("Config key \"" + key + "\" should be one of these types \"" + str(types) + "\"")
	
	def get_device_usage(self, device):
		
		args = ["df", device]
		
		returncode, stdout, stderr = self.execute_command(args)
		if returncode != 0:
			raise Exception("Failed to poll device usage\n" + stderr)
		
		# Grab percent
		pattern = re.compile(".*?(?P<percent_integer>[0-9]+)%.*?", re.DOTALL)
		match = pattern.match(str(stdout))
		if not match:
			raise Exception("Unable to parse device usage from:\n" + str(stdout))
		percent_integer = int(match.group("percent_integer"))
		
		return percent_integer
	
	@staticmethod
	def execute_command(args):
		
		# Start the process
		#process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
		process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		#
		stdout, stderr = process.communicate()
		
		if stdout:
			stdout = stdout.decode()
		if stderr:
			stderr = stderr.decode()
		
		return process.returncode, stdout, stderr
