import streamlit as st
import pandas as pd
import random

st.set_page_config(
    layout="wide"
)

# functions

@st.cache_data
def load_data():
    df = pd.read_parquet('./data/pokemon-forms.parquet')
    return df

def get_tick_emoji(condition):
    if condition:
        return '✅'
    else:
        return '❌'


# APP

st.title('Pokémon List')

# get data
df = load_data()

# init lists
types_list = [
    'grass', 'fire', 'water', 'bug', 'normal', 'poison', 'electric',
    'ground', 'fairy', 'fighting', 'psychic', 'rock', 'ghost', 'ice',
    'dragon', 'dark', 'steel', 'flying', None
]
colors_list = [
    'green', 'red', 'blue', 'white', 'brown', 
    'yellow', 'purple', 'pink', 'gray', 'black'
]
shape_list = [
    'quadruped', 'upright', 'armor', 'squiggle', 'bug-wings', 'wings',
    'humanoid', 'legs', 'blob', 'heads', 'tentacles', 'arms', 'fish', 'ball'
]
egg_group_list = [
    'ground','dragon','flying','mineral',
    'water1','water2','water3',
    'plant','bug','fairy',
    'ditto', 'monster','humanshape','indeterminate',
    'no-eggs', None
 ]
gens_list = [ 
    x for x in range(1,10) 
]
games_list = [
    'red-and-blue', 
    'gold-and-silver', 
    'ruby-and-sapphire', 'emerald', 'firered-and-leafgreen',
    'diamond-and-pearl', 'platinum', 'heartgold-and-soulsilver',
    'black-and-white', 'black-2-and-white-2',
    'x-and-y', 'omega-ruby-and-alpha-sapphire',
    'sun-and-moon', 'ultra-sun-and-ultra-moon', 'lets-go-pikachu-and-lets-go-eevee',
    'sword-and-shield', 'the-isle-of-armor', 'the-crown-tundra', 'legends-arceus',
    'scarlet-and-violet', 'the-teal-mask', 'the-indigo-disk',
]

'---'

st.markdown(f'#### Filters')
'\n'

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        'Include forms:'
        include_default = st.checkbox("Default species", value=True)
        include_regional = st.checkbox("Regional forms", value=True)
        include_mega = st.checkbox("Megas", value=True)
        include_gmax = st.checkbox("Gigantamax", value=True)
        include_other = st.checkbox("Other forms", value=True)

        if not include_default:
            df = df[~df.is_default]
        if not include_regional:
            df = df[~df.is_regional]
        if not include_mega:
            df = df[~df.is_mega]
        if not include_gmax:
            df = df[~df.is_gmax]
        if not include_other:
            df = df[(df.is_default | df.is_regional | df.is_mega | df.is_gmax)]

    with st.container(border=True):
        'Select only:'
        baby = st.checkbox("Baby", value=False)
        legendary = st.checkbox("Legendary", value=False)
        mythical = st.checkbox("Mythical", value=False)
        totem = st.checkbox("Totem", value=False)
        #battle = st.checkbox("Battle-only forms", value=False)
        
        if baby:
            df = df[df.is_baby]
        if legendary:
            df = df[df.is_legendary]
        if mythical:
            df = df[df.is_mythical]
        if totem:
            df = df[df.is_totem]
        # if battle:
        #     df = df[df.is_battle_only]


