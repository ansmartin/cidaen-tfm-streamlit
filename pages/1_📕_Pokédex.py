import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    layout="wide"
)

# functions

@st.cache_data
def load_data_species():
    df = pd.read_parquet('./data/pokemon-species.parquet')
    return df

@st.cache_data
def load_data_forms():
    df = pd.read_parquet('./data/pokemon-forms.parquet')
    return df

def get_tick_emoji(condition):
    if condition:
        return '✅'
    else:
        return '❌'

def get_form_name(form_name_text):
    if form_name_text:
        form_name = form_name_text.upper()
    else:
        form_name = 'None'
    return form_name


# APP

st.title('Pokédex')

# get data
df = load_data_species()
df_forms = load_data_forms()

option = st.selectbox(
    'Select a Pokémon:',
    df.species_name
)

poke = df[df.species_name==option].iloc[0]
forms = df_forms[df_forms.species_name==option]

# default form
poke_form = forms[forms.is_default].iloc[0]

species_name = option.upper()



# ------------------------------------------------------------

'---'
# Pokémon name and category
st.markdown(f'## {species_name}')
f'{poke.genus}'
'\n'

col1, col2, col3 = st.columns(3)

# ------------------------------------------------------------

with col1:
    with st.container(border=True):
        image_url = poke.sprite_default

        if(image_url):
            st.image(image_url, use_container_width=True)
        else:
            'Image not found'


    # minicol1, minicol2 = st.columns(2)
    # with minicol1:
    #     with st.container(border=True, height=250):
    #         f'**Varieties List:**'
    #         poke.varieties_list

    # with minicol2:
    #     with st.container(border=True, height=250):
    #         f'**Forms List:**'
    #         poke.forms_list


# ------------------------------------------------------------


with col2:
    #with st.container(border=True):
        with st.container(border=True):
            f'**National Pokédex number**: {poke.species_id}'
            f'**Default form name:** {get_form_name(poke_form.form_name_text)}'
        
        with st.container(border=True):
            # typing
            minicol1, minicol2, minicol3 = st.columns([1,2,2])
            with minicol1:
                '**Type:**'
            with minicol2:
                if(poke.first_type):
                    st.image(f'./images/types/{poke.first_type}.png', use_container_width=True)
            with minicol3:
                if(poke.second_type):
                    st.image(f'./images/types/{poke.second_type}.png', use_container_width=True)

        with st.container(border=True):
            # abilities
            abilities = f'{poke.first_ability.upper().replace('-',' ')}'
            if(poke.second_ability):
                abilities += f' / {poke.second_ability.upper().replace('-',' ')}'
            f'**Abilities:** {abilities}'

            hidden_ability = poke.hidden_ability.upper().replace('-',' ') if poke.hidden_ability else 'None'
            f'**Hidden ability:** {hidden_ability}'

        with st.container(border=True):
            height = poke.height/10 if pd.notna(poke.height) else '???'
            f'**Height:** {height} m'

            weight = poke.weight/10 if pd.notna(poke.weight) else '???'
            f'**Weight:** {weight} kg'

        with st.container(border=True):
            gender_ratio = poke.gender_rate
            if(gender_ratio<0):
                f'**Gender ratio:** Gender unknown'
            else:
                female_ratio = (gender_ratio * 10) * 1.25
                male_ratio = 100 - female_ratio
                # colors: blue, green, orange, red, violet.
                f'**Gender ratio:** :blue[{male_ratio:.2f}% male] / :violet[{female_ratio:.2f}% female]'
            
            f'**Has gender differences:** {get_tick_emoji(poke.has_gender_differences)}'

        with st.container(border=True):
            f'**Catch rate value (between 0 and 255):** {poke.capture_rate}'
            
        with st.container(border=True):
            # experience
            f'**Base experience yield:** {poke.base_experience}'
            f'**Leveling rate:** {poke.growth_rate_name.upper().replace('-',' ')}'

        with st.container(border=True):
            f'**Introduced in generation**: {poke.species_generation_number}'
            game = poke_form.version_group_name.replace('-',' ').upper() if poke_form.version_group_name else ''
            f'**Game versions:** {game}'

# ------------------------------------------------------------

