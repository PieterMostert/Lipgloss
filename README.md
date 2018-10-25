# Lipgloss
Python app for creating glaze recipes.

See README.pdf in README LaTeX files for more info.

NB: This is a Python 3 application and does not work with Python 2. 

## Getting started on a Mac

Using [homebrew](http://docs.brew.sh/Installation.html) will make your life much, much easier.

* Install git if you haven't already `brew install git`
* Clone the repo `git clone https://github.com/PieterMostert/Lipgloss.git`
* Install [python 3](https://www.python.org/downloads/) `brew install python3`
* Install [the linear programming API PuLP](https://github.com/coin-or/pulp) `pip3 install pulp`
* Comment out `solver = GLPK(msg=0)` and uncomment `solver = PULP_CBC_CMD()` in model\lipgloss\lp_recipe_problem.py. 
* Running the main.py script opens the graphical user interface. 

Note, you can use the GLPK solver to speed things up, but it's a NIGHTMARE to install, so don't bother unless you're super keen.
* Install [GLPK](https://www.gnu.org/software/glpk/) library `brew install homebrew/science/glpk`
* Install the python bindings for GLPK. Somehow. Good luck!
