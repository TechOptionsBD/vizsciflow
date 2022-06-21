from git import Repo

def run_gitclone(context, *args, **kwargs):

    arguments = context.parse_args('gitclone', 'git', *args, **kwargs)
    srcpath = arguments['data'] if 'data' in arguments.keys() else context.createoutdir()
    repo = Repo.clone_from(url=arguments['url'], to_path=srcpath, recursive=True)

    return repo.working_dir