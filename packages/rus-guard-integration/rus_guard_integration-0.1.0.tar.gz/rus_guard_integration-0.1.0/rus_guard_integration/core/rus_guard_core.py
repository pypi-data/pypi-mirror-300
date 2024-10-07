from typing import List

from loguru import logger

from rus_guard_integration.core.base_core import BaseRusGuardCore
from rus_guard_integration.dto.model_dto import RusGuardEmployeeDto, AcsAccessLevelDto


class RusGuardCore(BaseRusGuardCore):

    async def get_all_positions(self):
        """
        Получить список должностей

        :return: zeep.objects.LEmployeePositionsData
        return example:
                        {
                    'Count': 9,
                    'UserPositions': {
                        'LEmployeePositionInfo': [
                            {
                                'Code': None,
                                'Comment': None,
                                'ID': 'dff77863-d98f-4117-9abc-25c3b9182b20',
                                'IsRemoved': False,
                                'Name': 'test_position_9'
                            },
                            {
                                'Code': None,
                                'Comment': None,
                                'ID': '64357f0b-575a-4285-b2e3-f9ecb3921450',
                                'IsRemoved': False,
                                'Name': 'test_position'
                                    }
                                ]
                            }
                        }

        """
        return await self._read_all('GetEmployeePositions')

    async def get_one_position(self, position_id: str):
        """
        Получить должность по ее uuid

        :param position_id: str, uuid должности
        :return: LEmployeePositionInfo
        return example:
        {
            'Code': None,
            'Comment': None,
            'ID': '60c2ccaf-f574-48a1-8af5-9c7d7b8a4cf4',
            'IsRemoved': False,
            'Name': 'test_position_7'
        }
        """

        return await self._read('GetEmployeePosition', position_id)

    async def create_position(self, position_name: str, comment: str = '', _code: str = ''):
        """
        Создать новую должность

        :param position_name: Наименование должности
        :param comment: Комментарий
        :param _code: ???
        :return: LEmployeePositionInfo

        return example:
        {
            'Code': None,
            'Comment': None,
            'ID': '60c2ccaf-f574-48a1-8af5-9c7d7b8a4cf4',
            'IsRemoved': False,
            'Name': 'test_position_7'
        }
        """
        return await self._create_or_update_or_delete('AddEmployeePosition',
                                                      position_name, comment, _code)

    async def update_position(self, position_id: str, position_name: str, comment: str = '', _code: str = '') -> None:

        """
        Изменить должность

        :param position_id: str, uuid должности
        :param position_name: Наименование должности
        :param comment: Комментарий
        :param _code: ???
        :return: None
        """
        return await self._create_or_update_or_delete('SaveEmployeePosition',
                                                      position_id, position_name, comment, _code)

    async def delete_position(self, position_id: str) -> None:
        """
        Удалить должность

        :param position_id: str, uuid должности
        :param position_id:
        :return: None
        """
        return await self._create_or_update_or_delete('RemoveEmployeePosition', position_id)

    async def get_employee_groups(self):
        """
        Получить список групп

        :return: List[AcsEmployeeGroup]
        return example:
        [{
            'Comment': None,
            'CreationDateTime': datetime.datetime(2024, 6, 14, 15, 27, 37),
            'EmployeeGroups': None,
            'FavoriteName': None,
            'FavoritePath': None,
            'GroupCode': None,
            'GroupType': 'GuestGroup',
            'ID': 'caa413cc-7d6d-4990-8fd9-124612bd6a37',
            'IsGuestGroup': True,
            'IsRemoved': False,
            'ModificationDateTime': datetime.datetime(2024, 6, 14, 15, 27, 37),
            'Name': 'test_group_15'
        }]
        """
        return await self._read_all('GetAcsEmployeeGroups')

    async def get_employee_group(self, group_id: str):
        """
        Получить группу по ее uuid
        :param group_id: str uuid группы
        :return: AcsEmployeeGroup

        return example:
        {
        'Comment': 'test_comment',
        'CreationDateTime': datetime.datetime(2024, 6, 14, 13, 37, 51),
        'EmployeeGroups': None,
        'FavoriteName': None,
        'FavoritePath': None,
        'GroupCode': 'Test',
        'GroupType': 'GuestGroup',
        'ID': 'b63b065a-4970-4804-b362-f0a209d360ea',
        'IsGuestGroup': True,
        'IsRemoved': False,
        'ModificationDateTime': datetime.datetime(2024, 6, 14, 13, 37, 51),
        'Name': 'test_employee_group_3'
        }

        """
        return await self._read('GetAcsEmployeeGroup', group_id)

    async def create_employee_group(self, name: str, guid: str = None, comment: str = '',
                                    is_guest_group: bool = True, group_code: str = ''):
        """
        Создать группу сотрудников
        :param name: Наименование группы
        :param guid:
        :param comment: Комментарий
        :param is_guest_group:
        :param group_code:
        :return: AcsEmployeeGroup
        return example:
        {
        'Comment': 'test_comment',
        'CreationDateTime': datetime.datetime(2024, 6, 14, 13, 37, 51),
        'EmployeeGroups': None,
        'FavoriteName': None,
        'FavoritePath': None,
        'GroupCode': 'Test',
        'GroupType': 'GuestGroup',
        'ID': 'b63b065a-4970-4804-b362-f0a209d360ea',
        'IsGuestGroup': True,
        'IsRemoved': False,
        'ModificationDateTime': datetime.datetime(2024, 6, 14, 13, 37, 51),
        'Name': 'test_employee_group_3'
        }
        """
        return await self._create_or_update_or_delete('AddAcsEmployeeGroup',
                                                      guid, name, comment, None, is_guest_group, group_code)

    async def update_employee_group(self, group_id, name: str, guid_list: List[str] = None, comment: str = '',
                                    is_guest_group: bool = True, group_code: str = '') -> None:
        """
        Обновить группу сорудников

        :param group_id:
        :param name:
        :param guid:
        :param comment:
        :param is_guest_group:
        :param group_code:
        :return:
        """
        return await self._create_or_update_or_delete('SaveAcsEmployeeGroup',
                                                      group_id, name,guid_list,comment, is_guest_group, group_code)

    async def delete_employee_group(self, group_id) -> None:
        return await self._create_or_update_or_delete('RemoveAcsEmployeeGroup', group_id)

    async def get_employee(self, employee_id: str):
        """

        :param employee_id: uuid сотрудника
        :return: AcsEmployeeFull
        return example:

        {
            'Comment': 'some comment',
            'FirstName': 'Иван',
            'IsLocked': False,
            'LastName': 'SomeLastName',
            'Number': None,
            'SecondName': None,
            'Authority': None,
            'DateOfIssue': None,
            'PINCode': None,
            'PINCodeDescription': None,
            'PINCodeUnderPressure': None,
            'PINCodeUnderPressureDescription': None,
            'PassportIssue': None,
            'PassportNumber': None,
            'RegistrationAddress': None,
            'ResidentialAddress': None,
            'CreationDateTime': datetime.datetime(2024, 6, 17, 16, 18, 1),
            'EmployeeGroupID': '37c5fd7b-0deb-4fe3-bdeb-a36c3e331013',
            'EmployeeGroupPath': None,
            'ID': 'dd594cce-f335-45dc-b272-732c724a09f8',
            'IsRemoved': False,
            'ModificationDateTime': datetime.datetime(2024, 6, 17, 16, 18, 1),
            'Position': {
                'Code': None,
                'Comment': None,
                'ID': None,
                'IsRemoved': None,
                'Name': None
            }
        }
        """
        return await self._read('GetAcsEmployee', employee_id)

    async def get_employees(self):
        """


        :return: EmployeesInfoData2
        return example:
        {
    'Count': -1,
    'Employees': {
        'AcsEmployeeInfo': [
            {
                'Comment': None,
                'FirstName': None,
                'IsLocked': False,
                'LastName': 'SomeLastName',
                'Number': None,
                'SecondName': None,
                'GroupCode': None,
                'GroupID': '177e8407-c440-4393-9ef8-1b91e9e2f834',
                'GroupName': 'some_test_group',
                'GroupPath': '/some_test_group',
                'ID': '88c733c4-1733-4090-b501-358191dfd1d4',
                'PositionCode': None,
                'PositionName': None,
                'SecurityGroupID': '00000000-0000-0000-0000-000000000000',
                'SecurityGroupName': None
            },{
                'Comment': 'some comment',
                'FirstName': 'TTTTT',
                'IsLocked': False,
                'LastName': 'Test_63',
                'Number': None,
                'SecondName': None,
                'GroupCode': None,
                'GroupID': '37c5fd7b-0deb-4fe3-bdeb-a36c3e331013',
                'GroupName': 'test_group_15',
                'GroupPath': '/test_group_15',
                'ID': '60f2bfed-1eb8-46aa-8523-f4265036e947',
                'PositionCode': None,
                'PositionName': None,
                'SecurityGroupID': '00000000-0000-0000-0000-000000000000',
                'SecurityGroupName': None
                    }
                ]
            },
            'PageNumber': 0
        }
        """
        return await self._read_all('GetAcsEmployees')

    async def get_employee_in_group(self, group_id: str):
        """

        :param group_id:
        :return example:
        [{
    'Comment': 'some comment',
    'FirstName': 'TTTTT',
    'IsLocked': False,
    'LastName': 'Test_70',
    'Number': None,
    'SecondName': None,
    'AccessLevels': None,
    'CreationDateTime': datetime.datetime(2024, 6, 19, 17, 26, 31),
    'EmployeeGroupID': '37c5fd7b-0deb-4fe3-bdeb-a36c3e331013',
    'EmployeeGroupPath': None,
    'GroupCode': None,
    'ID': 'eda54725-115f-44ee-9a16-050b82e6bbff',
    'IsAccessLevelsInherited': True,
    'IsPhotoAny': False,
    'IsRemoved': False,
    'IsWorkSchedulesInherited': True,
    'IsWorkZonesInherited': True,
    'Keys': None,
    'ModificationDateTime': datetime.datetime(2024, 6, 19, 17, 27, 38),
    'Position': {
        'Code': None,
        'Comment': None,
        'ID': None,
        'IsRemoved': None,
        'Name': None
    },
    'RowNumber': None,
    'WorkSchedules': None,
    'WorkZones': None
}]
        """
        return await self._read('GetAcsEmployeesByGroup', group_id)

    async def create_employee(self, dto: RusGuardEmployeeDto.Create):
        """

        :param dto:
        :return: AcsEmployeeSlim
        return example:
        {
    'Comment': None,
    'FirstName': None,
    'IsLocked': False,
    'LastName': 'test_last_name',
    'Number': None,
    'SecondName': None,
    'AccessLevels': None,
    'CreationDateTime': datetime.datetime(2024, 9, 26, 10, 59, 19),
    'EmployeeGroupID': 'f750f3ac-fa2d-4408-aff9-68f037ac3357',
    'EmployeeGroupPath': None,
    'GroupCode': None,
    'ID': '575b1984-a3cf-4506-abd6-1143d2ac15b2',
    'IsAccessLevelsInherited': False,
    'IsPhotoAny': False,
    'IsRemoved': False,
    'IsWorkSchedulesInherited': False,
    'IsWorkZonesInherited': False,
    'Keys': None,
    'ModificationDateTime': datetime.datetime(2024, 9, 26, 10, 59, 19),
    'Position': {
        'Code': None,
        'Comment': None,
        'ID': None,
        'IsRemoved': None,
        'Name': None
    },
    'RowNumber': None,
    'WorkSchedules': None,
    'WorkZones': None
}
        """
        return await self._create_or_update_or_delete('AddAcsEmployee',
                                                      dto.rus_guard_group_guid,
                                                      dto.model_dump(exclude={'rus_guard_group_guid'},
                                                               exclude_none=True))

    async def update_employee(self, employee_id: str, dto: RusGuardEmployeeDto.Create) -> None:
        return await self._create_or_update_or_delete('SaveAcsEmployee',
                                                      employee_id, dto.model_dump(exclude_none=True))

    async def delete_employee(self, employee_id: str):
        employee_cards = await self._read('GetAcsKeysForEmployee', employee_id)
        if employee_cards:
            for card in employee_cards:
                await self._create_or_update_or_delete('RemoveAcsKey', card.CardTypeID)
        await self._create_or_update_or_delete('RemoveAcsEmployee', employee_id)

    async def get_card_type(self, card_type_id: str):
        return await self._read('GetCardType', card_type_id)

    async def get_all_card_types(self):
        return await self._read_all('GetCardTypes')

    async def create_card_type(self, name: str, comment: str = ''):
        all_card_type = await self.get_all_card_types()
        logger.info(all_card_type)
        for card_type in all_card_type.CardTypes.CardTypeInfo:
            if card_type.Name == name:
                return card_type.ID
        return await self._create_or_update_or_delete('AddCardType', name, comment)

    async def update_card_type(self, card_type_id: str, name: str | None = None, comment: str | None = None):
        return await self._create_or_update_or_delete('SaveCardType', card_type_id, name, comment)

    async def delete_card_type(self, card_type_id: str):
        return await self._create_or_update_or_delete('RemoveCardType', card_type_id)

    async def set_rfid(self, employee_id: str, card_type_id: str):
        result = await self._create_or_update_or_delete('ForceAssignAcsKeyForEmployee', employee_id, None,
                                                        {'CardTypeID': f'{card_type_id}'})
        self.service_config.ReindexKeys(employee_id)
        return result

    async def get_access_levels(self):
        return await self._read_all('GetAcsAccessLevelsSlimInfo')

    async def create_access_level(self, dto: AcsAccessLevelDto.Create):
        """

        :param dto:
        :return: AcsAccessLevelSlimInfo
        return example:
        {
    'Name': 'test_3',
    'Description': 'test_description',
    'EndDate': None,
    'Folder': {
        'Description': None,
        'Left': None,
        'Name': None,
        'Owner': None,
        'ParentID': None,
        'ID': None,
        'Level': None,
        'Right': None
    },
    'Id': '5caf3a86-f9f2-4eb2-8b43-8fe4c4b40d1b',
    'IsFolder': False,
    'IsRemoved': False,
    'NumberOfAccessPoints': 0,
    'ReadRightDisabled': None
}
        """
        return await self._create_or_update_or_delete('AddAcsAccessLevel', dto.model_dump(exclude_none=True))

    async def update_access_level(self, access_level_id: str, new_name:str, description:str=None)->None:
        return await self._create_or_update_or_delete('SaveAcsAccessLevel', access_level_id,  {"Name": new_name, "Description": description})

    async def delete_access_level(self, access_level_id: str):
        return await self._create_or_update_or_delete('RemoveAcsAccessLevel', access_level_id)
















    # async def block_pass(self, employee_id: [str]):
    #     '''Dont work'''
    #     return await self._create_or_update_or_delete('LockAcsEmployee', employee_id, None)
    #
    # async def add_vehicle(self):
    #     return await self._create_or_update_or_delete('AddEmployee2VehicleChain', )
    #
    # async def update_vehicle(self):
    #     return await self._create_or_update_or_delete('SaveAcsVehicle', )
    #
    # async def delete_vehicle(self):
    #     return await self._create_or_update_or_delete('RemoveAcsVehicle', )