from pbxproj import XcodeProject
import os


def list_swift_files(project_path, target_name):
    """
    Lists Swift files for a target name.

    :param project_path: path to .xcodeproj file
    :param target_name: name of the target
    :return:
    """
    (project_directory, _) = os.path.split(project_path)
    project = XcodeProject.load(os.path.join(project_path, 'project.pbxproj'))
    target = project.get_target_by_name(target_name)

    build_phases = (project.objects[p] for p in target.buildPhases if project.objects[p].isa == 'PBXSourcesBuildPhase')
    build_files = (f for p in build_phases for f in p.files)
    build_files = (project.objects[project.objects[f].fileRef] for f in build_files)
    files = (__full_path(project, file) for file in build_files)
    return [os.path.join(project_directory, file_path) for file_path in files]


def __full_path(project, file_ref):
    folder = ''

    if file_ref.sourceTree == '<group>':
        parent = __parent_group(project, file_ref)

        if parent:
            folder = __full_path(project, parent)
    elif file_ref.sourceTree == '<absolute>':
        folder = '/'

    if 'path' in file_ref:
        return os.path.join(folder, file_ref['path'])
    else:
        return folder


def __parent_group(project, file_ref):
    for group in project.objects.get_objects_in_section('PBXGroup'):
        if group.has_child(file_ref.get_id()):
            return group
