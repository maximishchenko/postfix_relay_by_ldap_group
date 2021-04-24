#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import json

class config(object):
	""" Возвращает параметры конфигурации """
	def __init__(self, configfile = "config/config.ini"):
		super(config, self).__init__()
		self.config = configparser.ConfigParser()
		self.config.read(configfile)

	def get_ldap_host(self):
		""" возвращает хост для подключения к ldap """
		return self.config.get("AD", "host")

	def get_ldap_user(self):
		""" возвращает имя пользователя для подключения к ldap-каталогу """
		return self.config.get("AD", "bind_user")

	def get_ldap_password(self):
		""" возвращает пароль пользователя для подключения к ldap-каталогу """
		return self.config.get("AD", "bind_password")

	def get_ldap_search_tree(self):
		""" возвращает директорию поиска ldap-каталога """
		return self.config.get("AD", "search_tree")

	def get_generic_path(self):
		""" возвращает путь для файла generic """
		return self.config.get("OUT", "generic")

	def get_relayhost_path(self):
		""" возвращает путь для файла relayhost """
		return self.config.get("OUT", "relayhost")

	def get_saslpass_path(self):
		""" возвращает путь для файла saslpass """
		return self.config.get("OUT", "saslpass")

	def get_smtp_ldap_groups(self):
		"""
		возвращает список секций файла конфигурации,
		содержащих настройки требуемых ldap-групп
		"""
		groups = {}
		group_key = 0
		for section in self.config.sections():
			if self.config.has_option(section, 'ldap_group'):
				group_key = group_key + 1
				groups.update({group_key:section})
		return json.dumps(groups)

	def get_ldap_group(self, section):
		""" возвращает имя ldap-группы по имени секции файла конфигурации """
		return self.config.get(section, 'ldap_group')

	def get_smtp_user(self, section):
		""" возвращает имя smtp-пользователя по имени секции файла конфигурации """
		return self.config.get(section, 'smtp_user')

	def get_smtp_password(self, section):
		""" возвращает пароль smtp-пользователя по имени секции файла конфигурации """
		return self.config.get(section, 'smtp_password')

	def get_smtp_server(self, section):
		""" возвращает адрес smtp-сервера по имени секции файла конфигурации """
		return self.config.get(section, 'smtp_server')

	def get_smtp_port(self, section):
		"""
		возвращает порт подключения к smtp-серверу
		по имени секции файла конфигурации
		"""
		return self.config.get(section, 'smtp_port')