from setuptools import setup, find_packages

setup (
  name='pygments_ayed2',
  packages=find_packages(),
  version='0.0.1',
  entry_points =
  """
  [pygments.lexers]
  ayed2lexer = pygments_ayed2.lexer:Ayed2Lexer
  [pygments.styles]
  ayed2style = pygments_ayed2.style:Ayed2Style
  """,
)
