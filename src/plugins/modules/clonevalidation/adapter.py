import pickle
from flask import request
import xml.etree.ElementTree as ET
from os import path

def run_clonevalidation(context, *args, **kwargs):

	arguments = context.parse_args('ValidateClone', 'nicad', *args, **kwargs)

	tree2 = ET.parse(arguments['data'])
	root = tree2.getroot()
	totalClonePairs = len(root)

	mlValidationCount = 0

	mlValidation_output_file = arguments['data'] + '.mlValidated'
	if path.exists(mlValidation_output_file):
		mlValidationCount = sum(1 for line in open(mlValidation_output_file))
	else:
		with open(mlValidation_output_file, "w") as new_file:
			pass

	for aCloneIndex in range(mlValidationCount, totalClonePairs):
		fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, clones_validated,	total_clones = get_next_clone_pair_for_validation(arguments['data'], mlValidation_output_file)

		true_probability = app_code_clone_getValidationScore(fragment_1_clone, fragment_2_clone, 'java')

		with open(mlValidation_output_file, "a") as validationFile:
			if true_probability >= arguments['threshold']:
				validationFile.write('true' + ',' + fragment_1_path + ',' + fragment_1_startline + ',' + fragment_1_endline+','+fragment_2_path+','+fragment_2_startline+','+fragment_2_endline + '\n')
			else:
				validationFile.write('false' + ',' + fragment_1_path + ',' + fragment_1_startline + ',' + fragment_1_endline + ',' + fragment_2_path + ',' + fragment_2_startline + ',' + fragment_2_endline + '\n')

	return mlValidation_output_file

def run_clonevalidationmanually(context, *args, **kwargs):

	arguments = context.parse_args('ValidateCloneManually', 'nicad', *args, **kwargs)

	# getting the example program name
	#manual_validation_response = 'true'


	theValidationFile = arguments['data'] + '.validated'

	saveManualValidationResponse(theValidationFile, arguments['response'], arguments['fragment1'],
	                             arguments['startline1'], arguments['endline1'], arguments['fragment2'], arguments['startline2'], arguments['endline2'])

	# with open(theValidationFile, "a") as validationFile:
	# 	validationFile.write(arguments['response'] + ',' + arguments['fragment1'] + ',' + arguments['startline1'] + ',' + arguments['endline1']+','+ arguments['fragment2']+','+ arguments['startline2']+','+ arguments['endline2'] + '\n')

	fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, clones_validated, total_clones = get_next_clone_pair_for_validation(arguments['data'], theValidationFile)
	
	context.out.append("fragment1: {0}, startline1: {1}, endline1: {2}, clone1: {3}, fragment2: {4}, startline2: {5}, endline2: {6}, clone2: {7}, clones_validated: {8}, total_clones: {9}".format(fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, clones_validated, total_clones))

	return theValidationFile

def run_clonevalidationstats(context, *args, **kwargs):

	arguments = context.parse_args('CloneValidationStat', 'nicad', *args, **kwargs)

	with open(arguments['data'], "r") as validationFile:
		validationResponseLines = validationFile.readlines()

	totalClones = len(validationResponseLines)
	trueCount = 0

	for aValidationLine in validationResponseLines:
		aResponse = aValidationLine.split(',')[0]
		if aResponse =='true':
			trueCount = trueCount + 1

# var totalClones = '<br>Total Clone Pairs: ' + option.totalClonePairs;
#             var truePositives = '<br>True Positives: ' + option.trueClones;
#             var falsePositives = '<br>False Positives: ' + (option.totalClonePairs -  option.trueClones);
#             var precision = '<br>Precision: ' + (option.trueClones / option.totalClonePairs)


#             var stats = totalClones + truePositives + falsePositives + precision;

	return trueCount, totalClones

def saveManualValidationResponse(theValidationFile, response, fragment_1_path, fragment_1_start_line, fragment_1_end_line, fragment_2_path, fragment_2_start_line, fragment_2_end_line):

	with open(theValidationFile, "a") as validationFile:
		validationFile.write(response + ',' + fragment_1_path + ',' + fragment_1_start_line + ',' + fragment_1_end_line+','+fragment_2_path+','+fragment_2_start_line+','+fragment_2_end_line + '\n')


