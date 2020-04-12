#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from vars import *
from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL


class ad(object):
	""" Обеспечивает взаимодействие с ldap-каталогом Active Directory """
	def __init__(self, server, user, password):
		super(ad, self).__init__()
		self.__server = server
		self.__user = user
		self.__password = password
		self.__connect()
		self.__bind()

	def __connect(self):
		""" Подключение к ldap-серверу """
		server = Server(self.__server)
		try:
			self.__connection = Connection(server,user=self.__user,password=self.__password)
			logging.info(u'Подключение к контроллеру домена успешно установлено')
		except Exception as e:
			logging.error(u'Невозможно установить gодключение к контроллеру домена')
			sys.exit()
		else:
			pass
		finally:
			pass		
		return self.__connection

	def __bind(self):
		""" Подключение к каталогу """
		logging.info(u'Производится подключение к каталогу LDAP')
		return self.__connection.bind()

	def get_group_memberships(self, search_tree, group):
		""" Получение пользователей в группе """
		logging.info(u'Получение списка пользователей группы ' + group)
		users = {}
		users_key = 0
		self.__connection.search(search_tree,'(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(memberOf=%s))' % (group),
			SUBTREE,
    		attributes =['cn','mail','department','sAMAccountName','displayName','userPrincipalName']
		)
		''' TODO добавить проверку непустого результата '''
		for entry in self.__connection.entries:
			users_key = users_key + 1
			users.update({users_key:str(entry.userPrincipalName)})
		logging.info(u'Список пользователей сформирован')
		return users