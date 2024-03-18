#import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from datamodels.database import db 
from flask import Flask, render_template, request, redirect, url_for




