from os import path
thispath = path.abspath(path.dirname(__file__))

def demo_service(context, *args, **kwargs):
	arguments = context.parse_args('findclonepairs', 'nicad', *args, **kwargs)
	cmdargs = [arguments['data'], arguments['threshold']]
	cmdargs.append(arguments['minclonesize'])
	cmdargs.append(arguments['maxclonesize'])
	out, _ = context.docker_run('scicloneservice', 'FindClonePairs', *arguments, cwd='/tools/nicad/scripts/')
	return out
