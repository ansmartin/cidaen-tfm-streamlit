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
        
        checked = st.checkbox('Filter by type')

        if checked:
            options = ['Specify type position', 'Any type position'] #'Don\'t filter by type'

            option = st.selectbox(
                #'Filter by type:',
                '',
                options
            )

            #types_list.append(None)

            with st.container(border=True):
                if option==options[0]:
                    with st.container():
                        first_types_selected = st.multiselect("First type", types_list)
                    with st.container():
                        second_types_selected = st.multiselect("Second type", types_list)

                    if len(first_types_selected)==0:
                        df = df[df.second_type.isin(second_types_selected)]
                    elif len(second_types_selected)==0:
                        df = df[df.first_type.isin(first_types_selected)]
                    else:
                        df = df[(df.first_type.isin(first_types_selected)) & (df.second_type.isin(second_types_selected))]

                elif option==options[1]:
                    types_container = st.container()
                    with types_container:
                        types_selected = st.multiselect("Type", types_list)
                        df = df[(df.first_type.isin(types_selected)) | (df.second_type.isin(types_selected))]

    with st.container(border=True):
        gens_selected = st.multiselect("Pokémon species generation", gens_list)
        if len(gens_selected)>0:
            df = df[df.species_generation_number.isin(gens_selected)]
            
        gens_selected = st.multiselect("Pokémon form generation", gens_list)
        if len(gens_selected)>0:
            df = df[df.form_generation_number.isin(gens_selected)]
            
    with st.container(border=True):
        games_selected = st.multiselect("Game version", games_list)
        if len(games_selected)>0:
            df = df[df.version_group_name.isin(games_selected)]

with col2:
    with st.container(border=True):
        # forms = ['Default', 'Mega', 'GMax', 'Regional']

        # with st.container():
        #     forms_selected = st.multiselect("Forms", forms, default=forms)

        # for x in forms_selected:
        #     if x==forms[0]:
        #         df = df[df.is_default]
        #     elif x==forms[1]:
        #         df = df[df.is_mega]
        #     elif x==forms[2]:
        #         df = df[df.is_gmax]
        #     elif x==forms[3]:
        #         df = df[df.is_regional]
                

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
        if baby:
            df = df[df.is_baby]
        if legendary:
            df = df[df.is_legendary]
        if mythical:
            df = df[df.is_mythical]


with col3:
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
        colors_selected = st.multiselect("Color", colors_list)
        if len(colors_selected)>0:
            df = df[df.color_name.isin(colors_selected)]

with col4:
    with st.container(border=True):
        checked = st.checkbox('Filter by base stats')

        if checked:
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

    with st.container(border=True):
        checked = st.checkbox('Filter by total base stats')

        if checked:
            total_slider = st.slider('Total', 0, 1530, (0,1530))
            condition = (df.stats_total.between(total_slider[0], total_slider[1]))
            df = df[condition]

#df.first_type = df.first_type.apply(lambda x: f'./images/types/{x}.png')
#df.second_type = df.second_type.apply(lambda x: f'./images/types/{x}.png')

'---'
st.markdown(f'#### Data')

f'Number of results: {df.shape[0]} rows'
'\n'

st.dataframe(
    df, 
    # column_config={
    #     'first_type' : st.column_config.ImageColumn(),
    #     'second_type' : st.column_config.ImageColumn(),
    # },
    hide_index=True
)