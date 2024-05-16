from flask import Flask, render_template, redirect, url_for, request
import requests
import json


class RestSign:
    @staticmethod
    def after_login(token):
        link = request.args.get('link')
        if link is None or 0:
            return redirect(url_for('vehicle'))
        elif link == '1':
            return redirect(url_for('alarm'))
        elif link == '2':
            return redirect(url_for('new_mission'))
        elif link == '3':
            return redirect(url_for('s', token))
        else:
            return "LNG" + link




