import click
import subprocess

@click.command()
def start():
    """Start your vm"""
    subprocess.run("gcloud compute instances start --zone=europe-west1-d lewagon-data-eng-vm-erikrowens")

@click.command()
def stop():
    """Stop your vm"""
    subprocess.run("gcloud compute instances stop --zone=europe-west1-d lewagon-data-eng-vm-erikrowens")

@click.command()
def connect():
    """Connect to your vm in vscode inside your ~/code/erikrowens/folder """
    subprocess.run("code --folder-uri vscode-remote://ssh-remote+username@35.241.182.252/home/eo/code/erikrowens/")
