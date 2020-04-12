#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Настраивает postfix, работающий в режиме smarthost
Проводит соответствие пользователей групп ldap-каталога учетным записям smtp-сервера
"""

import configparser
import json
from ad import ad
from postfix import postfix
from config import config

if __name__ == '__main__':
	""" получение параметров конфигурации из файла конфигурации """
	conf = config()
	''' сервер ldap-каталога Active Directory '''
	ad_server = conf.get_ldap_host()
	''' пользователь для подключения к ldap-каталогу '''
	ad_user = conf.get_ldap_user()
	''' пароль пользователя для подключения к ldap-каталогу '''
	ad_password = conf.get_ldap_password()
	''' дерево поиска ldap '''
	ad_search_tree = conf.get_ldap_search_tree()
	''' группы ldap-каталога, имеющие доступ к отправке smtp '''
	ad_smtp_groups = json.loads(conf.get_smtp_ldap_groups())
	''' путь к файлу generic '''
	out_generic = conf.get_generic_path()
	''' путь к файлу relayhost_map '''
	out_relayhost = conf.get_relayhost_path()
	''' путь к файлу saslpass '''
	out_saslpass = conf.get_saslpass_path()

	''' инициализация классов для работы с LDAP и Postfix '''
	ldap = ad(ad_server, ad_user, ad_password)
	smtp = postfix(out_generic, out_relayhost, out_saslpass)

	"""
	обработка групп конфигуграций smtp
	"""
	for item in ad_smtp_groups:
		section = ad_smtp_groups[item]
		''' получение группы пользователей ldap из файла конфигурации '''
		ad_group = conf.get_ldap_group(section)
		''' получение smtp-имени пользователя из файла конфигурации '''
		smtp_user = conf.get_smtp_user(section)
		''' получение smtp-пароля пользователя из файла конфигурации '''
		smtp_password = conf.get_smtp_password(section)
		''' получение адреса smtp-сервера из файла конфигурации '''
		smtp_server = conf.get_smtp_server(section)
		''' получение порта smtp-сервера из файла конфигурации '''
		smtp_port = conf.get_smtp_port(section)
		''' запрос пользователей в группе ldap-каталога '''
		ad_users = ldap.get_group_memberships(ad_search_tree, ad_group)

		"""
		формирование данных конфигурации для каждого члена выбранных ldap-групп
		"""
		for entry in ad_users:
			''' подготовка json-данных generic '''
			generic = smtp.make_generic_data(ad_users[entry], smtp_user)
			''' подготовка json-данных relayhost '''
			relayhost = smtp.make_relayhost_data(ad_users[entry], smtp_server, smtp_port)
			''' подготовка json-данных saslpass '''
			saslpass = smtp.make_saslpass_data(ad_users[entry], smtp_user, smtp_password)

	"""
	герерация файлов конфигурации postfix
	Генерируются файлы конфигурации generic, relayhost, saslpass
	"""
	smtp.make_config_file(out_generic, generic)
	smtp.make_config_file(out_relayhost, relayhost)
	smtp.make_config_file(out_saslpass, saslpass)

	"""
	применение изменений конфигурации postfix
	генерация hash-таблиц сгенерированных файлов конфигурации
	добавление/обновление соответствующих директив в глобальный файл конфигурации
	перезапуск демона
	"""
	smtp.make_generic_hash()
	smtp.make_relayhost_hash()
	smtp.make_saslpass_hash()
	smtp.set_smtp_generic_maps()
	smtp.set_sender_dependent_relayhost_maps()
	smtp.set_smtp_sasl_password_maps()
	smtp.reload()