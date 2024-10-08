


''''
foam_pet_1 parrot check_EQ \
--origin "/Metro/vehicles/foam_pet/_health/monitors/parrot/status_1/example_equality/directory_1" \
--to "/Metro/vehicles/foam_pet/_health/monitors/parrot/status_1/example_equality/directory_2"
"'''

''''
foam_pet_1 parrot check_EQ \
--origin "/Metro/vehicles/foam_pet/_health/monitors/parrot/status_1/example_inequality/directory_1" \
--to "/Metro/vehicles/foam_pet/_health/monitors/parrot/status_1/example_inequality/directory_2"
"'''

''''
foam_pet_1 parrot equalize \
--origin "/Metro/vehicles/foam_pet/_health/monitors/parrot/status_1/example_equality" \
--to "/Metro/vehicles/foam_pet/_health/monitors/parrot/status_1/example_equality_2"

foam_pet_1 parrot check_EQ \
--origin "/Metro/vehicles/foam_pet/_health/monitors/parrot/status_1/example_equality" \
--to "/Metro/vehicles/foam_pet/_health/monitors/parrot/status_1/example_equality_2"
"'''

''''
	TODO:
		foam_pet parrot equalize
		foam_pet parrot check_EQ
		
		__glossary/foam_pet_1
"'''
def check_1 ():
	return;



checks = {
	'check 1': check_1
}