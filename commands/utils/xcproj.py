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
    files = []

    for build_phase_id in target.buildPhases:
        build_phase = project.objects[build_phase_id]
        if build_phase.isa == 'PBXSourcesBuildPhase':
            for build_file_id in build_phase.files:
                build_file = project.objects[build_file_id]
                file_ref = project.objects[build_file.fileRef]
                files.append(__full_path(project, file_ref))

    return [os.path.join(project_directory, file_path) for file_path in files]


def __full_path(project, file_ref):
    folder = None

    if file_ref.sourceTree == '<group>':
        parent = __parent_group(project, file_ref)

        if parent:
            folder = __full_path(project, parent)
    elif file_ref.sourceTree == '<absolute>':
        folder = '/'

    folder = folder if folder else ''

    if 'path' in file_ref:
        return os.path.join(folder, file_ref['path'])
    else:
        return folder


def __parent_group(project, file_ref):
    for group in project.objects.get_objects_in_section('PBXGroup'):
        if group.has_child(file_ref.get_id()):
            return group
