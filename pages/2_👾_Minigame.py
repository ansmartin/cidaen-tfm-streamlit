import streamlit as st
import pandas as pd
import random
import json

st.set_page_config(
    layout="wide"
)

# functions

@st.cache_data
def load_data_forms(path):
    df = pd.read_parquet(path)
    df = df[(df.is_default) | (df.is_mega) | (df.is_gmax) | (df.is_regional & ~df.is_totem)]
    return df

@st.cache_data
def load_data_species(path):
    df = pd.read_parquet(path)
    return df

def get_tick_emoji(condition):
    if condition:
        return '✅'
    else:
        return '❌'


# APP

st.title('Guess the Pokémon!')

# set random seed
seed = st.number_input('Set the random seed', min_value=0, max_value=999999999999999, value=0, step=1)
random.seed(seed)

'---'

# get data
get_data_from_aws = False

if get_data_from_aws:
    with open('data/aws.json', 'r') as file:
        data_urls = json.load(file)

    df_forms = load_data_forms(data_urls['forms'])
    df_species = load_data_species(data_urls['species'])
else:
    df_forms = load_data_forms('./data/pokemon-forms.parquet')
    df_species = load_data_species('./data/pokemon-species.parquet')


# select
random_value = random.randint(0, df_forms.shape[0]-1)
poke = df_forms.iloc[random_value]
species = df_species.loc[poke.species_id]

col1, col2 = st.columns(2)
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

    st.markdown(f'#### :grey[HINT 2.] Name starts with the letter {poke.pokemon_name[0].upper()}')

    st.markdown(f'#### :grey[HINT 3.] Its shape is {species.shape_name.upper()}')

    hint4 = f'#### :grey[HINT 4.] This Pokémon was introduced in generation {poke.form_generation_number}'
    if not poke.is_default and poke.form_generation_number>species.species_generation_number:  
        hint4 += f', but the Pokémon species was introduced in generation {species.species_generation_number}'
    
    st.markdown(hint4)

    if not poke.is_mega and not poke.is_gmax:
        st.markdown(f'#### :grey[HINT 5.] Has pre-evolution: {get_tick_emoji(poke.evolves_from_pokemon_base_name!=None)}')
        st.markdown(f'#### :grey[HINT 6.] Has evolution: {get_tick_emoji(poke.evolutions.size>0)}')


    '\n'
    '\n'

    if poke.is_default:
        if poke.has_gender_differences:
            st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon has gender differences')
        if poke.has_mega:
            st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon can Mega-Evolve')
        if poke.has_gmax:
            st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon can Gigantamax')


    if poke.is_legendary:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is considered legendary')
    if poke.is_sublegendary:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is considered sub-legendary')
    if poke.is_mythical:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is considered mythical')
    if poke.is_powerhouse:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is considered powerhouse')

    if poke.is_mega:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is Mega-Evolved')
    elif poke.is_gmax:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is Gigantamax')
    elif poke.is_regional:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is a regional form')
    elif not poke.is_default:
        st.markdown(f'#### :grey[ADDITIONAL HINT.] This Pokémon is not considered the default within its own species')



with col2:
    with st.container(border=True):
        option = st.selectbox(
            'Select the name of this Pokémon:',
            df_forms.pokemon_name
        )

        if option==poke.pokemon_name:
            '✅ Correct answer. You are an expert!'

            name = (poke.pokemon_form_name_text if poke.pokemon_form_name_text else poke.species_name).upper()
            f'The name of this Pokémon is {name}'

            image_url = poke.sprite_default
            if(image_url):
                st.image(image_url, width=300)
        else:
            '❌ Wrong answer'
