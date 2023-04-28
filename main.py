from sys import argv
import argparse

parser = argparse.ArgumentParser(
                    prog='Hunter Control Terminal',
                    description='''
                    A Terminal based program to allow multiple users and clients connect seamlessly, 
                    and have multiple independent sessions which allow the trade of commands and responses 
                    across a remote network
                    ''',
                    epilog='Text at the bottom of help')

if len(argv) <= 1:
    parser.print_help()
args = parser.parse_args()