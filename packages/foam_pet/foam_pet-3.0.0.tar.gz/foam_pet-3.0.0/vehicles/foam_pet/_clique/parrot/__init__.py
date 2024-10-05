

import click

def parrot ():
	@click.group ("parrot")
	def group ():
		pass

	
	@group.command ("check")
	@click.option ('--path', required = True)
	def search (path):
		print ("not built.")
	
		return;
		
	@group.command ("equalize")
	@click.option ('--path', required = True)
	def search (path):
		print ("not built.")
	
		return;

	return group




#



