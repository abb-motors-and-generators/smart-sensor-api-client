import pytest
import os
from unittest.mock import patch

from tests import SETTING_FILE_PATH, setup_test_environment

from use_case_1.get_detailed_sensor_and_asset_data import run_task as run_task_1_1
from use_case_1.get_plant_data import run_task as run_task_1_2
from use_case_1.get_simplified_asset_data import run_task as run_task_1_3
from use_case_2.add_notification_channel import run_task as run_task_2_1
from use_case_3.change_threshold_values_for_kpis import run_task as run_task_3_1
from use_case_4.get_condition_indexes import run_task as run_task_4_1
from use_case_5.get_historic_measurements import run_task as run_task_5_1
from use_case_5.get_latest_measurements import run_task as run_task_5_2


class TestUseCase1:
    @classmethod
    def setup_class(cls):
        setup_test_environment()

    @classmethod
    def teardown_class(cls):
        os.remove(SETTING_FILE_PATH)

    def test_get_detailed_sensor_and_asset_data(self):
        assert run_task_1_1(settings_file=SETTING_FILE_PATH) is True

    def test_get_plant_data(self):
        assert run_task_1_2(settings_file=SETTING_FILE_PATH) is True

    def test_get_simplified_asset_data(self):
        assert run_task_1_3(settings_file=SETTING_FILE_PATH) is True


class TestUseCase2:
    @classmethod
    def setup_class(cls):
        setup_test_environment()

    @classmethod
    def teardown_class(cls):
        os.remove(SETTING_FILE_PATH)

    def test_add_notification_channel(self):
        asset_list = [os.getenv("ASSET_ID_1")]
        notification_type = os.getenv("NOTIFICATION_TYPE")
        notification_channel = os.getenv("NOTIFICATION_CHANNEL")
        url = os.getenv("URL")
        assert run_task_2_1(asset_list=asset_list, notification_type=notification_type, notification_channel=notification_channel, url=url) is True


class TestUseCase3:
    @classmethod
    def setup_class(cls):
        setup_test_environment()

    @classmethod
    def teardown_class(cls):
        os.remove(SETTING_FILE_PATH)

    def test_change_threshold_values_for_kpis(self):
        value_list = os.getenv("VALUE_LIST").split(",")
        assert run_task_3_1(settings_file=SETTING_FILE_PATH, asset_id=os.getenv("ASSET_ID_1"), measurement_type=os.getenv("MEASUREMENT_TYPE_1"),value_list=value_list, debug=True) is True


class TestUseCase4:
    @classmethod
    def setup_class(cls):
        setup_test_environment()

    @classmethod
    def teardown_class(cls):
        os.remove(SETTING_FILE_PATH)

    def test_get_condition_indexes(self):
        asset_list = [os.getenv("ASSET_ID_1")]
        assert run_task_4_1(settings_file=SETTING_FILE_PATH, asset_list=asset_list) is True


class TestUseCase5:
    @classmethod
    def setup_class(cls):
        setup_test_environment()

    @classmethod
    def teardown_class(cls):
        os.remove(SETTING_FILE_PATH)

    @patch("matplotlib.pyplot.show")
    def test_get_historic_measurements(self, mock_show):
        assert run_task_5_1(settings_file=SETTING_FILE_PATH, asset_id=os.getenv("ASSET_ID_1"), measurement_type=os.getenv("MEASUREMENT_TYPE_1"), start_date=os.getenv("START_DATE"), end_date=os.getenv("END_DATE"))

    def test_get_latest_measurements(self):
        assert run_task_5_2(settings_file=SETTING_FILE_PATH) is True
