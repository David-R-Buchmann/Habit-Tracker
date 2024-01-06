from flask import Flask, render_template, request, redirect, url_for

tasks = [{"task": "Insert your first task here", "done": False}]
