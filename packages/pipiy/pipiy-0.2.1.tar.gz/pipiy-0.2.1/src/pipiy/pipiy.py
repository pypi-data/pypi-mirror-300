import subprocess
import os
from wson import parse_wson, WSONParseError

class PipiyError(Exception):
    pass

def init_project():
    default_wson_content = """{
        module: []
}
"""
    with open("pypackage.ws", "w") as f:
        f.write(default_wson_content.strip())
    print("Initialized pipiy project with default pypackage.ws.")

def get_latest_version(package_name):
    try:
        result = subprocess.check_output([os.sys.executable, '-m', 'pip', 'install', package_name + '==random'], stderr=subprocess.STDOUT, universal_newlines=True)
        lines = result.splitlines()
        for line in lines:
            if "from versions:" in line:
                # 설치 가능한 버전 목록을 찾음
                versions = line.split("from versions: ")[1]
                version_list = versions.strip().split(", ")
                return version_list[-1]  # 가장 최신 버전 반환
    except subprocess.CalledProcessError:
        pass
    return None

def install_package(package_name):
    version = get_latest_version(package_name)
    package_with_version = f"{package_name}=={version}" if version else package_name
    try:
        subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', package_with_version])
        add_to_requirements(package_name, version)
    except subprocess.CalledProcessError as e:
        raise PipiyError(f"Failed to install package {package_with_version}. Error: {str(e)}")

def add_to_requirements(package_name, version):
    try:
        requirements = read_wson_requirements("pypackage.ws")
        module_list = requirements.get('module', [])

        # 버전이 없을 경우 None으로 설정
        if version is None:
            entry = f'{package_name}'
        else:
            entry = f'{package_name} = "{version}"'

        if entry not in module_list:
            module_list.append(entry)

        # WSON 파일에 업데이트된 내용을 작성
        with open("pypackage.ws", "w") as f:
            f.write(f'{{\n    module: [\n        {",\n        ".join(module_list)}\n    ]\n}}')

    except (WSONParseError, FileNotFoundError):
        raise PipiyError("Error updating requirements.")

def read_wson_requirements(file_path):
    with open(file_path, 'r') as file:
        wson_str = file.read()
    return parse_wson(wson_str)

def install_requirements(file_path):
    try:
        requirements = read_wson_requirements(file_path)
        for module in requirements.get('module', []):
            if '=' in module:
                package_name, version = module.split(' = ')
                version = version.strip('"')  # 쌍따옴표 제거
            else:
                package_name, version = module, None
            install_package(package_name.strip())
    except (WSONParseError, FileNotFoundError) as e:
        raise PipiyError(f"Error reading requirements: {str(e)}")
def show_version():
    print("Pipiy version 0.2.1")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Pipiy - WSON package manager')
    subparsers = parser.add_subparsers(dest='command')

    # init 명령어 추가
    init_parser = subparsers.add_parser('init', help='Initialize a new pipiy project.')

    # install 명령어 추가
    install_parser = subparsers.add_parser('install', help='Install modules from a WSON file or a specific module.')
    install_parser.add_argument('module_name', nargs='?', help='Name of the module to install.')
    install_parser.add_argument('file', nargs='?', default='pypackage.ws', help='WSON requirements file.')

    # version 명령어 추가
    version_parser = subparsers.add_parser('version', help='Show the version of pipiy.')

    args = parser.parse_args()

    if args.command == 'init':
        init_project()
    elif args.command == 'install':
        if args.module_name:
            install_package(args.module_name)  # 버전 자동 인식
        else:
            install_requirements(args.file)
    elif args.command == 'version':
        show_version()

if __name__ == "__main__":
    main()