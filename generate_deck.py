#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "genanki",
#     "python-chess",
# ]
# ///

import random
import genanki
import chess
import chess.svg

deck = genanki.Deck(
  2059400110,
  'Blind Chess'
)

model= genanki.Model(
  1120858226,
  'Chess Model',
  fields=[
    {'name': 'guid'},
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Board'},
  ],
  templates=[
    {
      'name': 'Base Card with SVG board in answer',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}} {{Board}}',
    },
  ]
)

class ChessNote(genanki.Note):
  @property
  def guid(self):
    # slug-square-piece
    return genanki.guid_for(self.fields[0])

def square_color(sq_name):
    sq_id = chess.parse_square(sq_name)
    sq_file = chess.square_file(sq_id)
    sq_rank = chess.square_rank(sq_id)

    guid = f'{sq_name}-color'
    question = f'What is the color of square {sq_name}?'
    answer = 'black' if (sq_file+sq_rank) % 2 == 0 else 'white'
    board_svg = chess.svg.board(None, squares=sq_id)
    return ChessNote(model, [guid, question, answer, board_svg])

def knight_moves(sq_name):
    board = chess.Board().empty()
    sq_id = chess.parse_square(sq_name)
    board.set_piece_at(sq_id, chess.Piece(chess.KNIGHT, chess.WHITE))
    attacks = board.attacks(sq_id)

    guid = f'{sq_name}-knight-moves' #guid
    question = f'Where can the knight move from square {sq_name}?'
    answer = ', '.join(chess.SQUARE_NAMES[sq] for sq in list(attacks))
    board_svg = chess.svg.board(board, fill=dict.fromkeys(attacks, "#cc0000cc"))
    # return ChessNote(model, [guid, question, answer, board_svg])
    return ChessNote(model, [guid,question,answer,board_svg])

def notes():
    # square colors
    for sq_name in chess.SQUARE_NAMES:
        yield square_color(sq_name)
        yield knight_moves(sq_name)

notes = list(notes())

# randomize the order of the notes
random.shuffle(notes)
for note in notes:
  deck.add_note(note)

genanki.Package(deck).write_to_file('chess.apkg')
print(f'Created deck chess.apkg with {len(deck.notes)} notes')
