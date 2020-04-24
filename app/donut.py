import donut
import os


async def donut_handler(services, args) -> (str, str):
    _, file_name = await services.get('file_svc').find_file_path(args.get('file'), location='payloads')
    dir_path, donut_ext = os.path.split(file_name)
    exe_path = os.path.join(dir_path, '%s.exe' % donut_ext.split('.')[0])
    os.replace(src=file_name, dst=exe_path)
    shellcode = donut.create(file=exe_path)
    _write_shellcode_to_file(shellcode, exe_path)
    os.replace(src=exe_path, dst=file_name)
    return donut_ext, donut_ext  # payload, display_name

""" PRIVATE """


def _write_shellcode_to_file(shellcode, file_name):
    try:
        with open(file_name, 'wb') as f:
            f.write(shellcode)
    except Exception as ex:
        print(ex)
