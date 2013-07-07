#!/usr/bin/python
# -*- coding: utf-8 -*-


def write_event(event):
	'''Writes an event to stdout'''
	if event.is_finished():
		s = u"{:<10}{:<20}{:<5}{:<20}{:<5}".format(
				event.start_date.strftime("%d/%m"), 
				event.home_team.name, 
				event.home_team_score, 
				event.visiting_team.name,
				event.visiting_team_score)
	else:
		s = u"{:<10}{:<20}{:<20}".format(event.start_date.strftime("%d/%m"), 
			event.home_team.name, event.visiting_team.name)

	print s


def write_events(events):
	'''Writes a list of events to stdout'''
	for event in events:
		write_event(event)


def write_tables(standing_groups, 
				cols=('gp', 'w', 'd', 'l','gf','ga','gd','pts')):
	'''Writes standings for groups'''
	for group in standing_groups:
		for team_stats in group.standings:
			s = u"{:<25}".format(team_stats.team.name)
			for col in cols:
				val = getattr(team_stats.stats, col, None)
				if val:
					s += u"{:>5}".format(str(val))
			print s
		print
