import os
import argparse
# import pprint

from utils_hj3415.helpers import SettingsManager


def unittest_setUp_test_server_setting() -> dict:
    """
    unittest의 setUp 함수에서 db 주소를 임시로 테스트 서버로 변경하는 함수
    :return: original sever setting dictionary
    """
    test_server_addr = {
        'mongo': "mongodb+srv://Cluster13994:Rnt3Q1hrZnFT@cluster13994.vhtfyhr.mongodb.net/",
        'redis': "localhost",
    }
    setting_manager = DbSettingsManager()
    original_settings_dict = setting_manager.load_settings()
    # print("<< original settings >>")
    # pprint.pprint(original_settings_dict)

    # print("<< change to temporary settings >>")
    for db_type, address in test_server_addr.items():
        setting_manager.set_address(db_type, address, verbose=False)
    # pprint.pprint(test_server_addr)

    return original_settings_dict

def unittest_tearDown_test_server_setting(original_settings_dict: dict):
    """
    unittest의 tearDown 함수에서 임시로 변경된 db 주소를 다시 원래로 돌리는 함수
    :return:
    """
    # print("<< change to original settings >>")
    setting_manager = DbSettingsManager()
    for k, v in original_settings_dict.items():
        setting_manager.set_address(k, v, verbose=False)
    # pprint.pprint(setting_manager.load_settings())


class DbSettingsManager(SettingsManager):
    DEFAULT_SETTING = {
        'mongo': 'mongodb://hj3415:piyrw421@localhost:27017',
        'redis': 'localhost',
    }
    DB_TYPE = DEFAULT_SETTING.keys()

    def __init__(self):
        settings_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json')
        super().__init__(settings_file)

    def set_address(self, db_type: str, address: str, verbose = True):
        assert db_type in self.DB_TYPE, f"db_type 인자는 {self.DB_TYPE} 중에 있어야 합니다."
        self.settings_dict[db_type] = address
        self.save_settings()
        if db_type == 'mongo':
            from db_hj3415 import mymongo
            mymongo.Base.mongo_client = mymongo.connect_to_mongo(address)
        elif db_type == 'redis':
            from db_hj3415 import myredis
            myredis.Base.redis_client = myredis.connect_to_redis(address)

        if verbose:
            print(f"{db_type} 주소가 저장되었으며 데이터베이스의 연결 주소도 변경되었습니다.: {address}")

    def get_address(self, db_type: str) -> str:
        assert db_type in self.DB_TYPE, f"db_type 인자는 {self.DB_TYPE} 중에 있어야 합니다."
        return self.settings_dict.get(db_type, self.DEFAULT_SETTING[db_type])

    def reset_address(self, db_type: str, verbose = True):
        assert db_type in self.DB_TYPE, f"db_type 인자는 {self.DB_TYPE} 중에 있어야 합니다."
        self.set_address(db_type, self.DEFAULT_SETTING[db_type], verbose=False)
        if verbose:
            print(f"{db_type} 주소가 기본값 ({self.DEFAULT_SETTING[db_type]}) 으로 초기화 되었습니다.")


def db_manager():
    settings_manager = DbSettingsManager()

    parser = argparse.ArgumentParser(description="데이터베이스 주소 관리 프로그램")
    subparsers = parser.add_subparsers(dest='db_type', help='데이터베이스 종류를 지정하세요(mongo, redis)')

    for db in ['mongo', 'redis']:
        db_parser = subparsers.add_parser(db, help=f"{db} 주소를 관리합니다.")
        db_subparsers = db_parser.add_subparsers(dest='command', help='명령을 선택하세요.')

        # save 명령어
        save_parser = db_subparsers.add_parser('save', help=f"{db} 주소를 저장합니다.")
        save_parser.add_argument('address', type=str, help=f"저장할 {db} 주소를 입력하세요.")

        # print 명령어
        db_subparsers.add_parser('print', help=f"{db} 주소를 출력합니다.")

        # reset 명령어
        db_subparsers.add_parser('reset', help=f"{db} 주소를 기본값으로 초기화합니다.")

    args = parser.parse_args()

    if args.db_type:
        if args.command == 'save':
            settings_manager.set_address(args.db_type, args.address)
        elif args.command == 'print':
            address = settings_manager.get_address(args.db_type)
            print(f"{args.db_type} 주소: {address}")
        elif args.command == 'reset':
            settings_manager.reset_address(args.db_type)
        else:
            parser.print_help()
    else:
        parser.print_help()
