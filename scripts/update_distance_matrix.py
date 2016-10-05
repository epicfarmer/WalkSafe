if __name__ == '__main__':
	import matplotlib.pyplot as plt
	nbins = 1
	processed = []
	while nbins < 4:
		nbins *= 2
		print nbins
		coord_list = gridBaltimore.bins(nbins)
		for coords in coord_list:
			coords = list(coords)
			if coords not in processed:
				processed.append(coords)

	print len(processed)
	print processed

	x = map(lambda i: i[0], processed)
	y = map(lambda i: i[1], processed)

	plt.scatter(x, y)
	plt.show()