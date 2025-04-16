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
  614661503,
  'Simple Model',
  fields=[
    {'name': 'Slug'},
    {'name': 'Square'},
    {'name': 'Piece'},
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Board'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}} {{Square}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}} <div id="answer">{{Board}}</div>',
    },
  ]
)

class ChessNote(genanki.Note):
  @property
  def guid(self):
    # slug-square-piece
    return genanki.guid_for(self.fields[0], self.fields[1], self.fields[2])

board = chess.BaseBoard()
board.clear_board()

notes = []
for sq_name in chess.SQUARE_NAMES:
    # square colors
    sq_id = chess.parse_square(sq_name)
    sq_file = chess.square_file(sq_id)
    sq_rank = chess.square_rank(sq_id)
    sq_color = 'black' if (sq_file+sq_rank) % 2 == 0 else 'white'
    board_svg = chess.svg.board(
            board, 
            squares=chess.SquareSet([sq_id]),
            )
    note = ChessNote(
      model=model,
      fields=[
          'color',
          sq_name,
          '',
          'What is the color of square',
          sq_color,
          board_svg,
      ],
    )
    notes.append(note)

# randomize the order of the notes
random.shuffle(notes)
for note in notes:
  deck.add_note(note)

genanki.Package(deck).write_to_file('chess.apkg')
print('Deck generated: chess.apkg')
