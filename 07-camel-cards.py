import pandas as pd

hands = []
bids = []

with open('07_input') as file:
    for line in file:
        if len(line):
            hands.append(line.split()[0])
            bids.append(int(line.split()[1]))

df = pd.DataFrame({'hand': hands, 'bid': bids})

df['hand_type'] = pd.Categorical(['high_card' for _ in range(df.shape[0])],
                                 categories=['high_card', 'one_pair', 'two_pair', 'three_of_a_kind',
                                             'full_house', 'four_of_a_kind', 'five_of_a_kind'],
                                 ordered=True)

cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
cards_cat = pd.api.types.CategoricalDtype(categories=cards, ordered=True)

for card in cards:
    if 'J' == card:
        continue

    counts = df['hand'].str.count(card)

    df.loc[5 == counts, 'hand_type'] = 'five_of_a_kind'
    df.loc[4 == counts, 'hand_type'] = 'four_of_a_kind'
    df.loc[(3 == counts) & ('one_pair' == df['hand_type']), 'hand_type'] = 'full_house'
    df.loc[(3 == counts) & ('high_card' == df['hand_type']), 'hand_type'] = 'three_of_a_kind'
    df.loc[(2 == counts) & ('three_of_a_kind' == df['hand_type']), 'hand_type'] = 'full_house'
    df.loc[(2 == counts) & ('one_pair' == df['hand_type']), 'hand_type'] = 'two_pair'
    df.loc[(2 == counts) & ('high_card' == df['hand_type']), 'hand_type'] = 'one_pair'

# evaluate J separately, with an extra joker column
df['joker_type'] = df['hand_type'].copy()
counts = df['hand'].str.count('J')

df.loc[5 == counts, 'hand_type'] = 'five_of_a_kind'
df.loc[5 == counts, 'joker_type'] = 'five_of_a_kind'

df.loc[4 == counts, 'hand_type'] = 'four_of_a_kind'
df.loc[4 == counts, 'joker_type'] = 'five_of_a_kind'

df.loc[(3 == counts) & ('one_pair' == df['hand_type']), 'hand_type'] = 'full_house'
df.loc[(3 == counts) & ('one_pair' == df['joker_type']), 'joker_type'] = 'five_of_a_kind'
df.loc[(3 == counts) & ('high_card' == df['hand_type']), 'hand_type'] = 'three_of_a_kind'
df.loc[(3 == counts) & ('high_card' == df['joker_type']), 'joker_type'] = 'four_of_a_kind'

df.loc[(2 == counts) & ('three_of_a_kind' == df['hand_type']), 'hand_type'] = 'full_house'
df.loc[(2 == counts) & ('three_of_a_kind' == df['joker_type']), 'joker_type'] = 'five_of_a_kind'
df.loc[(2 == counts) & ('one_pair' == df['hand_type']), 'hand_type'] = 'two_pair'
df.loc[(2 == counts) & ('one_pair' == df['joker_type']), 'joker_type'] = 'four_of_a_kind'
df.loc[(2 == counts) & ('high_card' == df['hand_type']), 'hand_type'] = 'one_pair'
df.loc[(2 == counts) & ('high_card' == df['joker_type']), 'joker_type'] = 'three_of_a_kind'

df.loc[(1 == counts) & ('four_of_a_kind' == df['joker_type']), 'joker_type'] = 'five_of_a_kind'
df.loc[(1 == counts) & ('three_of_a_kind' == df['joker_type']), 'joker_type'] = 'four_of_a_kind'
df.loc[(1 == counts) & ('two_pair' == df['joker_type']), 'joker_type'] = 'full_house'
df.loc[(1 == counts) & ('one_pair' == df['joker_type']), 'joker_type'] = 'three_of_a_kind'
df.loc[(1 == counts) & ('high_card' == df['joker_type']), 'joker_type'] = 'one_pair'

splits = df['hand'].str.split('', expand=True).astype(cards_cat)
df = pd.merge(df, splits.loc[:, 1:5], left_index=True, right_index=True)
df.sort_values(by=['hand_type', 1, 2, 3, 4, 5], inplace=True, ignore_index=True)
df['winnings'] = (df.index + 1) * df['bid']

print(f"The total winnings are {df['winnings'].sum()}")

# resort with J as joker
cards = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
for i in range(1, 6):
    df[i] = df[i].cat.reorder_categories(cards)
df.sort_values(by=['joker_type', 1, 2, 3, 4, 5], inplace=True, ignore_index=True)
df['joker_winnings'] = (df.index + 1) * df['bid']

print(f"The new total winnings with J as jokers are {df['joker_winnings'].sum()}")
