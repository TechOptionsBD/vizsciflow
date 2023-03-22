from os import path
import matplotlib.pyplot as plt

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('ChartTest', 'demo', *args, **kwargs)
	
	plt.plot(arguments["data"], arguments["data2"])
	plt.xlabel('Months')
	plt.ylabel('Books Read')

	output = path.join(context.gettempdir(), 'books_read.png')
	plt.savefig(output)
	return output