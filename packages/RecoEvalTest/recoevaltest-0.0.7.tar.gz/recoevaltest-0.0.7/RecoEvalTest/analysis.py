# write a class to analyze data
# input is a file path, use pandas to read the file, and preprocess the data
# then wirte a function to calculate the precision and recall given two columns

import pandas as pd

class DataAnalysis:
	def __init__(self, file_path):
		self.file_path = file_path
		sep = ''
		with open(file_path, 'r', encoding="utf8") as f:
			first_line = f.readline()
			if '\t' in first_line:
				sep = '\t'
			elif ',' in first_line:
				sep = ','
			else:
				raise ValueError('The file does not contain the valid separator')
		self.df = pd.read_csv(file_path, sep=sep)
	
	def calculate_prf(self, ground_truth_colunm, predict_column):
		"""
		Calculate the precision and recall of the prediction
		:param ground_truth_colunm: ground truth column
		:param predict_column: predict column
		:return: precision, recall
		"""
		# remove rows with missing values in the two columns
		self.df = self.df.dropna(subset=[ground_truth_colunm, predict_column])
		ground_truth = self.df[ground_truth_colunm]
		predict = self.df[predict_column]
		TP = 0
		FP = 0
		FN = 0
		for i in range(len(ground_truth)):
			if ground_truth[i] == 1 and predict[i] == 1:
				TP += 1
			elif ground_truth[i] == 0 and predict[i] == 1:
				FP += 1
			elif ground_truth[i] == 1 and predict[i] == 0:
				FN += 1
		TN = len(ground_truth) - TP - FP - FN
		if TP + FP == 0:
			precision = 0
		else:
			precision = TP / (TP + FP)
		if TP + FN == 0:
			recall = 0
		else:
			recall = TP / (TP + FN)
		if precision + recall == 0:
			F = 0
		else:
			F = 2 * precision * recall / (precision + recall)
		positive = sum(ground_truth)
		return TP, FP, TN, FN, precision, recall, F, positive
