"""
This module provides a function called merge which can merge a list.
Say the input list is [2, 2, 0, 4], then we will get [4, 4, 0, 0] back.
"""


def merge(input_list):

	def rearrange_lists(in_list):
		# make the non_zero numbers to left
		_list = list()
		for dummy_num in range(len(in_list)):
			if in_list[dummy_num] != 0:
				_list.append(in_list[dummy_num])
			else:
				continue
		for dummy_num in range(len(in_list) - len(_list)):
			_list.append(0)
		return _list

	def do_add_numbers_in_list(in_list):
		# the following codes are used for adding numbers
		_index_list = list()
		out_list = list()
		for _index in range(len(rearrange_list)):
			if rearrange_list[_index] == 0 or _index == len(rearrange_list) - 1:
				# there is no need to deal with the numbers which is zero or which is the last number
				out_list.append(rearrange_list[_index])
				continue
			if _index - 1 in _index_list:
				# this means the two numbers we have already added them, so pass
				continue
			if rearrange_list[_index] == rearrange_list[_index + 1]:
				# add the two identical numbers
				out_list.append(2 * rearrange_list[_index])
				_index_list.append(_index)
			else:
				out_list.append(rearrange_list[_index])
		# to make the length of the two lists equals to each other
		for dummy_num in range(len(rearrange_list) - len(out_list)):
			out_list.append(0)
		# rearrange the output
		out_list = rearrange_lists(out_list)
		return out_list

	rearrange_list = rearrange_lists(input_list)
	output_list = do_add_numbers_in_list(rearrange_list)
	return output_list


if __name__ == '__main__':
	# testing part
	print(merge([2, 2, 0, 4]))
	print(merge([2, 0, 4, 2, 2]))
	print(merge([2, 2, 2, 2, 2]))
	print(merge([8, 16, 16, 8]))