with col3:
    #with st.container(border=True):
        with st.container(border=True):
            # evolutions
            preevo = poke.evolves_from_pokemon_base_name.upper() if poke.evolves_from_pokemon_base_name else 'None'
            f'**Evolves from:** {preevo}'
            evolutions = (', '.join(poke.evolutions)).upper().replace("'",'') if poke.evolutions.size>0 else 'None'
            f'**Evolutions:** {evolutions}'

        with st.container(border=True):
            f'**Shape:** {poke.shape_name.upper().replace('-',' ')}'

        with st.container(border=True):
            f'**Color:** {poke.color_name.upper()}'
            st.write(
                f"""<div style="background-color: {poke.color_name}; border-radius: 10px; width: 20px; height: 20px; "> </div>""",
                unsafe_allow_html=True
            )
            '\n'

        with st.container(border=True):
            f'**Base friendship:** {poke.base_happiness}'

        with st.container(border=True):
            egg_group = f'**Egg Groups:** {poke.first_egg_group.upper()}'
            if(poke.second_egg_group):
                egg_group += f' / {poke.second_egg_group.upper()}'
            egg_group

            f'**Hatch time:** {poke.hatch_counter} cycles'

        with st.container(border=True):
            f'**Is baby:** {get_tick_emoji(poke.is_baby)}'
            f'**Is legendary:** {get_tick_emoji(poke.is_legendary)}'
            f'**Is mythical:** {get_tick_emoji(poke.is_mythical)}'

        with st.container(border=True):
            f'**Has Mega-Evolution:** {get_tick_emoji(poke.has_mega)}'
            f'**Has Gigantamax:** {get_tick_emoji(poke.has_gmax)}'
            f'**Has a regional form:** {get_tick_emoji(poke.has_regional)}'


# ------------------------------------------------------------

'\n'

with st.container(border=True):
    games = [
        'red_en', 'blue_en', 'yellow_en', 
        'gold_en', 'silver_en', 'crystal_en',
        'ruby_en', 'sapphire_en', 'emerald_en', 'firered_en', 'leafgreen_en',
        'diamond_en', 'pearl_en', 'platinum_en', 'heartgold_en', 'soulsilver_en', 
        'black_en', 'white_en', 'black_2_en', 'white_2_en',
        'x_en', 'y_en', 'omega_ruby_en', 'alpha_sapphire_en', 
        'sun_en', 'moon_en', 'ultra_sun_en', 'ultra_moon_en', 'lets_go_pikachu_en', 'lets_go_eevee_en', 
        'sword_en', 'shield_en', 'legends_arceus_en', 
        'scarlet_en', 'violet_en'
    ]
    entries_games = []
    entries_text = []
    for x in games:
        if poke[x]:
            game_name = x[:-3].upper().replace('_',' ')
            entries_games.append(game_name)
            entries_text.append(poke[x])
    
    df_entries = pd.DataFrame({
        'game': entries_games,
        'description': entries_text
    })

    st.markdown('#### Pokédex entries')
    st.dataframe(df_entries, hide_index=True)


'\n'

# ------------------------------------------------------------


col1, col2 = st.columns([2,1])

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

        f'**Total stats:** {poke.stats_total}'

with col2:
    with st.container(border=True):
        st.markdown('#### EV yield')

        effort_values = pd.DataFrame({
            'stat': ['HP','Attack','Defense','SpecialAttack','SpecialDefense','Speed'],
            'value': [poke.stat_hp_effort, poke.stat_attack_effort, poke.stat_defense_effort, poke.stat_special_attack_effort, poke.stat_special_defense_effort, poke.stat_speed_effort]
        })

        chart = alt.Chart(effort_values).mark_bar().encode(
            y=alt.Y('stat', sort=None),
            x=alt.X('value', scale=alt.Scale(domain=[0, 3], clamp=True)),
        )

        st.altair_chart(chart)

        f'**Total effort values:** {poke.effort_total}'

# with col3:
#     with st.container(border=True):
#         st.markdown('#### Move List')
#         poke.moves_list

'\n'

# ------------------------------------------------------------


    
# FORMS
has_forms = forms.shape[0]>1

