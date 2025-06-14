import streamlit as st
import pandas as pd
import random

st.set_page_config(
    layout="wide"
)

# functions

@st.cache_data
def load_data(path):
    df = pd.read_parquet(path)
    return df


# APP

st.title('Guess the Pokémon!')

# set random seed
seed = st.number_input('Set the random seed', min_value=0, max_value=999999, value=0, step=1)
random.seed(seed)

'\n'

col1, col2 = st.columns(2)

df = load_data('./data/gold.parquet')

random_value = random.randint(0, df.shape[0]-1)

poke = df.iloc[random_value]

with col1:


    # types
    typing = f'{poke.first_type.upper()}'
    if(poke.second_type):
        typing += f' / {poke.second_type.upper()}' 

    st.markdown(f'#### HINT 1. Type {typing}')

    st.markdown(f'#### HINT 2. Color {poke.color_name.upper()}')

    st.markdown(f'#### HINT 3. Name starts with the letter \"{poke.pokemon_name[0].upper()}\"')

    hint4 = f'#### HINT 4. This Pokémon was introduced in generation {poke.pokemon_generation_number}'
    if not poke.is_default and poke.pokemon_generation_number>poke.species_generation_number:  
        hint4 += f', but the Pokémon species was introduced in generation {poke.species_generation_number}'
    
    st.markdown(hint4)

    hint5 = '#### HINT 5. '
    if(poke.evolves_from_species_name):
        hint5 += 'Has pre-evolution'
    else:
        hint5 += 'Does not have pre-evolution'
    st.markdown(hint5)

    hint6 = '#### HINT 6. '
    if(poke.evolutions.size>0):
        hint6 += 'Can evolve'
    else:
        hint6 += 'Cannot evolve'
    st.markdown(hint6)

    # preevo = poke.evolves_from_species_name is not None
    # evolutions = poke.evolutions.size>0

    # if preevo and evolutions:
    #     st.markdown(f'#### HINT 5. This Pokémon has pre-evolution and can evolve')
    # else:
    #     if preevo:
    #         st.markdown(f'#### HINT 5. This Pokémon has pre-evolution but cannot evolve')
    #     elif evolutions:
    #         st.markdown(f'#### HINT 5. This Pokémon has no pre-evolution but can evolve')
    #     else:
    #         st.markdown(f'#### HINT 5. This Pokémon has neither pre-evolution nor evolutions')


    '\n'
    '\n'

    if poke.has_gender_differences:
        st.markdown(f'#### ADDITIONAL HINT. This Pokémon species has gender differences')
    if poke.is_baby:
        st.markdown(f'#### ADDITIONAL HINT. This Pokémon is considered baby')
    if poke.is_legendary:
        st.markdown(f'#### ADDITIONAL HINT. This Pokémon is considered legendary')
    if poke.is_mythical:
        st.markdown(f'#### ADDITIONAL HINT. This Pokémon is considered mythical')

    if poke.is_mega:
        st.markdown(f'#### ADDITIONAL HINT. This Pokémon is Mega-Evolved')
    elif poke.is_gmax:
        st.markdown(f'#### ADDITIONAL HINT. This Pokémon is Gigantamax')
    elif not poke.is_default:
        st.markdown(f'#### ADDITIONAL HINT. This Pokémon is not considered the default within its own species')

    if poke.has_mega:
        st.markdown(f'#### ADDITIONAL HINT. This Pokémon can Mega-Evolve')
    if poke.has_gmax:
        st.markdown(f'#### ADDITIONAL HINT. This Pokémon can Gigantamax')


with col2:
    with st.container(border=True):
        option = st.selectbox(
            'Select the name of this Pokémon:',
            df.pokemon_name
        )

        if option==poke.pokemon_name:
            '✅ Correct answer. You are an expert!'
            f'The Pokémon\'s name is {option.upper()}'
            image_url = poke.sprite_default
            if(image_url):
                st.image(image_url, width=300)
        else:
            '❌ Wrong answer'
