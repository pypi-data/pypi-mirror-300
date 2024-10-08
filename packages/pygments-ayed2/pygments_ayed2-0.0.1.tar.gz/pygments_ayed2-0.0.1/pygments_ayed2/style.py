from pygments.style import Style
from pygments.token import Name, Punctuation, Token


class Ayed2Style(Style):
        styles = {
            Token.Keyword.Type:     'ansibrightblue',
            Token.String:           'ansibrightblue',
            Token.Number:           'ansibrightcyan',
            Token.Operator:         'ansibrightred',
            Token.Keyword:          'ansibrightgreen',
            Token.Name:             'ansiwhite',
            Token.Punctuation:      'ansicyan',
            Punctuation.Assignment: 'ansibrightyellow',
            Name.NamedLiteral:      'ansimagenta',
            Name.Builtin:           'ansibrightmagenta',
        }
