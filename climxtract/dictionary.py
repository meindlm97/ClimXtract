# dictionary.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Meindl, University of Vienna
"""

# Dictionary for datasets, variables and units
dictionary = {
    'tas': {
        'oeks15': {'name': 'temperature', 'units': ['Celsius']},
        'spartacus': {'name': 'temperature', 'units': ['Celsius']},
        'eurocordex': {'name': 'tas', 'units': ['Kelvin']},
        'eobs': {'name': 'tg', 'units': ['Celsius']},
        'destine': {'name': '167', 'units': ['Kelvin']},
        'era5': {'name': '2m_temperature', 'units': ['Kelvin']},
        'ch2025': {'name': 'air_temperature', 'units': ['degrees_C']},
    },
    'pr': {
        'oeks15': {'name': 'precipitation', 'units': ['kg m-2']},
        'spartacus': {'name': 'RR', 'units': ['kg m-2']},
        'eurocordex': {'name': 'pr', 'units': ['kg m-2 s-1']},
        'eobs': {'name': 'rr', 'units': ['mm/day', 'mm d-1']},
        'destine': {'name': '260048', 'units': ['kg m-2 s-1']},
        'era5': {'name': 'total_precipitation', 'units': ['m']},
        'ch2025': {'name': 'precipitation_sum', 'units': ['mm day-1']}
    }
}