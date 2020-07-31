import donut
import os
import base64


async def donut_handler(services, args):
    """Handle donut special payloads

    :param services: CALDERA services
    :type services: dict
    :param args: HTTP request arguments
    :type args: multidict
    :return: Payload, display name
    :rtype: string, string
    """
    _, donut_path = await services.get('file_svc').find_file_path(args.get('file'), location='payloads')
    donut_dir, donut_file = os.path.split(donut_path)
    exe_path = os.path.join(donut_dir, '{}.exe'.format(donut_file))
    os.replace(src=donut_path, dst=exe_path)
    parameters = await _get_parameters(services.get('data_svc'), args.get('file'))
    shellcode = donut.create(file=exe_path, params=parameters)
    _write_shellcode_to_file(shellcode, exe_path)
    os.replace(src=exe_path, dst=donut_path)
    return donut_file, donut_file  # payload, display_name

""" PRIVATE """


def _write_shellcode_to_file(shellcode, file_path):
    """Write shellcode to file path

    :param shellcode: Shellcode byte string
    :type shellcode: bytes
    :param file_path: File path to write to
    :type file_path: string
    """
    try:
        with open(file_path, 'wb') as f:
            f.write(shellcode)
    except Exception as ex:
        print(ex)


async def _get_parameters(data_svc, file_name):
    """Generate command line parameters from latest matching link

    Parameters are everything after the first instance of the payload
    (donut file name) in the ability command

    :param data_svc: Data service to collect operations
    :type data_svc: DataService
    :return: Donut parameters
    :rtype: string
    """
    parameters = ''
    operations = await data_svc.locate('operations', match=dict(state='running'))
    potential_links = [chain for operation in operations for chain in operation.chain
                       if not chain.finish and chain.ability.executor.startswith('donut')
                       and file_name in chain.ability.payloads]
    if potential_links:
        link = sorted(potential_links, key=lambda l: l.decide)[0]
        operation = [operation for operation in operations if operation.has_link(link.id)][0]
        if operation.obfuscator == 'plain-text':
            decoded_command = base64.b64decode(link.command).decode('utf-8')
            if file_name in decoded_command:
                parameters = ''.join(decoded_command.split(file_name)[1:])
            else:
                parameters = decoded_command
    return parameters