def get_next_clone_pair_for_validation(theCloneFile, theValidationFile):
	# getting the example program name

	tree2 = ET.parse(theCloneFile)
	root = tree2.getroot()

	nextCloneIndex = 0

	if path.exists(theValidationFile):
		nextCloneIndex = sum(1 for line in open(theValidationFile))
	else:
		with open(theValidationFile, "w") as new_file:
			pass

	return root[nextCloneIndex][0].attrib['file'], root[nextCloneIndex][0].attrib['startline'], root[nextCloneIndex][0].attrib['endline'], root[nextCloneIndex][1].text, root[nextCloneIndex][2].attrib['file'], root[nextCloneIndex][2].attrib['startline'], root[nextCloneIndex][2].attrib['endline'], root[nextCloneIndex][3].text, nextCloneIndex+1, len(root)


@app_code_clone.route('/txln', methods=['POST'])
def txln():
	# getting the txl and the input file to parse
	txl_source = request.form['txl_source']
	input_to_parse = request.form['input_to_parse']

	# generate a unique random file name for preventing conflicts
	fileName = str(uuid.uuid4())
	txl_source_file = 'app_txl_cloud/txl_tmp_file_dir/' + fileName + '.txl'

	fileName = str(uuid.uuid4())
	input_to_parse_file = 'app_txl_cloud/txl_tmp_file_dir/' + fileName + '.txt'

	# write submitted txl and input to corresponding files
	with open(txl_source_file, "w") as fo:
		fo.write(txl_source)

	with open(input_to_parse_file, "w") as fo:
		fo.write(input_to_parse)

	# parsing
	p = subprocess.Popen(['/usr/local/bin/txl', '-Dapply', txl_source_file, input_to_parse_file], stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
	# p = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()

	# once done remove the file
	#os.remove(txl_source_file)
	#os.remove(input_to_parse_file)

	# preparing the log file for better readabilty...
	# err = err.replace('\n','<br>') #add new line for html
	err = str(err, 'utf-8')
	out = str(out, 'utf-8')
	err = err.replace(txl_source_file, 'YOUR_TXL_FILE')
	err = err.replace(input_to_parse_file, 'YOUR_INPUT_FILE')

	return jsonify({'txl_log': err, 'txl_output': out})


@app_code_clone.route('/load_example_txl_programn', methods=['POST'])
def load_example_txl_programn():
	# getting the example program name
	example_name = request.form['txl_example_program_name']

	txl_example_program_dir = 'app_txl_cloud/txl_sources/examples/'

	file_location = txl_example_program_dir + example_name + '/' + example_name

	txl_source = ''
	with open(file_location + '.txl', 'r') as f:
		for line in f:
			txl_source = txl_source + line

	input_to_parse = ''
	with open(file_location + '.txt', 'r') as f:
		for line in f:
			input_to_parse = input_to_parse + line

	# txl_source = str(txl_source, 'utf-8')
	return jsonify({'example_txl_source': txl_source, 'input_to_parse': input_to_parse})


########################################################################################################################
########################################################################################################################
########################################################################################################################
#############################  MACHINE LEARNING MODEL ##################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


def app_code_clone_getValidationScore(sourceCode1, sourceCode2,model, lang='java' ):

	#load the trained Neural Net
	with open(model, 'rb') as fileObject:
		loaded_fnn = pickle.load(fileObject, encoding='latin1')

	type1sim_by_line, type2sim_by_line, type3sim_by_line = app_code_clone_similaritiesNormalizedByLine(sourceCode1, sourceCode2,lang)
	type1sim_by_token, type2sim_by_token, type3sim_by_token = app_code_clone_similaritiesNormalizedByToken(sourceCode1, sourceCode2,lang)

	network_prediction = loaded_fnn.activate(
	    [type2sim_by_line, type2sim_by_line, type3sim_by_line, type1sim_by_token, type2sim_by_token, type3sim_by_token])

	return network_prediction[1]


def app_code_clone_execTxl(txlFilePath, sourceCode, lang, saveOutputFile=False):
	# get an unique file name for storing the code temporarily
	fileName = str(uuid.uuid4())
	sourceFile = '/home/ubuntu/Webpage/txl_tmp_file_dir/' + fileName + '.txt'

	# write submitted source code to corresponding files
	with open(sourceFile, "w") as fo:
		fo.write(sourceCode)

	# get the required txl file for feature extraction
	# txlPath = '/home/ubuntu/Webpage/txl_features/txl_features/java/PrettyPrint.txl'

	# do the feature extraction by txl
	p = subprocess.Popen(['/usr/local/bin/txl', '-Dapply', txlFilePath, sourceFile], stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
	out, err = p.communicate()

	# convert to utf-8 format for easier readibility
	out = str(out, 'utf-8')
	err = str(err, 'utf-8')

	err = err.replace(sourceFile, 'YOUR_SOURCE_FILE')
	err = err.replace(txlFilePath, 'REQUIRED_TXL_FILE')

	# once done remove the temp file
	os.remove(sourceFile)

	if saveOutputFile == False:
		return out, err
	else:
		outputFileLocation = str(uuid.uuid4())
		outputFileLocation = '/home/ubuntu/Webpage/txl_tmp_file_dir/' + \
		    outputFileLocation + '.txt'
		with open(outputFileLocation, "w") as fo:
			fo.write(out)

		return outputFileLocation, out, err


def app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath):
	saveOutputFile = True
	outputFileLocation1, out1, err1 = app_code_clone_execTxl(
	    txlFilePath, sourceCode1, lang, saveOutputFile)
	outputFileLocation2, out2, err2 = app_code_clone_execTxl(
	    txlFilePath, sourceCode2, lang, saveOutputFile)

	p = subprocess.Popen(['/usr/bin/java', '-jar', '/home/ubuntu/Webpage/txl_tmp_file_dir/calculateCloneSimilarity.jar',
                       outputFileLocation1, outputFileLocation2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	similarityValue, err = p.communicate()

	similarityValue = str(similarityValue, 'utf-8')
	similarityValue = similarityValue.replace('\n', '')
	err = str(err, 'utf-8')

	# once done remove the temp files
	os.remove(outputFileLocation1)
	os.remove(outputFileLocation2)

	return similarityValue


def app_code_clone_similaritiesNormalizedByLine(sourceCode1, sourceCode2, lang):
	# getting the txl and the input file to parse
	# sourceCode1 = request.form['sourceCode_1']
	# sourceCode2 = request.form['sourceCode_2']
	# lang = request.form['lang']

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/PrettyPrint.txl'
	type1sim_by_line = app_code_clone_getCodeCloneSimilarity(
	    sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/normalizeLiteralsToDefault.txl'
	type2sim_by_line = app_code_clone_getCodeCloneSimilarity(
	    sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/normalizeLiteralsToZero.txl'
	type3sim_by_line = app_code_clone_getCodeCloneSimilarity(
	    sourceCode1, sourceCode2, lang, txlFilePath)

	#out = {'type_1_similarity_by_line': type1sim_by_line, 'type_2_similarity_by_line': type2sim_by_line,
	#	   'type_3_similarity_by_line': type3sim_by_line}

	#return jsonify({'error_msg': 'None',
	#				'log_msg': 'Preprocessing Source Codes...\nNormalizing Source Codes...\nCalculating Similarities...\nDone.',
	#				'output': out})

	return type1sim_by_line, type2sim_by_line, type3sim_by_line


def app_code_clone_similaritiesNormalizedByToken(sourceCode1, sourceCode2, lang):
	# getting the txl and the input file to parse
	# sourceCode1 = request.form['sourceCode_1']
	# sourceCode2 = request.form['sourceCode_2']
	# lang = request.form['lang']

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/consistentRenameIdentifiers.txl'
	type1sim_by_token = app_code_clone_getCodeCloneSimilarity(
	    sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/normalizeLiteralsToZero.txl'
	type2sim_by_token = app_code_clone_getCodeCloneSimilarity(
	    sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/normalizeLiteralsToZero.txl'
	type3sim_by_token = app_code_clone_getCodeCloneSimilarity(
	    sourceCode1, sourceCode2, lang, txlFilePath)

	# out = {'type_1_similarity_by_token': type1sim_by_token, 'type_2_similarity_by_token': type2sim_by_token,
	# 	   'type_3_similarity_by_token': type3sim_by_token}
    #
	# return jsonify({'error_msg': 'None',
	# 				'log_msg': 'Preprocessing Source Codes...\nNormalizing Source Codes...\nCalculating Similarities...\nDone.',
	# 				'output': out})

	return type1sim_by_token, type2sim_by_token, type3sim_by_token
