import base64
import importlib
import re
from datetime import datetime
from io import BytesIO

import requests
from django.conf import settings

from zs_utils.api.services import ApiRequestLogService
from zs_utils.exceptions import CustomException
from zs_utils.json_utils import pretty_json


PROJECT_CONST = {
    "default": {
        "MAILGUN_SENDER_DOMAIN": "mg.zonesmart.ru",
        "EMAIL_STATIC_FOLDER_URL": "https://storage.yandexcloud.net/zs-static/email/",
    },
    "oms": {
        "MAILGUN_SENDER_DOMAIN": "mg.zonesmart.ru",
        "EMAIL_STATIC_FOLDER_URL": "https://storage.yandexcloud.net/zs-static/email/",
    },
    "repricer": {
        "MAILGUN_SENDER_DOMAIN": "repricer.zonesmart.su",
        "EMAIL_STATIC_FOLDER_URL": "https://storage.yandexcloud.net/zs-static/email/",
    },
    "landing": {
        "MAILGUN_SENDER_DOMAIN": "landing.zonesmart.su",
        "EMAIL_STATIC_FOLDER_URL": "https://storage.yandexcloud.net/zs-static/email/",
    },
}


class EmailServiceException(CustomException):
    pass


class Unisender:
    API_URL = "https://go1.unisender.ru/ru/transactional/api/v1/"
    FROM_EMAIL = "noreply@id.kokocgroup.ru"

    @classmethod
    def send_email(
            cls,
            receivers: list,
            sender: str,
            subject: str,
            message: str,
            api_key: str,
            files: dict = None,
            message_format: str = "plaintext",
            **kwargs,
    ):
        data = {
            "message": {
                "recipients": [{"email": email} for email in receivers],
                "body": {message_format: message},
                "subject": subject,
                "from_email": cls.FROM_EMAIL,
                "from_name": sender,
                "skip_unsubscribe": 1,
                "attachments": [
                    {"name": name, "content": value, "type": "application/octet-stream"}
                    for name, value in files.items()
                ]
                if files
                else None,
            }
        }

        response = requests.post(
            url=cls.API_URL + "email/send.json", headers={"X-API-KEY": api_key}, json=data,
        )
        ApiRequestLogService.save_api_request_log_by_response(response=response, save_if_is_success=False)
        if not response.ok:
            raise EmailServiceException(pretty_json(response.json()))

        return response.json()

    @classmethod
    def send_html_email(cls, **kwargs):
        return cls.send_email(message_format="html", **kwargs)


class Mailgun:
    API_URL = "https://api.mailgun.net/v3/"

    @staticmethod
    def format_date(date: datetime) -> str:
        """
        Конвертация timezone.datetime в строку формата: '%a, %d %b %Y %H:%M:%S 0000'
        """
        return date.strftime("%a, %d %b %Y %H:%M:%S 0000")

    @classmethod
    def send_email(
            cls,
            project: str,
            sender: str,
            receivers: list,
            subject: str,
            api_key: str,
            text: str = None,
            files: dict = None,
            html: str = None,
            delivery_time: datetime = None,
            tags: list = None,
            **kwargs,
    ) -> dict:
        """
        Отправка email-уведомления на пользовательские email адреса
        """

        attachments = []
        if files:
            for name, base64_file in files.items():
                attachments.append(
                    ("attachment", (name, BytesIO(initial_bytes=base64.b64decode(base64_file.encode()))))
                )

        mailgun_domain = PROJECT_CONST.get(project, PROJECT_CONST["default"])["MAILGUN_SENDER_DOMAIN"]

        data = {
            "from": sender,
            "to": receivers,
            "subject": subject,
            "text": text,
            "html": html,
            "o:tag": tags,
        }
        if delivery_time:
            data["o:deliverytime"] = cls.format_date(delivery_time)
        data = {key: value for key, value in data.items() if value}

        response = requests.post(
            url=f"{cls.API_URL}{mailgun_domain}/messages",
            auth=("api", api_key),
            data=data,
            files=attachments if attachments else None,
        )
        ApiRequestLogService.save_api_request_log_by_response(response=response, save_if_is_success=False)
        return response.json()

    @classmethod
    def send_html_email(cls, message: str, **kwargs):
        return cls.send_email(html=message, **kwargs)


