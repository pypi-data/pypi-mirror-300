import json
import os
import logging
from logging import Logger


class SettingsManager:
    """
    세팅 파일을 저장하는 기본 클래스
    self.settings_dict 의 내용이 저장되므로 self.settings_dict 를 채운후 self.save_settings를 실행해 파일로 저장한다.
    """
    def __init__(self, settings_file: str):
        self.settings_file = settings_file
        self.settings_dict = self.load_settings()

    def load_settings(self) -> dict:
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError as e:
                print(f"설정 파일을 읽는 중 오류 발생: {e}")
                return {}
        else:
            return {}

    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as file:
                json.dump(self.settings_dict, file, indent=4)
        except IOError as e:
            print(f"설정 파일을 저장하는 중 오류 발생: {e}")


def setup_logger(logger_name: str) -> Logger:
    # 로거 생성
    logger = logging.getLogger(logger_name)

    # 이미 핸들러가 추가된 경우 새로 추가하지 않음
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # 콘솔 핸들러 설정
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 포맷터 설정
        formatter = logging.Formatter('%(module)s / %(levelname)s / func(%(funcName)s) / %(message)s')
        console_handler.setFormatter(formatter)

        # 핸들러를 로거에 추가
        logger.addHandler(console_handler)

    return logger
