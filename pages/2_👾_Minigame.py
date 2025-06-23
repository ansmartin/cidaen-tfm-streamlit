import streamlit as st
import pandas as pd
import random

st.set_page_config(
    layout="wide"
)

# functions

@st.cache_data
def load_data():
    df = pd.read_parquet('./data/minigame.parquet')
    return df

def get_tick_emoji(condition):
    if condition:
        return '✅'
    else:
        return '❌'


# APP

st.title('Guess the Pokémon!')

# set random seed
seed = st.number_input('Set the random seed', min_value=0, max_value=999999, value=0, step=1)
random.seed(seed)

'\n'

col1, col2 = st.columns(2)

df = load_data()

random_value = random.randint(0, df.shape[0]-1)

poke = df.iloc[random_value]

with col1:


    # types
    minicol1, minicol2, minicol3, minicol4  = st.columns([1,1,1,1])
    with minicol1:
        st.markdown(f'#### :grey[HINT 1.] Type:')
    with minicol2:
        if(poke.first_type):
            st.image(f'./images/types/{poke.first_type}.png', use_container_width=True)
    with minicol3:
        if(poke.second_type):
            st.image(f'./images/types/{poke.second_type}.png', use_container_width=True)


    st.markdown(f'#### :grey[HINT 2.] Its main color is {poke.color_name.upper()}')

    st.markdown(f'#### :grey[HINT 3.] Name starts with the letter {poke.pokemon_name[0].upper()}')

    hint4 = f'#### :grey[HINT 4.] This Pokémon was introduced in generation {poke.pokemon_generation_number}'
    if not poke.is_default and poke.pokemon_generation_number>poke.species_generation_number:  
        hint4 += f', but the Pokémon species was introduced in generation {poke.species_generation_number}'
    
    st.markdown(hint4)

    st.markdown(f'#### :grey[HINT 5.] Has pre-evolution: {get_tick_emoji(poke.evolves_from_pokemon_base_name!=None)}')
    st.markdown(f'#### :grey[HINT 6.] Has evolution: {get_tick_emoji(poke.evolutions.size>0)}')


    '\n'
    '\n'

    if poke.is_default:
        if poke.has_gender_differences:
            st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon has gender differences')

    if poke.is_baby:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is considered baby')
    if poke.is_legendary:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is considered legendary')
    if poke.is_mythical:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is considered mythical')

    if poke.is_mega:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is Mega-Evolved')
    elif poke.is_gmax:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is Gigantamax')
    elif poke.is_regional:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is a regional form')
    elif not poke.is_default:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is not considered the default within its own species')

    if poke.has_mega:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon can Mega-Evolve')
    if poke.has_gmax:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon can Gigantamax')
    if poke.has_regional:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon has a regional form')


with col2:
    with st.container(border=True):
        option = st.selectbox(
            'Select the name of this Pokémon:',
            df.pokemon_name
        )

        if option==poke.pokemon_name:
            '✅ Correct answer. You are an expert!'
            f'The name of this Pokémon is {option.upper()}'
            image_url = poke.sprite_default
            if(image_url):
                st.image(image_url, width=300)
        else:
            '❌ Wrong answer'
