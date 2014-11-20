#! /usr/bin/python2.7

# Copyright 2014 Jtmorgan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import csv
import geo
import MySQLdb
import geo_config
import sys

def project_editors_primary_ips(cursor, query):
	"""
	Get user_id, user_name, and primary ip from recentchanges table.
	"""
	output = []
	cursor.execute(query)
	rows = cursor.fetchall()	
	for row in rows: 
		output.append([row[0], row[1], row[2], row[3]]) #generalize for any number of fields?
	return output	

def sort_top_editors_per_country(editors, editcount_index, top_n):
	"""
	Takes a list of lists of editors with editcounts
	and a top editor cutoff int, returns a sorted top list.
	"""
	editors.sort(key=lambda x: int(x[2]), reverse=True)
	if len(editors) > top_n:
		editors = editors[:top_n]
	return editors
	
def write_top_editors_to_file(countries, output_path):	
	"""
	Takes a dict of lists, returns a csv file with rows for each value.
	"""	 
	with open(output_path, 'wb') as csvout:
		csvout = csv.writer(csvout, quoting=csv.QUOTE_NONNUMERIC)
		csvout.writerow( ('user name','user id', 'recent edits', 'country code') )
		for country, editors in countries.iteritems():
			for editor in editors:
				csvout.writerow( (editor[0], editor[1], editor[2], country) ) #try?
	
if __name__ == '__main__':
	wiki = sys.argv[1] #the project you want to get data about
	top_n = int(sys.argv[2]) #the number of people per geo
	output_path = sys.argv[3] #the name of the file you want to output
# 	project_db = geo_config.s6_dbname
	countries = geo_config.countries
	conn = MySQLdb.connect(host = geo_config.s6_host, db = wiki, read_default_file = geo_config.s6_defaultcnf, use_unicode=1, charset="utf8")	
	cursor = conn.cursor()
	query = """select user_name, user_id, total_edits, primary_ip 
	  from (
		select sum(edits) as total_edits, user_id, user_name, primary_ip from (
		  select count(cuc_id) as edits, cuc_user as user_id, cuc_user_text AS user_name, cuc_ip as primary_ip 
	  from %s.cu_changes 
		where cuc_user != 0 
		and cuc_type = 0 
		  and cuc_user NOT IN (
			SELECT ug_user FROM %s.user_groups WHERE ug_group = 'bot'
			)
		 group by cuc_user, cuc_ip 
		 order by edits desc
		 ) as tmp 
	   group by user_id order by total_edits desc
		 ) as tmp2 
	   where total_edits >= 15 
	   order by total_edits desc; """ % (wiki, wiki,)
	
	editors_ips = project_editors_primary_ips(cursor, query)
	for editor in editors_ips:
		country_code = geo.geo_country([unicode(editor[3], "UTF-8")])
		if country_code[0] in countries.keys():
			countries[country_code[0]].append([editor[0], editor[1], editor[2]])
	for country, editors in countries.iteritems():	
		countries[country] = sort_top_editors_per_country(editors, 2, top_n)	#return sorted and abbreviated list	
	write_top_editors_to_file(countries, output_path)