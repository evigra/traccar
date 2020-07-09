# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Traccar',
    'price' : '95.0',
    'currency' : 'EUR',
    'images': ['static/description/map_online.png'],    
    'author': "SolesGPS :: Eduardo Vizcaino",
    'category': 'fleet, GPS, Geolocation',
    'website' : 'https://solesgps.com',
    'summary' : 'Locate the satellite coordinates that your GPS devices throw. Save that information here and see it on the map.',
    'description' : """
Vehicle, leasing, insurances, cost
==================================
With this module, Odoo helps you managing all your vehicles, the
contracts associated to those vehicle as well as services, fuel log
entries, costs and many other features necessary to the management 
of your fleet of vehicle(s)

Main Features
-------------
* Add vehicles to your fleet
* Manage contracts for vehicles
* Reminder when a contract reach its expiration date
* Add services, fuel log entry, odometer values for all vehicles
* Show all costs associated to a vehicle or to a type of service
* Analysis graph for costs
""",
    'depends': [
        'gpsmap',
    ],
    'data': [
#        'security/solesgpsmap_security.xml',
#        'security/ir.model.access.csv',
#        'views/solesgpsmap_menuitem.xml',
#        'views/solesgpsmap_views.xml',
    ],

#    'demo': ['data/solesgpsmap_demo.xml'],
#    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}