class EmailService(Unisender):
    """
    Сервис для отправки писем по шаблону из mailgun
    """

    # ------------------------------ Генерация полного HTML шаблона ------------------------------
    @classmethod
    def get_template_file(cls, template_name: str):
        """
        Получение файла с частями шаблона
        """
        template_package = getattr(settings, "EMAIL_TEMPLATE_PACKAGE", "zs_utils.email.templates.kokocid")
        if not template_package:
            raise EmailServiceException("Не указан базовый пакет шаблонов в настройках")

        full_template_module = f"{template_package}.{template_name}"

        try:
            template_module = importlib.import_module(full_template_module)
        except ModuleNotFoundError:
            raise EmailServiceException(f"Шаблон {template_name} не найден")

        return template_module

    @classmethod
    def get_template_languages(cls, template_name: str) -> list:
        """
        Получение всех языков шаблона
        """
        template_file = cls.get_template_file(template_name=template_name)
        languages = list()
        for part in dir(template_file):
            if "body" in part:
                languages.append(part.split("_")[-1])
        return languages

    @classmethod
    def get_templates(cls, project: str, base_template: str, template_name: str) -> dict:
        """
        Сбор шаблонов из файла с частями
        """
        templates_dict = dict()
        languages = cls.get_template_languages(template_name=template_name)
        for language in languages:
            template_data = cls.get_template_data(project=project, template_name=template_name, language=language)
            templates_dict[f"{project}.{template_name}.{language}"] = base_template.format(**template_data)
        return templates_dict

    @classmethod
    def validate_template_params(cls, html_template: str, template_params: dict):
        """
        Валидация параметров шаблона
        """
        params = re.findall(pattern=r"{(.*?)}", string=html_template)
        required_params = [template_param.replace("{", "") for template_param in params]

        errors = dict()
        required_params = list(set(required_params))
        for required_param in required_params:
            if required_param not in template_params:
                errors[f"template_params.{required_param}"] = "Обязательное поле."
        if errors:
            raise EmailServiceException(message_dict=errors)

    @classmethod
    def get_template_data(cls, project: str, template_name: str, language: str, template_params: dict) -> dict:
        """
        Получение данных шаблона
        """
        # Базовая информация: файл шаблона с частями и url со статикой
        template_file = cls.get_template_file(template_name=template_name)
        static_url = PROJECT_CONST.get(project, PROJECT_CONST["default"])["EMAIL_STATIC_FOLDER_URL"]
        if not hasattr(template_file, f"body_{language}"):
            raise EmailServiceException(
                message_dict={"language": f"Для данного шаблона не определён язык '{language}'"}
            )

        # Костыль для шаблона zonesmart.order
        if "items" in template_params:
            items = ""
            item_template = getattr(template_file, f"items_{language}", getattr(template_file, "items", None))
            for item in template_params["items"]:
                items += item_template.format(**item)
            template_params["items"] = items

        # Переносим части шаблона в словарь
        title = getattr(template_file, f"title_{language}")
        template_data = {
            "title": title,
            "subject": getattr(template_file, f"subject_{language}", title).format(**template_params),
            "body": getattr(template_file, f"body_{language}"),
            "cheers": getattr(template_file, f"cheers_{language}", ""),
            "footer": getattr(template_file, f"footer_{language}", ""),
            "logo_url": f"{static_url}{template_file.base.logo}",
            "email_icon_url": f"{static_url}{getattr(template_file, 'icon', '')}",
        }

        # Составление полного шаблона из частей
        base_template = template_file.base.base_template
        template_data["html"] = base_template.format(**template_data)
        cls.validate_template_params(html_template=template_data["html"], template_params=template_params)
        template_data["html"] = template_data["html"].format(**template_params)
        return template_data

    # ------------------------------ Отправка email письма ------------------------------

    @classmethod
    def send_template_email(
        cls,
        project: str,
        template_name: str,
        language: str,
        sender: str,
        receivers: list,
        template_params: dict,
        api_key: str,
        files: dict = None,
        **kwargs,
    ):
        """
        Отправка email-уведомления по шаблону
        """
        language = language if language == "ru" else "en"
        template_data = cls.get_template_data(
            project=project, template_name=template_name, language=language, template_params=template_params
        )
        return cls.send_html_email(
            project=project,
            sender=sender,
            receivers=receivers,
            subject=template_data["subject"],
            message=template_data["html"],
            files=files,
            api_key=api_key,
        )
