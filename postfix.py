#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from vars import *

class postfix(object):
	""" Взаиодействие с демоном postfix"""
	def __init__(self, generic_file, relayhost_file, saslpass_file):
		super(postfix, self).__init__()
		self.generic_file = generic_file
		self.relayhost_file = relayhost_file
		self.saslpass_file = saslpass_file
		self.newline = "\n"
		self.__generic_json = {}
		self.__relayhost_json = {}
		self.__saslpass_json = {}

	def make_generic_hash(self):
		"""
		генерирует hash-таблицу файла generic
		"""		
		logging.info(u'Генерация hash-таблицы generic')
		os.system('postmap ' + self.generic_file)

	def make_relayhost_hash(self):
		"""
		генерирует hash-таблицу файла relayhost_maps
		"""
		logging.info(u'Генераация hash-таблицы relayhost')
		os.system('postmap ' + self.relayhost_file)

	def make_saslpass_hash(self):
		"""
		генерирует hash-таблицу файла saslpass
		"""
		logging.info(u'Генераация hash-таблицы saslpass')
		os.system('postmap ' + self.saslpass_file)

	def set_smtp_generic_maps(self):
		"""
		добавляет/обновляет значение директивы smtp_generic_maps 
		"""
		logging.info(u'Обновление директивы smtp_generic_maps')
		os.system('postconf -e smtp_generic_maps=hash:' + self.generic_file)

	def set_sender_dependent_relayhost_maps(self):
		"""
		добавляет/обновляет значение директивы sender_dependent_relayhost_maps
		"""
		logging.info(u'Обновление директивы sender_dependent_relayhost_maps')
		os.system('postconf -e sender_dependent_relayhost_maps=hash:' + self.relayhost_file)

	def set_smtp_sasl_password_maps(self):
		"""
		добавляет/обновляет значение директивы smtp_sasl_password_maps
		"""
		logging.info(u'Обновление директивы smtp_sasl_password_maps')
		os.system('postconf -e smtp_sasl_password_maps=hash:' + self.saslpass_file)

	def make_generic_data(self, ldap_account, smtp_account):	
		"""
		формирует json-данные файла generic
		"""
		logging.info(u'Генерация json-данных generic')
		generic_data = { ldap_account : smtp_account }
		self.__generic_json.update(generic_data)
		return json.loads(json.dumps(self.__generic_json))

	def make_relayhost_data(self, ldap_account, smtp_server, smtp_port):
		"""
		формирует json-данные файла relayhost_maps
		"""
		logging.info(u'Генерация json-данных relayhost')
		relayhost_data = { ldap_account : "[" + smtp_server + "]:" + smtp_port }
		self.__relayhost_json.update(relayhost_data)
		return json.loads(json.dumps(self.__relayhost_json))

	def make_saslpass_data(self, ldap_account, smtp_account, smtp_password):
		"""
		формирует json-данные файла saslpass
		"""
		logging.info(u'Генерация json-данных saslpass')
		saslpass_data = { ldap_account : smtp_account + ":" + smtp_password }
		self.__saslpass_json.update(saslpass_data)
		return json.loads(json.dumps(self.__saslpass_json))

	def make_config_file(self, out_file, data_json):
		"""
		Создает файл конфигурации
		Используется для генерации файлов generic, relayhost, saslpass
		"""
		logging.info(u'Генерация файла ' + out_file)
		with open(out_file, 'w', newline=self.newline) as config_file:
			for account in data_json:
				accounts = account + " " + data_json[account] + "\n"
				config_file.writelines(accounts)

	def reload(self):
		"""
		перезапускает postfix daemon
		перечитывается файл конфигурации
		"""
		logging.info(u'Перезапуск демона Postfix')
		os.system('postfix reload')