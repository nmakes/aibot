"""
NAME: Naveen Venkat
ID: 2015A7PS0078P
"""

from graphics import *
from modules import *
import config

# ==================================
# MAIN FUNCTION : DRIVER STARTS HERE
# ==================================

def main():

	inp = 0

	while(inp!=5):

			if config.gui:
				gui_menu()
			else:
				menu()

			inp = int(raw_input("Enter an option: "))
			
			if (inp==1):
				if config.gui:
					gui_print_board()
				else:
					print
					print_board(TreeNode.initial_state(16))
				
			elif (inp==2):
				if config.gui:
					config.R4 = time()
					play_gui_minimax_game()
					print "Game is running ..."
				else:
					play_console_minimax_game()

			elif (inp==3):
				if config.gui:
					config.R8 = time()
					play_gui_alphabeta_game()
					config.R8 = time() - config.R8
					print "Game is running ..."
				else:
					play_console_alphabeta_game()

			elif (inp==4):
				if config.gui:
					gui_publish_stats()
				else:
					publish_minimax_stats()
					publish_alphabeta_stats()
					publish_comparative_stats()
					print
					raw_input("press enter to continue ...")

			elif (inp==5):
				break

			else:
				print "Wrong option. Try again"

main()