if has_forms:

    '---'

    st.markdown(f'## Forms')
    '\n'
    
    poke_otherforms = forms[~forms.is_default]

    option = st.selectbox(
        'Select a form:',
        poke_otherforms.pokemon_form_name
    )
    
    poke_form = poke_otherforms[poke_otherforms.pokemon_form_name==option].iloc[0]

    # description
    if poke.forms_description:
        '\n'
        poke.forms_description

    '\n'

    # name = (
    #     poke_form.pokemon_form_name_text 
    #     if poke_form.pokemon_form_name_text 
    #     else f'{poke_form.species_name} ({(poke_form.form_name_text.replace('-',' ') if poke_form.form_name_text else '')})'
    # ).upper()
    name = (poke_form.pokemon_form_name_text if poke_form.pokemon_form_name_text else poke_form.species_name).upper()

    # Pokémon form name
    st.markdown(f'## {name}')
    '\n'
    

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            image_url = poke_form.sprite_default

            if(image_url):
                st.image(image_url, use_container_width=True)
            else:
                'Image not found'

    with col2:
        #with st.container(border=True):
            with st.container(border=True):
                f'**Form name:** {get_form_name(poke_form.form_name_text)}'
            
            #if(not poke_form.is_gmax):
            with st.container(border=True):
                # typing
                minicol1, minicol2, minicol3 = st.columns([1,2,2])
                with minicol1:
                    '**Type:**'
                with minicol2:
                    if(poke_form.first_type):
                        st.image(f'./images/types/{poke_form.first_type}.png', use_container_width=True)
                with minicol3:
                    if(poke_form.second_type):
                        st.image(f'./images/types/{poke_form.second_type}.png', use_container_width=True)

            with st.container(border=True):
                # abilities
                abilities = f'{poke_form.first_ability.upper().replace('-',' ')}'
                if(poke_form.second_ability):
                    abilities += f' / {poke_form.second_ability.upper().replace('-',' ')}'
                f'**Abilities:** {abilities}'

                hidden_ability = poke_form.hidden_ability.upper().replace('-',' ') if poke_form.hidden_ability else 'None'
                f'**Hidden ability:** {hidden_ability}'

            with st.container(border=True):
                height = poke_form.height/10 if pd.notna(poke_form.height) else '???'
                f'**Height:** {height} m'

                weight = poke_form.weight/10 if pd.notna(poke_form.weight) else '???'
                f'**Weight:** {weight} kg'

            with st.container(border=True):
                f'**Form introduced in generation**: {poke_form.form_generation_number}'
                game = poke_form.version_group_name.replace('-',' ').upper() if poke_form.version_group_name else ''
                f'**Game versions:** {game}'

            # if(poke_form.is_gmax):
            #     with st.container(border=True):
            #         'Gigantamax forms have the same types, abilities, base stats and effort values as the base Pokémon.'

    with col3:
        #with st.container(border=True):
            if(poke_form.is_mega | poke_form.is_gmax):
                pass
            else:
                with st.container(border=True):
                    # evolutions
                    preevo = poke_form.evolves_from_pokemon_base_name.upper() if poke_form.evolves_from_pokemon_base_name else 'None'
                    f'**Evolves from:** {preevo}'
                    evolutions = (', '.join(poke_form.evolutions)).upper().replace("'",'') if poke_form.evolutions.size>0 else 'None'
                    f'**Evolutions:** {evolutions}'

            # color of this form 
            with st.container(border=True):
                f'**Color:** {poke_form.color_name.upper()}'
                st.write(
                    f"""<div style="background-color: {poke_form.color_name}; border-radius: 10px; width: 20px; height: 20px; "> </div>""",
                    unsafe_allow_html=True
                )
                '\n'

            with st.container(border=True):
                f'**Is a battle-only form:** {get_tick_emoji(poke_form.is_battle_only)}'
                f'**Is Mega-Evolved:** {get_tick_emoji(poke_form.is_mega)}'
                f'**Is Gigantamax:** {get_tick_emoji(poke_form.is_gmax)}'

            with st.container(border=True):
                f'**Is a regional form:** {get_tick_emoji(poke_form.is_regional)}'
                f'**Is separated from species:** {get_tick_emoji(poke_form.is_separated_from_species)}'
                

    
    # -----------------------------

    # if(poke_form.is_gmax):
    #     with st.container(border=True):
    #         pass

    # else:   
    col1, col2 = st.columns([2,1])

    with col1:
        # stats bar chart
        with st.container(border=True):
            st.markdown('#### Base stats')

            stats = pd.DataFrame({
                'stat': ['HP','Attack','Defense','SpecialAttack','SpecialDefense','Speed'],
                'value': [poke_form.stat_hp_base, poke_form.stat_attack_base, poke_form.stat_defense_base, poke_form.stat_special_attack_base, poke_form.stat_special_defense_base, poke_form.stat_speed_base]
            })

            chart = alt.Chart(stats).mark_bar().encode(
                y=alt.Y('stat', sort=None),
                x=alt.X('value', scale=alt.Scale(domain=[0, 255], clamp=True)),
                color = combined_condition 
            )

            st.altair_chart(chart)

            f'**Total stats:** {poke_form.stats_total}'

    with col2:
        with st.container(border=True):
            st.markdown('#### EV yield')

            effort_values = pd.DataFrame({
                'stat': ['HP','Attack','Defense','SpecialAttack','SpecialDefense','Speed'],
                'value': [poke_form.stat_hp_effort, poke_form.stat_attack_effort, poke_form.stat_defense_effort, poke_form.stat_special_attack_effort, poke_form.stat_special_defense_effort, poke_form.stat_speed_effort]
            })

            chart = alt.Chart(effort_values).mark_bar().encode(
                y=alt.Y('stat', sort=None),
                x=alt.X('value', scale=alt.Scale(domain=[0, 3], clamp=True)),
            )

            st.altair_chart(chart)

            f'**Total effort values:** {poke_form.effort_total}'

    # with col3:
    #     with st.container(border=True):
    #         st.markdown('#### Move List')
    #         poke_form.moves_list