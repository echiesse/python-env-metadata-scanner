import os
import sys

import contextlib


def load_text_from_file(path):
    content = None
    with contextlib.suppress(Exception):
        with open(path) as file:
            content = file.read()
    return content


def save_text_to_file(text, path):
    with open(path, 'w') as file:
        file.write(text)


def split_package_name(package_name):
    name = package_name.replace('.dist-info', '')
    name, version = name.split('-')
    return name, version


def scan_licenses(site_packages_dir):
    current_dir = os.getcwd()
    os.chdir(site_packages_dir)
    dirs = os.listdir('.')
    dist_info_dirs = list(filter(lambda name: 'dist-info' in name, dirs))
    packages = []
    for dist_info_dir in dist_info_dirs:
        package_name, version = split_package_name(dist_info_dir)
        metadata = load_text_from_file(os.path.join(dist_info_dir, 'METADATA'))

        lines = list(map(str.strip, metadata.split('\n')))
        license_lines = list(filter(lambda line: line.startswith('License:'), lines))
        license = 'ABSENT'
        if len(license_lines) > 0:
            license = license_lines[0].replace('License:', '').strip()

        packages.append((package_name, version, license))
    os.chdir(current_dir)

    return packages


def load_projects(project_locator_file):
    content = load_text_from_file(project_locator_file)
    if content is None:
        return None

    content = content.strip()
    lines = list(map(str.strip, content.split('\n')))
    projects = {}
    for project_info in lines:
        project_name, lib_path = project_info.split('=')
        project_name = project_name.strip()
        lib_path = lib_path.strip()
        projects[project_name] = lib_path

    return projects


def run(project_locator_file):
    projects = load_projects(project_locator_file)
    titles = ['Package', 'Version', 'License']
    for project_name, lib_path in projects.items():
        output_lines = []
        output_lines.append(';'.join(titles))
        packages = scan_licenses(lib_path)
        for package_info in packages:
            name, version, license = package_info
            output_lines.append(f'{name};{version};{license}')

        save_text_to_file('\n'.join(output_lines), f'{project_name}-licenses.csv')


if __name__ == '__main__':
    run(sys.argv[1])
