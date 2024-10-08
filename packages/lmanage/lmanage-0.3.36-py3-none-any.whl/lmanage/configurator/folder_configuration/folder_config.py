from os import name
from lmanage.utils import logger_creation as log_color

# logger = log_color.init_logger(__name__, logger_level)


class FolderConfig():
    ''' Class to read in folder metadata and unested_folder_data '''

    def __init__(self, folders):
        self.folder_metadata = folders

    def unnest_folder_data(self):
        response = []

        for d in self.folder_metadata:
            folder_dict = d
            metadata_list = []
            metadata_list = self.walk_folder_structure(
                dict_obj=folder_dict,
                data_storage=metadata_list,
                parent_id='1')

            response.append(metadata_list)

        logger.info('retrieved yaml folder files')
        logger.debug('folder metadata = %s', response)

        return response

    def walk_folder_structure(self, dict_obj: dict, data_storage: list, parent_id: str):
        temp = {}
        temp['name'] = dict_obj.get('name')
        temp['legacy_id'] = dict_obj.get('id')
        temp['team_edit'] = dict_obj.get('team_edit')
        temp['team_view'] = dict_obj.get('team_view')
        temp['parent_id'] = parent_id
        logger.debug('data_structure to be appended = %s', temp)
        data_storage.append(temp)

        if isinstance(dict_obj.get('subfolder'), list):
            for subfolder in dict_obj.get('subfolder'):
                self.walk_folder_structure(subfolder, data_storage,
                                           parent_id=dict_obj.get('name'))

        return data_storage
