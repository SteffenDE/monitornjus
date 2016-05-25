#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015 Steffen Deusch
# Licensed under the MIT license
# MonitorNjus, 28.11.2015 (Version 1.1)

import random                       # Random Modul importieren

rancolor = ['red', 'indigo', 'blue', 'light-blue', 'cyan', 'teal',
            'green', 'light-green', 'amber', 'orange', 'deep-orange', 'blue-grey']
color = random.choice(rancolor)     # Zufallsauswahl der Darbe

if color == "red":                  # Umwandlung des Farbnamens in Hexadezimal
    hexa = "#f44336"
elif color == "indigo":
    hexa = "#3f51b5"
elif color == "blue":
    hexa = "#2196f3"
elif color == "light-blue":
    hexa = "#03a9f4"
elif color == "cyan":
    hexa = "#00bcd4"
elif color == "teal":
    hexa = "#009688"
elif color == "green":
    hexa = "#4caf50"
elif color == "light-green":
    hexa = "#8bc34a"
# elif color == "lime":
# 	hexa = "#cddc39"
elif color == "amber":
    hexa = "#ffc107"
elif color == "orange":
    hexa = "#ff9800"
elif color == "deep-orange":
    hexa = "#ff5722"
# elif color == "grey":
# 	hexa = "#9e9e9e"
elif color == "blue-grey":
    hexa = "#607d8b"
else:
    hexa == "wtf"

adminstyles = """
	<style type="text/css">

		.input-field label { 
			opacity: 0; 
		}

		.secondary-content, .input-field .prefix.active, .input-field input[type=text]:focus + label, .input-field input[type=password]:focus + label, .input-field input[type=email]:focus + label, .input-field input[type=url]:focus + label, .input-field input[type=date]:focus + label, .input-field input[type=tel]:focus + label, .input-field input[type=number]:focus + label, .input-field input[type=search]:focus + label, .input-field textarea:focus.materialize-textarea + label, .dropdown-content li > a, .dropdown-content li > span { 
			color: """ + hexa + """; opacity: 1; 
		}

		.switch label input[type=checkbox]:first-child:checked + .lever { 
			background-color: """ + hexa + """; opacity: 1; 
		}

		input[type=text], input[type=number] {
			color: grey
		}

		input[type=text]:focus, input[type=password]:focus, input[type=email]:focus, input[type=url]:focus, input[type=date]:focus, input[type=tel]:focus, input[type=number]:focus, input[type=search]:focus, textarea:focus.materialize-textarea { 
			border-bottom: 1px solid """ + hexa + """;
			-webkit-box-shadow: 0 1px 0 0 """ + hexa + """;
			-moz-box-shadow: 0 1px 0 0 """ + hexa + """;
			box-shadow: 0 1px 0 0 """ + hexa + """; 
			color: black;
		}

		input[type=range]::-webkit-slider-thumb {
			background-color: """ + hexa + """;
		}

		input[type=range]::-moz-range-thumb {
			background: """ + hexa + """;
		}

		input[type=range] + .thumb {
			background-color: """ + hexa + """;
		}

		[type="checkbox"]:checked + label:before {
			border-right: 2px solid """ + hexa + """;
			border-bottom: 2px solid """ + hexa + """; 
		}

		.btn:hover, .btn-large:hover { background-color: """ + hexa + """; opacity: 1; }
		.btn, .btn-large, .btn-floating { background-color: """ + hexa + """; opacity: 0.8; }

	</style>"""
