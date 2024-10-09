import subprocess
import os
import toml
from wson import parse_wson, WSONParseError

class PipiyError(Exception):
    pass

def init_project():
    # 기본 WSON 구조 수정
    default_wson_content = """{
        module: []
}
"""
    with open("pypackage.ws", "w") as f:
        f.write(default_wson_content.strip())
    print("Initialized pipiy project with default pypackage.ws.")

def install_package(package_name, version):
    package_with_version = f"{package_name} = \"{version}\"" if version else package_name
    try:
        subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', package_with_version])
        # WSON 파일에 패키지 추가
        add_package_to_wson(package_name, version)
    except subprocess.CalledProcessError as e:
        raise PipiyError(f"Failed to install package {package_with_version}. Error: {str(e)}")

def add_package_to_wson(package_name, version):
    # 현재 WSON 파일 읽기
    try:
        with open("pypackage.ws", 'r') as file:
            # WSON 형식으로 읽기
            wson_content = file.read()
            requirements = parse_wson(wson_content)
    except (FileNotFoundError, WSONParseError):
        requirements = {"module": []}

    # 모듈 이름과 버전 추가
    if version:
        package_entry = f"{package_name} = \"{version}\""
    else:
        package_entry = package_name

    requirements["module"].append(package_entry)

    # 업데이트된 WSON 파일 작성
    with open("pypackage.ws", 'w') as file:
        # WSON 형식으로 작성
        file.write("{\n    module: [\n")
        for entry in requirements["module"]:
            file.write(f'        {entry},\n')  # 문자열 형태로 작성
        file.write("    ]\n}")

def read_wson_requirements(file_path):
    with open(file_path, 'r') as file:
        wson_str = file.read()
    return parse_wson(wson_str)

def install_requirements(file_path):
    try:
        requirements = read_wson_requirements(file_path)
        for module_entry in requirements.get('module', []):
            # "module = version" 형식으로 분리
            if '=' in module_entry:
                package_name, version = module_entry.split(" = ")
                install_package(package_name.strip(), version.strip('"'))
            else:
                install_package(module_entry.strip(), None)
    except (WSONParseError, FileNotFoundError) as e:
        raise PipiyError(f"Error reading requirements: {str(e)}")

def show_version():
    print("Pipiy version 0.1.9")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Pipiy - WSON package manager')
    subparsers = parser.add_subparsers(dest='command')

    # init 명령어 추가
    init_parser = subparsers.add_parser('init', help='Initialize a new pipiy project.')

    # install 명령어 추가
    install_parser = subparsers.add_parser('install', help='Install modules from a WSON file or a specific module.')
    install_parser.add_argument('module_name', nargs='?', help='Name of the module to install.')
    install_parser.add_argument('version', nargs='?', help='Version of the module to install.')
    install_parser.add_argument('-p', '--package-file', default='pypackage.ws', help='WSON requirements file.')

    # version 명령어 추가
    version_parser = subparsers.add_parser('version', help='Show the version of Pipiy.')

    args = parser.parse_args()

    if args.command == 'init':
        init_project()
    elif args.command == 'install':
        if args.module_name:
            install_package(args.module_name, args.version)
        else:
            install_requirements(args.package_file)
    elif args.command == 'version':
        show_version()

if __name__ == "__main__":
    main()