with col2:
    with st.container(border=True):
        
        checked = st.checkbox('Filter by type')

        if checked:
            options = ['Any type position', 'Specify type position']

            option = st.selectbox(
                #'Filter by type:',
                '',
                options
            )

            #types_list.append(None)

            with st.container(border=True):
                if option==options[1]:
                    with st.container():
                        first_types_selected = st.multiselect("First type", types_list)
                    with st.container():
                        second_types_selected = st.multiselect("Second type", types_list)
                
                    if len(first_types_selected)==0 and len(second_types_selected)==0:
                        pass
                    else:
                        cond1 = cond2 = True
                        if len(first_types_selected)>0:
                            cond1 = (df.first_type.isin(first_types_selected))
                        if len(second_types_selected)>0:
                            cond2 = (df.second_type.isin(second_types_selected))

                        df = df[(cond1) & (cond2)]

                elif option==options[0]:
                    types_container = st.container()

                    with types_container:
                        types_selected = st.multiselect("Type", types_list)

                        df = df[(df.first_type.isin(types_selected)) | (df.second_type.isin(types_selected))]

    with st.container(border=True):

        checked = st.checkbox('Filter by ability')

        if checked:
            options = ['Any ability position', 'Specify ability position']

            option = st.selectbox(
                '',
                options
            )

            abilities = set(df.first_ability)
            abilities.update(set(df.second_ability))
            abilities.update(set(df.hidden_ability))
            abilities_list = list(abilities)

            with st.container(border=True):
                if option==options[1]:
                    with st.container():
                        first_abilities_selected = st.multiselect("First ability", abilities_list)
                    with st.container():
                        second_abilities_selected = st.multiselect("Second ability", abilities_list)
                    with st.container():
                        hidden_abilities_selected = st.multiselect("Hidden ability", abilities_list)

                    if len(first_abilities_selected)==0 and len(second_abilities_selected)==0 and len(hidden_abilities_selected)==0:
                        pass
                    else:
                        cond1 = cond2 = cond3 = True
                        if len(first_abilities_selected)>0:
                            cond1 = (df.first_ability.isin(first_abilities_selected))
                        if len(second_abilities_selected)>0:
                            cond2 = (df.second_ability.isin(second_abilities_selected))
                        if len(hidden_abilities_selected)>0:
                            cond3 = (df.hidden_ability.isin(hidden_abilities_selected))

                        df = df[(cond1) & (cond2) & (cond3)]

                elif option==options[0]:
                    abilities_container = st.container()

                    with abilities_container:
                        abilities_selected = st.multiselect("Ability", abilities_list)

                        df = df[
                            (df.first_ability.isin(abilities_selected)) | 
                            (df.second_ability.isin(abilities_selected)) | 
                            (df.hidden_ability.isin(abilities_selected))
                        ]

    with st.container(border=True):
        gens_selected = st.multiselect("Filter by Pokémon species generation", gens_list)
        if len(gens_selected)>0:
            df = df[df.species_generation_number.isin(gens_selected)]
            
        gens_selected = st.multiselect("Filter by Pokémon form generation", gens_list)
        if len(gens_selected)>0:
            df = df[df.form_generation_number.isin(gens_selected)]
            
    with st.container(border=True):
        games_selected = st.multiselect("Filter by game version", games_list)
        if len(games_selected)>0:
            df = df[df.version_group_name.isin(games_selected)]


with col3:
    with st.container(border=True):
        
        checked = st.checkbox('Filter by egg group')

        if checked:
            options = ['Any egg group position', 'Specify egg group position']

            option = st.selectbox(
                '',
                options
            )

            with st.container(border=True):
                if option==options[1]:
                    with st.container():
                        first_eg_selected = st.multiselect("First egg group", egg_group_list)
                    with st.container():
                        second_eg_selected = st.multiselect("Second egg group", egg_group_list)

                    if len(first_eg_selected)==0 and len(second_eg_selected)==0:
                        pass
                    else:
                        cond1 = cond2 = True
                        if len(first_eg_selected)>0:
                            cond1 = (df.first_egg_group.isin(first_eg_selected))
                        if len(second_eg_selected)>0:
                            cond2 = (df.second_egg_group.isin(second_eg_selected))

                        df = df[(cond1) & (cond2)]

                elif option==options[0]:
                    eggs_container = st.container()
                    with eggs_container:
                        eggs_selected = st.multiselect("Egg group", egg_group_list)
                        df = df[(df.first_egg_group.isin(eggs_selected)) | (df.second_egg_group.isin(eggs_selected))]

    with st.container(border=True):
        cond1 = cond2 = True
        checked_h = st.checkbox('Filter by height')
        if checked_h:
            height_slider = st.slider('Height', 1, 1000, (1,1000))
            cond1 = (df.height.between(height_slider[0], height_slider[1]))

        checked_w = st.checkbox('Filter by weight')
        if checked_w:
            weight_slider = st.slider('Weight', 1, 9999, (1,9999))
            cond2 = (df.weight.between(weight_slider[0], weight_slider[1]))

        if checked_h and checked_w:
            df = df[cond1 & cond2]
        elif checked_h:
            df = df[cond1]
        elif checked_w:
            df = df[cond2]

    with st.container(border=True):
        shapes_selected = st.multiselect("Filter by shape", shape_list)
        if len(shapes_selected)>0:
            df = df[df.shape_name.isin(shapes_selected)]

        colors_selected = st.multiselect("Filter by color", colors_list)
        if len(colors_selected)>0:
            df = df[df.color_name.isin(colors_selected)]

    with st.container(border=True):
        options = ['None','Select Pokémon without pre-evolution', 'Select Pokémon with pre-evolution']

        option = st.selectbox(
            'Filter by pre-evolution',
            options
        )

        if option==options[0]:
            pass
        elif option==options[1]:
            df = df[df.evolves_from_pokemon_base_name.isna()]
        else:
            df = df[df.evolves_from_pokemon_base_name.notna()]

    with st.container(border=True):
        checked = st.checkbox('Filter by evolutions')
        if checked:
            total_slider = st.slider('Number of potential evolutions', 0, 8, (0,8))
            condition = (df.evolutions.apply(lambda values: len(values)).between(total_slider[0], total_slider[1]))
            df = df[condition]

         
