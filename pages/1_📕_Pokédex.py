import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    layout="wide"
)

# functions

@st.cache_data
def load_data(path):
    df = pd.read_parquet(path)
    return df

def get_tick_emoji(condition):
    if condition:
        return '✅'
    else:
        return '❌'


# APP

st.title('Pokédex')

df = load_data('./data/gold.parquet')

option = st.selectbox(
    'Select a Pokémon:',
    df.pokemon_name
)

st.write('You selected:', option.upper())


poke = df[df.pokemon_name==option].iloc[0]

'\n'

col1, col2, col3 = st.columns(3)

# ------------------------------------------------------------

with col1:
    with st.container(border=True):
        image_url = poke.sprite_default
        
        if(image_url):
            st.image(image_url)
        else:
            'Image not found'


# ------------------------------------------------------------


with col2:
    #with st.container(border=True):
        with st.container(border=True):
            f'**Pokémon name:** {option.upper()}'
            f'**Introduced in generation**: {poke.pokemon_generation_number}'
        with st.container(border=True):
            f'**National Pokédex number**: {poke.species_id}'
            f'**Species name:** {poke.species_name.upper()}'
            f'**Species introduced in generation**: {poke.species_generation_number}'
        
        with st.container(border=True):
            # types
            typing = f'**Type:** {poke.first_type.upper()}'
            if(poke.second_type):
                typing += f' / {poke.second_type.upper()}' 
            typing

        with st.container(border=True):
            # abilities
            abilities = f'**Abilities:** {poke.first_ability.upper()}'
            if(poke.second_ability):
                abilities += f' / {poke.second_ability.upper()}'
            abilities

            hidden_ability = poke.hidden_ability.upper() if poke.hidden_ability else 'None'
            f'**Hidden ability:** {hidden_ability}'

        with st.container(border=True):
            f'**Catch rate value (between 0 and 255):** {poke.capture_rate}'

        with st.container(border=True):
            gender_ratio = poke.gender_rate
            if(gender_ratio<0):
                f'**Gender ratio:** Gender unknown'
            else:
                female_ratio = (gender_ratio * 10) * 1.25
                male_ratio = 100 - female_ratio
                f'**Gender ratio:** :blue[{male_ratio:.2f}% male] / :violet[{female_ratio:.2f}% female]'
            
            # colors: blue, green, orange, red, violet.
            f'**Has gender differences:** {get_tick_emoji(poke.has_gender_differences)}'

        with st.container(border=True):
            egg_group = f'**Egg Group:** {poke.first_egg_group.upper()}'
            if(poke.second_egg_group):
                egg_group += f' / {poke.second_egg_group.upper()}'
            egg_group

            f'**Hatch time:** {poke.hatch_counter} cycles'
            f'**Is baby:** {get_tick_emoji(poke.is_baby)}'

with col3:
    #with st.container(border=True):
        with st.container(border=True):
            f'**Height:** {poke.height/10} m'
            f'**Weight:** {poke.weight/10} kg'
            f'**Shape:** {poke.shape_name.upper()}'

            f'**Color:** {poke.color_name.upper()}'
            st.write(
                f"""<div style="background-color: {poke.color_name}; border-radius: 10px; width: 20px; height: 20px; "> </div>""",
                unsafe_allow_html=True
            )
            '\n'

        with st.container(border=True):
            # experience
            f'**Base experience yield:** {poke.base_experience}'
            f'**Leveling rate:** {poke.growth_rate_name.upper().replace('-',' ')}'

        with st.container(border=True):
            # evolutions
            preevo = poke.evolves_from_species_name.upper() if poke.evolves_from_species_name else 'None'
            f'**Evolves from species:** {preevo}'

            evolutions = (', '.join(poke.evolutions)).upper().replace("'",'') if poke.evolutions.size>0 else 'None'
            f'**Potential evolutions:** {evolutions}'

        with st.container(border=True):
            f'**Is Mega-Evolved:** {get_tick_emoji(poke.is_mega)}'
            f'**Is Gigantamax:** {get_tick_emoji(poke.is_gmax)}'
        with st.container(border=True):
            f'**Has Mega-Evolution:** {get_tick_emoji(poke.has_mega)}'
            f'**Has Gigantamax:** {get_tick_emoji(poke.has_gmax)}'

        with st.container(border=True):
            f'**Is legendary:** {get_tick_emoji(poke.is_legendary)}'
            f'**Is mythical:** {get_tick_emoji(poke.is_mythical)}'

'\n'


col1, col2 = st.columns(2)

with col1:
    # stats bar chart
    with st.container(border=True):
        st.markdown('#### Base stats')

        stats = pd.DataFrame({
            'stat': ['HP','Attack','Defense','SpecialAttack','SpecialDefense','Speed'],
            'value': [poke.stat_hp_base, poke.stat_attack_base, poke.stat_defense_base, poke.stat_special_attack_base, poke.stat_special_defense_base, poke.stat_speed_base]
        })

        # colors
        color_condition1 = alt.condition(
            alt.datum.value<50,
            alt.value("red"),
            alt.value("orange")
        )
        color_condition2 = alt.condition(
            alt.datum.value>=100,
            alt.value("green"),
            alt.value("green"),
        )
        combined_condition = color_condition1.copy()
        combined_condition['condition'] = [color_condition1['condition'], color_condition2['condition']]

        chart = alt.Chart(stats).mark_bar().encode(
            y=alt.Y('stat', sort=None),
            x=alt.X('value', scale=alt.Scale(domain=[0, 255], clamp=True)),
            color = combined_condition 
        )

        st.altair_chart(chart)

        f'**Total stats:** {poke.bst}'

    with st.container(border=True):
        st.markdown('#### EV yield')

        minicol1, minicol2, minicol3, minicol4, minicol5, minicol6 = st.columns(6)
        with minicol1:
            'HP'
            poke.stat_hp_effort
        with minicol2:
            'Attack'
            poke.stat_attack_effort
        with minicol3:
            'Defense'
            poke.stat_defense_effort
        with minicol4:
            'SpAttack'
            poke.stat_special_attack_effort
        with minicol5:
            'SpDefense'
            poke.stat_special_defense_effort
        with minicol6:
            'Speed'
            poke.stat_speed_effort


with col2:
        minicol1, minicol2 = st.columns(2)
        with minicol1:
            with st.container(border=True):
                st.markdown('#### Move List')
                poke.moves_list
        with minicol2:
            with st.container(border=True):
                ''
                #st.markdown('#### Text entries')
                #poke.flavor_text_entries