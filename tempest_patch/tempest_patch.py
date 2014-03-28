#!/usr/bin/python
import io
import fileinput
import os



def find_end_of_method_call(number_of_begin_method_call, path):
	with io.open(path,"r") as logfile:
		for num, line in enumerate(logfile, 1):
			if num > number_of_begin_method_call:
				if line.replace('\n', '')[-1] == ')':
					return num + 1

def _get_response_body(insert_string, resource_name):
	splited_string = insert_string.split('=')
	splited_string = splited_string[0].split(',')
	if len(splited_string) == 1:
		return splited_string[0].strip()
	else:
		if resource_name in resources:
			resource_name = resources[resource_name]
		return splited_string[1].strip() + '["' + resource_name + '"]'

def _get_resource_name(insert_string):
	resource_name = ''
	splited_string = insert_string.split('=')
	splited_string = splited_string[1].split('.')
	for i in splited_string:
		if 'create' in i and '_create' not in i:
			i = i.replace('create_', '')
			for j in i:
				if j == '(':
					break
				else:
					resource_name = resource_name + j
	return resource_name
def _classmethod_or_not(insert_string):
	if 'cls' in insert_string:
		return 'cls'
	else:
		return 'self'

def _get_ident(insert_string):
    indent = ''
    for i in insert_string:
		if i ==' ':
			indent = indent + i
		else:
			return indent
def create_string(insert_string):
	response_body =  ''
	indent = _get_ident(insert_string)
	resource_name = _get_resource_name(insert_string)
	response_body =  _get_response_body(insert_string, resource_name)
	method_type = _classmethod_or_not(insert_string)
	if resource_name == 'bulk_network' or resource_name == 'bulk_subnet' or resource_name == 'bulk_port':
		final_string = indent + 'for i in ' + response_body +':\n' +indent + '    ' + method_type + '.set_resource(i["id"], "' + resource_name + '")\n'
	else:
		final_string = indent + method_type + '.set_resource(' + response_body + '["id"], "' + resource_name + '")\n'
	return final_string 

def validate_string(string):
    if 'self.client.create' in string or "self.create" in string or "cls.create" in string:
    	if '#' in string or '=' not in string:
    		return False
    	else:
    		return True
    else:
    	return False


def add_decorators_safe_setup_to_file(path_to_file):
    for line in fileinput.input(path_to_file, inplace = 1):
        if 'def setUpClass(cls):' in line:
    	    indent = _get_ident(line)
    	    print indent + '@safe_setup\n', line,
        else:
    	    print line,
    fileinput.close()

def add_import_safe_setup_to_file(path_to_file):
    first_time= False
    for line in fileinput.input(path_to_file, inplace = 1):
        if 'import' in line and not first_time:
    	    indent = _get_ident(line)
    	    print indent + 'from tempest.test import safe_setup\n', line,
    	    first_time = True
        else:
    	    print line,
    fileinput.close()

def edit_test_py():
	path_to_test_py = '../tempest/test.py'
	safe_setup_method = ''
	first_time= False
	with io.open('safe_setup_method',"r") as safe_setup:
		for line in safe_setup:
			safe_setup_method = safe_setup_method + line
	finput = fileinput.input(path_to_test_py, inplace = 1)
	for line in finput:
		if 'def skip_because(*args, **kwargs):' in line:
			print safe_setup_method, line,
		elif 'BaseTestCase' in line:
			print line,
			end = find_end(finput, ')')
			indent = _get_ident(end)
			end = end[:-3] + ',\n' +  indent + 'resources.Resources):\n'
			print end, 
		elif 'import' in line and not first_time:
			indent = _get_ident(line)
			print indent + 'from tempest_patch import resources\n', line,
			first_time = True
		elif 'def tearDownClass' in line:
			print line,
			end = find_empty_line(finput)
			indent = _get_ident(end)
			end =  indent + '		cls.tearDownTempestResources()\n'
			print end
		else:
			print line, 

	fileinput.close()

def find_end(finput, endsymbol):
	for line in finput:
		if endsymbol in line:
			return line
		else:
			print line,

def find_empty_line(finput):
	for line in finput:
		if line == '\n':
			return line
		else:
			print line,

if __name__ == "__main__": 
	edit_test_py()
	resources = {'floating_ip' : 'floatingip',
				 'bulk_network' : 'networks',
				 'bulk_subnet' : 'subnets',
				 'bulk_port' : 'ports'}

	directory = '../tempest/api/network/'
	files = os.listdir(directory)
	files_for_patching = []
	for i in files:
		ext = i.split('.')
		if 'test_' in i and ext[1] == 'py':
			files_for_patching.append(i)
	for file_for_patching in files_for_patching:
		places_for_insert ={}
		PATH = '../tempest/api/network/' + file_for_patching
		add_import_safe_setup_to_file(PATH)
		add_decorators_safe_setup_to_file(PATH)
		with io.open(PATH,"r") as logfile:
		  for num, line in enumerate(logfile, 1):
		 	if validate_string(line):
		 		if line.replace('\n', '')[-1] != ')':
					result = find_end_of_method_call(num, PATH)
					places_for_insert[result] = create_string(line)
				else:
					places_for_insert[num +1] = create_string(line)
		for num, line in enumerate(fileinput.input(PATH, inplace = 84), 1):
			if num in places_for_insert.keys():
				print places_for_insert[num], line,
			else:
				print line,
		fileinput.close()