with col4:
    with st.container(border=True):
        checked = st.checkbox('Filter by base stats')

        if checked:
            with st.container(border=True):
                hp_slider = st.slider('HP', 0, 255, (0,255))
                attack_slider = st.slider('Attack', 0, 255, (0,255))
                defense_slider = st.slider('Defense', 0, 255, (0,255))
                sp_attack_slider = st.slider('SpecialAttack', 0, 255, (0,255))
                sp_defense_slider = st.slider('SpecialDefense', 0, 255, (0,255))
                speed_slider = st.slider('Speed', 0, 255, (0,255))

                condition = (
                    (df.stat_hp_base.between(hp_slider[0], hp_slider[1])) &
                    (df.stat_attack_base.between(attack_slider[0], attack_slider[1])) &
                    (df.stat_defense_base.between(defense_slider[0], defense_slider[1])) &
                    (df.stat_special_attack_base.between(sp_attack_slider[0], sp_attack_slider[1])) &
                    (df.stat_special_defense_base.between(sp_defense_slider[0], sp_defense_slider[1])) &
                    (df.stat_speed_base.between(speed_slider[0], speed_slider[1]))
                )
                df = df[condition]

        checked = st.checkbox('Filter by total base stats')

        if checked:
            total_slider = st.slider('Total', 0, 1530, (0,1530))
            condition = (df.stats_total.between(total_slider[0], total_slider[1]))
            df = df[condition]

    with st.container(border=True):
        checked = st.checkbox('Filter by effort values')

        if checked:
            with st.container(border=True):
                hp_slider = st.slider('HP', 0, 3, (0,3))
                attack_slider = st.slider('Attack', 0, 3, (0,3))
                defense_slider = st.slider('Defense', 0, 3, (0,3))
                sp_attack_slider = st.slider('SpecialAttack', 0, 3, (0,3))
                sp_defense_slider = st.slider('SpecialDefense', 0, 3, (0,3))
                speed_slider = st.slider('Speed', 0, 3, (0,3))

                condition = (
                    (df.stat_hp_effort.between(hp_slider[0], hp_slider[1])) &
                    (df.stat_attack_effort.between(attack_slider[0], attack_slider[1])) &
                    (df.stat_defense_effort.between(defense_slider[0], defense_slider[1])) &
                    (df.stat_special_attack_effort.between(sp_attack_slider[0], sp_attack_slider[1])) &
                    (df.stat_special_defense_effort.between(sp_defense_slider[0], sp_defense_slider[1])) &
                    (df.stat_speed_effort.between(speed_slider[0], speed_slider[1]))
                )
                df = df[condition]

        checked = st.checkbox('Filter by total effort values')

        if checked:
            total_slider = st.slider('Total', 0, 4, (0,4))
            condition = (df.effort_total.between(total_slider[0], total_slider[1]))
            df = df[condition]


'---'

st.markdown(f'#### Data')

f'Number of results: {df.shape[0]} rows'
'\n'

st.dataframe(
    df, 
    hide_index=True
)