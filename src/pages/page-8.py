#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback
import dash_daq as daq
import datetime
from flask import request
import re
import pandas as pd

#Zipcode section
df_zipcodes = pd.read_csv('Zipcodes_dereplicate.csv')
risk_dict = dict(zip(df_zipcodes['POSTALCODE'], df_zipcodes['RISK']))

#Keys tab
mykeys = [
  "consent",
  "zipcode",
  "which_residence",
  "previous_completion",
  "live_alone",
  "live_with_child_0_4",
  "live_with_child_5_14",
  "live_with_child_15_18",
  "live_with_someone_over_18",
  "dog",
  "cat",
  "horse",
  "anti_tick_treatment_dog",
  "vaccination_treatment_dog",
  "anti_tick_treatment_cat",
  "house_proximity_wooded_area",
  "access_courtyard",
  "house_deer",
  "courtyard_herbaceous_or_forest",
  "courtyard_children_play_area",
  "courtyard_fences_deer",
  "courtyard_corridor",
  "courtyard_mowing",
  "courtyard_fallen_leaves",
  "courtyard_clearing_herbaceous",
  "time_daily_wooded_area",
  "frequency_outdoor_activities",
  "visite_area_disease_ticks",
  "search_for_informations_ticks",
  "Wearing_long_layers_of_clothing",
  "Wearing_light-coloured_clothing",
  "Tucking_in_clothes",
  "DEET",
  "Walking_on_cleared_paths",
  "Examining_your_clothes",
  "clothes_in_the_dryer",
  "Examining_yourself",
  "Bathing_or_showering",
  "attached_to_your_skin",
  "Freely_moving",
  "On_a_pet",
  "Freely_moving_outside",
  "How_many_embedded_in_your_skin",
  "How_many_freely_moving_on_your_skin",
  "How_many_on_a_pet",
  "confidence_prevent_tick_bite",
  "confidence_young_tick",
  "confidence_adult_tick",
  "safely_remove_a_tick",
  "Age",
  "Education",
  "Employment_status",
  "Income",
  "primary_language",
  "population_group",
  "commentaries"
]
    

dash.register_page(__name__, path='/page-8')



layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
        html.B('Your personalized report', style={'font-size': '60px'})
    ], style={'text-align': 'center'}),
    html.Br(),
    
    # Section for the first gauge
    html.Br(),
    
    html.Div([
        html.P('Potential for BLT in environment', style={'font-size' : '25px', "font-weight": "bold"}),
        html.P('Risk of exposure', style={'font-size' : '25px', "font-weight": "bold"}),
        html.P('Level of preventive behaviours', style={'font-size' : '25px', "font-weight": "bold"})
    ], style={
        # Flexbox styling to arrange gauges horizontally
        'display': 'flex',
        'justify-content': 'space-evenly',   # Evenly distribute space between gauges
        'align-items': 'center',           # Align gauges vertically in the center
        'margin-top': '20px'
    }),
    # Flexbox container for all three gauges
    html.Div([
        daq.Gauge(
            color={"gradient": False, "ranges": {"grey": [0, 0.1], "limegreen": [0.1, 1], "orange": [1, 2], "red": [2, 3]}},
            scale={
                "custom": {0.6: {"label": "Low", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                           1.5: {"label": "Moderate", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                           2.4: {"label": "High", 'style': {'fontSize': 20, 'fontWeight': 'bold'}}
                }
            },
            max=3,
            min=0,
            label='',
            value=0.05,
            showCurrentValue=False,
            units='',
            id='gauge1'
        ),
        daq.Gauge(
            color={"gradient": False, "ranges": {"grey": [0, 0.1], "limegreen": [0.1, 1], "orange": [1, 2], "red": [2, 3]}},
            scale={
                "custom": {0.6: {"label": "Low", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                           1.5: {"label": "Moderate", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                           2.4: {"label": "High", 'style': {'fontSize': 20, 'fontWeight': 'bold'}}
                }
            },
            max=3,
            min=0,
            label='',
            value=0.05,
            showCurrentValue=False,
            units='',
            id='gauge2'
        ),
        daq.Gauge(
            color={"gradient": False, "ranges": {"grey": [0, 0.1], "red": [0.1, 1], "orange": [1, 2], "limegreen": [2, 3]}},
            scale={
                "custom": {0.6: {"label": "Low", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                           1.5: {"label": "Moderate", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                           2.4: {"label": "High", 'style': {'fontSize': 20, 'fontWeight': 'bold'}}
                }
            },
            max=3,
            min=0,
            label='',
            value=0.05,
            showCurrentValue=False,
            units='',
            id='gauge3'
        )
    ], style={
        'display': 'flex',
        'justify-content': 'space-evenly',   
        'align-items': 'center',           
        'margin-top': '20px'
    }),
    
    #html.Hr(className='grey_blue_line'),
    html.Br(),
    html.Br(),
    html.Div(id='text_report', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap', 'text-align': 'justify', 'marginLeft': '50px', 'marginRight': '50px'}),
    # Print button and other elements
    # html.Button('Print to PDF', id='print-button'),
    # html.Br(),
    # html.Br(),
    #html.Div(id='display-answers_p8', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
    
])
        
        
# CALLBACKS


@callback(
    [Output(component_id='gauge1', component_property='value'),
    Output(component_id='gauge2', component_property='value'),
    Output(component_id='gauge3', component_property='value')],
    Input('record_answers','data')
)

def calculat_score_and_record_answers(data):
    ######
    #Enregistrement des données en cas de consentement
    ######
    if data and data.get('consent') == 'yes':
        now = datetime.datetime.now()
        ip_address = request.remote_addr
        myline = str(ip_address) + '\t' + now.strftime('%Y-%m-%d %H:%M:%S') 
        for k in mykeys:
            if k in data.keys():
                myline += '\t' + str(data[k])
            else:
                myline += '\t\t'
            
        myline += '\n'
        unique_output = re.sub(r'[^a-zA-Z0-9]', '_', now.strftime('%Y-%m-%d %H:%M:%S'))
        filename = 'survey_results_' +  unique_output + '.tsv'
        with open(filename, 'a') as tsvfile:
            tsvfile.write(myline)
    ######
    ######
    # Risk Calculation based on zipcode
    #zipcode = data['zipcode']
    risk = risk_dict.get(data['zipcode'], 'Unknown')
    ######
    ######
    # Evaluation score1 BLT in environment
    ######
    score1 = 0
    if data and 'zipcode' in data:
        if risk == 'High':
            score1 = 2.5
        elif risk == 'Medium':
            if data['How_many_embedded_in_your_skin'] != "Not applicable" \
                and data['How_many_embedded_in_your_skin'] != "I don't remember" \
                    and data['How_many_embedded_in_your_skin'] != "0" \
                        and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
                            and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
                                and data['How_many_freely_moving_on_your_skin'] != "0":
                            score1 = 2.5
            else:
                if data['access_courtyard'] == "Yes" :
                    if(data['courtyard_herbaceous_or_forest'] == 'Yes'):
                        score1 = 2.5
                    else:
                        if data['house_deer'] == "Yes":
                            score1 = 2.5
                        else:
                            if data['house_proximity_wooded_area'] == "Yes":
                                score1 = 2.5
                            else :
                                score1 = 1.5
                else:
                    if data['house_proximity_wooded_area'] == "Yes":
                        score1 = 2.5
                    else:
                        score1 = 1.5
        elif risk == 'Low':
            if ( (data['How_many_embedded_in_your_skin'] != "Not applicable") \
                and (data['How_many_embedded_in_your_skin'] != "I don't remember") \
                    and (data['How_many_embedded_in_your_skin'] != "0")):
                score1 = 1.5
            else:
                if data['access_courtyard'] == "Yes" :
                    if data['house_deer'] == "Yes":
                        score1 = 1.5
                    else:
                        if data['house_proximity_wooded_area'] == "Yes":
                            score1 = 1.5
        #elif risk not found !
    ######
    # Risk of exposure
    #######       
    score2 = 0
    # optimiser avec x not in list
    if data['How_many_embedded_in_your_skin'] != "Not applicable" \
        and data['How_many_embedded_in_your_skin'] != "I don't remember" \
            and data['How_many_embedded_in_your_skin'] != "0"\
                and data['How_many_freely_moving_on_your_skin'] != "Not applicable" \
                    and data['How_many_freely_moving_on_your_skin'] != "I don't remember" \
                        and data['How_many_freely_moving_on_your_skin'] != "0":
                    score2 = 2.5
    else:
        if data['frequency_outdoor_activities'] == 'Very often (More than 10 times a year)':
            score2 = 2.5
        else:
            if ( data['time_daily_wooded_area'] == 'Between one and five hours per day' ) or (  data['time_daily_wooded_area'] == 'More than five hours per day' ):
                score2 = 2.5
            else:
                if data['frequency_outdoor_activities'] == 'Rarely':
                    score2 = 1.5
                else:
                    if data['time_daily_wooded_area'] in {'Never', 'Less than one hour per day'}:
                        score2 =1.5
    ######
    # Preventive behavior
    #######
    score3 = 0
    ###
    # Constructuion d'une table de reponses considérées comme oui
    considered_as_yes = ['Most of the time', 'Always', 'Not applicable to my situation']
    # Calcul du score de mesures de protection
    score_at_least_4_protective_behaviours = 0
    if data['search_for_informations_ticks'] == 'yes' :
        score_at_least_4_protective_behaviours += 1
    if data['Wearing_long_layers_of_clothing'] in considered_as_yes :
        score_at_least_4_protective_behaviours += 1
    if data['Wearing_light-coloured_clothing'] in considered_as_yes :
        score_at_least_4_protective_behaviours += 1
    if data['Tucking_in_clothes'] in considered_as_yes :
        score_at_least_4_protective_behaviours += 1
    if data['DEET'] in considered_as_yes :
        score_at_least_4_protective_behaviours += 1
    if data['Walking_on_cleared_paths'] in considered_as_yes :
        score_at_least_4_protective_behaviours += 1
    if data['Examining_your_clothes'] in considered_as_yes :
        score_at_least_4_protective_behaviours += 1
    if data['clothes_in_the_dryer'] in considered_as_yes :
        score_at_least_4_protective_behaviours += 1
    if data['Bathing_or_showering'] in considered_as_yes :
        score_at_least_4_protective_behaviours += 1
    ######
    ######
    if (risk == 'High') or (risk == 'Medium') or (data['visite_area_disease_ticks'] == 'Yes') : 
        if data['Examining_yourself'] == 'Yes':
            if (risk == 'Medium') or (risk == 'High'):
                if data['access_courtyard'] == 'Yes':
                    if data['courtyard_mowing'] in considered_as_yes:
                        if data['courtyard_fallen_leaves'] in considered_as_yes:
                            if data['courtyard_clearing_herbaceous'] in considered_as_yes:
                                if data['courtyard_clearing_herbaceous'] in considered_as_yes:
                                    if data['courtyard_fences_deer'] in considered_as_yes:
                                        if score_at_least_4_protective_behaviours >= 4 :
                                            score3 = 2.5
                                        else :
                                            score3  = 1.5
                                    else :
                                        if score_at_least_4_protective_behaviours >= 4 :
                                            score3 = 1.5
                                        else:
                                            score3 = 0.5
                            else :
                                if score_at_least_4_protective_behaviours >= 4 :
                                    score3 = 1.5
                                else :
                                    score3 = 0.5
                        else :
                            score3 = 0.5
                    else :
                        score3 = 0.5
                else:
                    if score_at_least_4_protective_behaviours >= 4:
                        score3 = 2.5
                    else :
                        score3 = 1.5
            else :
                if score_at_least_4_protective_behaviours >= 4:
                    score3 = 2.5  
                else :
                    score3 = 1.5
        else :
            score3 = 0.5
    ######
    ######
    ######
    ######
    return score1, score2, score3


######
# Adaptated text report
######

@callback(
    Output('text_report', 'children'),
    Input('record_answers', 'data')
    )

def display_personalized_text(data):
    
    risk = risk_dict.get(data['zipcode'], 'Unknown')
    no_anti_ticks = ['no', 'yes', "I don't remember"]
    
    
    
    
    
    ###############################################################################
    # 1 The potential of blacklegged ticks in your environment
    ###############################################################################
    
    
    sentence = "### The potential of blacklegged ticks in your environment\n\n"
    
    #Postal Code & residency feedback
    if data['which_residence'] == 'Primary' or data['which_residence'] == 'Secondary':
        sentence += f"""* The region of your {data['which_residence']} residence has a **{risk}** level risk"""
    else :
        sentence += f"""* The region of your residence has a **{risk}** level risk"""
    
    sentence += '\n\n'
    
    #Blacklegged ticks on your property and property management
    sentence += "* Evidence suggests that most tick exposure occurs in the peri-domestic environment, rather than further afield. While it is not possible to determine your exact level of risk for blacklegged ticks based on a questionnaire, the presence of certain features on or near your property can provide an indication of risk, based on evidence reported in the scientific literature.\n\n"
    
    # Herbaceous or wooded area in proximity
    if data['house_proximity_wooded_area'] not in no_anti_ticks:
        sentence += "* You reported having **herbaceous or wooded areas or edges on your property, and/or living near a wooded area**. The presence of herbaceous, wooded areas, and the intersection of these two habitats have been shown to be associated with an increase in diseases spread by ticks. This does not mean that you cannot spend time outdoors, but rather that **you should be vigilant and take steps to protect yourself**. There are several ways you can reduce the risk of exposure to ticks on your property - for more information, check [What can I do to reduce ticks in my yard?] (https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/). Remember to protect yourself while making modification to your property by **wearing long clothes and applying bug repellent, and to perform a tick check and take a bath or shower afterwards**.\n"
    
    # Courtyard feedback
    if data['access_courtyard']== 'yes':
        sentence += "* You reported **having a courtyard, garden, or wooded area**. While having an outdoor space does not automatically mean you are at risk of tick exposure, there are certain elements which are known to increase your risk of tick bite and/or diseases spread by ticks. These include: The **size of your yard, Certain types of cover, such as flower or vegetable gardens and herbaceous and wooded areas**.The **presence of a wood pile, the presence of a stone wall, the presence of leaf litter Activity areas such as children’s play areas, dining areas, and sitting areas**.\n"
    
    #children's play equipment
    if data['courtyard_children_play_area'] == 'yes':
        sentence += "* You reported **having children’s play equipment or an activity structure on your property**. It is a good idea to **move this type of equipment closer to the house, and away from long grass or herbaceous/wooded areas**. It is **preferable to have wood chips rather than grass in this area, or to keep the grass very short**.\n\n"
    
    
    #deer on your property
    if data['house_deer'] == 'yes':
        sentence += "* You reported **seeing or suspecting deer on your property**. Deer are a host species for the blacklegged tick, meaning they play an important role in the life cycle of the tick. Research suggests that not having a fence to exclude deer is associated with an increased risk of tick bites, and that the presence of deer is associated with an increased risk for people getting a disease spread by ticks. While it may not be feasible to install fencing around the entirety of your property, you could consider fencing off an area of the property that you use regularly. Doing this will also prevent deer from eating your plants and provides a safe space for pets to run. There are several ways you can reduce the risk of exposure to ticks on your property, such as installing fences and creating a mulch or gravel border around your yard. For more information, check [What can I do to reduce ticks in my yard?] (https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/). Remember to protect yourself while working on your property by wearing long clothes and applying bug repellent, and to perform a tick check and take a bath or shower afterwards.\n\n"
   
    sentence += '\n\n\n\n'
   
   
    ###############################################################################
    # 2 Your risk of exposure to ticks
    ###############################################################################
    
    
    sentence += "### Your risk of exposure to ticks\n\n"
    
    #Your tick exposure in the last 12 months
    #sentence += "### Your tick exposure in the last 12 months\n\n"
    
    if (data['attached_to_your_skin'] != 'Never' and  data['attached_to_your_skin'] != 'Not applicable') or (data['Freely_moving'] != 'Never' and  data['Freely_moving'] != 'Not applicable'):
        sentence += "* You reported having found a tick on yourself in the last 12 months. For this reason, you have been given a ‘high’ risk level for tick exposure.\n\n"
    
    if data['On_a_pet'] != 'Never' and  data['On_a_pet'] != 'Not applicable':
        sentence += "* You reported having found a tick on your pet in the last 12 months. For this reason, you have been given a ‘high’ risk level for tick exposure, as pet exposure to ticks usually suggests that their owners have also been in at at-risk habitat.\n\n"
    
    if data['Freely_moving_outside'] != 'Never' and  data['Freely_moving_outside'] != 'Not applicable':
        sentence += "* You reported having found a tick in your environment in the last 12 months. For this reason, you have been given a ‘high’ risk level for tick exposure as this suggests you spend time in or near tick habitats.\n\n"
    
    # Pas compris "For Section 4 : 'Your prior exposure'
    #À refaire
    
    #outdoor activity
    
    if data['time_daily_wooded_area'] == 'More than five hours per day':
        sentence += "* You reported engaging in at least one outdoor activity which occurs in potential tick habitats, at least once or twice a season. Outdoor recreation in general can be associated with increased tick bites and risk of disease spread by ticks, and increased time spent in vegetation can also increase the risk of diseases spread by ticks. Previous research studies have found associations between specific activities such as hiking, hunting, and yard work and an increased risk of contracting a disease transmitted by ticks. However, it is prudent to assume that there can be a risk of tick exposure when participating in any outdoor activity occurring in grassy, wooded, or herbaceous areas. While there is no need to stop doing these activities – it is important to protect yourself, your family, and your pets from tick bites, and to always perform tick checks! \n\n"
    elif data['time_daily_wooded_area'] == 'Between one and five hours per day':
        sentence += "* As with engaging in outdoor activities, occupational exposure to ticks has been associated with an increased risk of diseases spread by ticks, therefore it is important for you to adopt consistent and regular prevention measures. Depending on the bug repellent you choose to use and how long you are outdoors in one day, you may need to reapply the repellent while you are outside, so take it with you and/or leave one in the car. It is also a good idea to stop and perform tick checks throughout the day, rather than waiting until the end of the day.\n\n"
    
    if data['time_daily_wooded_area'] == 'More than five hours per day' or data['time_daily_wooded_area'] == 'Between one and five hours per day':
        sentence += "* If you frequently work or spend time in potential tick habitats, you may wish to invest in clothing which has been treated with permethrin as an additional layer of protection. For more information on how to protect yourself from ticks when outdoors, check [Everything you need to know about prevention] (https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n\n"
    
    no_in_prior_tick_exposure = ['Never','Not applicable']
    
    if (data['time_daily_wooded_area'] == 'Never' or data['time_daily_wooded_area'] == 'Less than one hour per day') \
        and (data['attached_to_your_skin'] in no_in_prior_tick_exposure ) \
            and (data['Freely_moving'] in no_in_prior_tick_exposure ) \
                and (data['On_a_pet'] in no_in_prior_tick_exposure) \
                    and (data['Freely_moving_outside'] in no_in_prior_tick_exposure) :
                        sentence += "* You reported spending little time either recreating or working outdoors, meaning you are less likely to enter tick habitats. However, note that is a low risk of encountering a tick anywhere in Canada south of the Arctic circle due to the possibility of ticks being dispersed by birds outside of their usual habitats.\n\n"
    
    if (data['time_daily_wooded_area'] == 'Never' or data['time_daily_wooded_area'] == 'Less than one hour per day') \
        and ( (data['attached_to_your_skin'] not in no_in_prior_tick_exposure ) \
            or (data['Freely_moving'] not in no_in_prior_tick_exposure ) \
                or (data['On_a_pet'] not in no_in_prior_tick_exposure) \
                    or (data['Freely_moving_outside'] not in no_in_prior_tick_exposure) ):
                        sentence += "* You reported having found a tick before, despite spending little time recreating or working outdoors. This may be because your activities bring you into proximity with tick habitats or that you encountered a tick outside of its usual habitat. Regardless of why, it will be important to remain vigilant and to perform tick checks.\n\n"

    sentence += '\n\n\n\n'



    
    ###############################################################################
    # 3 Your preventive behaviours
    ###############################################################################
    
    
    #Individual preventive behavioursà
       
    
    sentence += "### Individual preventive behaviours\n\n"
    
    if risk == 'Low':
        sentence += "*This is the risk level you would be given if you lived in or visited a Lyme disease risk area, or if Lyme diseases emerges in your current region.*\n\n"
        
    sentence += "Research has demonstrated the association between increased risk of diseases spread by ticks and the lack of adopting protective measures, including not performing a tick check, not using bug repellent, not wearing appropriate clothing, and not bathing after spending time outdoors. Each behaviour provides an additional layer of protection, and there is no single behaviour which is guaranteed to prevent tick bites or disease. Therefore, it is recommended that you adopt as many preventive behaviours as is possible and feasible for you and your family.\n\n"
    
    no_body_check = ['Never','Rarely', 'Sometimes']
    if data['Examining_yourself'] in no_body_check:
        sentence += "* You reported that you never, rarely, or sometimes perform a body check for ticks after being in a wooded area in a Lyme disease endemic region, which is why you have received a ‘Low’ score for your preventive behaviours.\n\n"
    
    if data['Examining_yourself'] in no_body_check or data['Examining_yourself'] == 'Not applicable':
        sentence += "* While no single behaviour has consistently been demonstrated to be the most effective, performing a thorough tick check is the most widely recommended method of protection. It does not require special equipment - although a full-length and hand-held mirror can help – it just takes time. By planning ahead and scheduling 10 minutes for a tick check after spending time outdoors, you can make it more likely that you will do so, and thereby reduce your chance of a tick bite or getting a disease spread by ticks. And don’t forget to check other household members and pets too! If you find a tick, congratulate yourself on doing so, remove it and continue your tick check in case there are more\n\n"
    else :
        sentence += "* You reported that you perform a body check for ticks most of the time after being in a wooded area in a Lyme disease endemic region – well done! While no single behaviour has consistently been demonstrated to be the most effective, performing a tick check is the most widely recommended method of protection you can adopt. It does not require special equipment - although a full-length and hand-held mirror can help – it just takes time. By planning ahead and scheduling time for a tick check after spending time outdoors, you can make it more likely that you will do so, and thereby reduce your chance of a tick bite or getting a disease spread by ticks. And don’t forget to check other household members and pets too! If you find a tick, congratulate yourself on doing so, remove it and continue your tick check in case there are more.\n\n"
    
    
    #Q13 ????????
    
    # Living alone or live with someone feedback
    if data['live_alone'] == 'yes' :
        sentence += """* Performing tick checks can be challenging for everyone, as ticks like to hide in places where they cannot be found. As you **live alone**, it can be very useful to have both a **full-length mirror** as well as a **handheld mirror** to make this process easier.Some people find that having a **lint roller** available can help to reach ticks which have not attached, and similarly, a **loofah in the shower** can help to dislodge ticks from places you cannot reach. Remember to pay particular attention to your **scalp, hairline, ears, arms, chest, back, waist, belly button, groin, legs and behind knees, and between the toes**.\n\n  In 2021, 45% of Lyme disease cases in Canada were diagnosed in adults aged 55-79 years. This does not mean that people in this age group cannot spend time outdoors, but rather suggests that this age group should **adopt consistent behaviours** to protect themselves from ticks.\n\n  For more information on how to protect yourself, check [Everything you need to know about prevention] (https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n"""
    elif data['live_with_someone_over_18'] == 'yes' :
        sentence += """* As you **live with another adult**, you can **remind each other to adopt preventive behaviours** against tick bites and **help each other to perform a tick check** – particularly the hard-to-reach places such as the **scalp and back**. By helping and reminding each other to think about ticks, it will be **easier to incorporate these practices into your routine**.**If performing a tick check alone**, it can be very useful to have both a **full-length mirror** as well as a **handheld mirror** to make this process easier. Some people find that having a **lint roller** available can also be helpful to reach ticks which have not attached, and similarly, a **loofah in the shower** can help to dislodge ticks from places you cannot reach.\n\n  In 2021, 45% of Lyme disease cases in Canada were diagnosed in adults aged 55-79 years. This does not mean that people in this age group cannot spend time outdoors, but rather suggests that this age group should try to adopt consistent behaviours to protect themselves from ticks.\n\n  For more information on how to protect yourself, check [Everything you need to know about prevention] (https://ticktool.etick.ca/all-you-need-to-know-about-ticks/)\n"""
    elif data['live_with_child_0_4'] == 'yes' or data['live_with_child_5_14'] == 'yes' or data['live_with_child_15_18'] == 'yes':
        sentence += """* Approximately **11% of Lyme disease cases reported in Canada in 2021 were in children aged 5-14 years**, however other evidence suggests that the risk of tick bites is **higher in children aged 5 years or less**. This can be attributed to the fact that children this age **often play low to the ground and leave designated trails**. They are also **less likely to check themselves** for ticks. This does **not** mean that older children cannot develop a tick-borne disease, and it is important for all members of the family to learn how to protect themselves from ticks. As with adults, the risk can be reduced by performing a **tick check, wearing long clothes, tucking in clothes, wearing bug repellent if over 6 months of age, and bathing or showering after spending time outdoors**.\n  For more information on how to protect children from ticks bites, check [How can I protect my children?] (https://ticktool.etick.ca/how-can-i-protect-my-children/)’.\n"""
    
    #Lawn management practice
    sentence += "\n\nThere are several ways to reduce the risk of tick exposure of your property. Here, we will describe three key methods:\n\n"
    
    yes_property_management = ['Most of the time', 'Always']
    
    #Mowing
    if data['courtyard_mowing'] in yes_property_management:
        sentence += "* Well done for regularly maintaining the lawn! Keeping the grass short is very important in reducing the risk of tick exposure. Ticks climb up long grass so they can attach to people and animals who brush past. By regularly and consistently keeping the grass short – especially in areas which you or your pets access – you are making your property less hospitable for ticks.\n\n"
    else:
        sentence += "* Lawn maintenance is very important in reducing the risk of tick exposure. Ticks climb up long grass so they can attach to people and animals who brush past. By regularly and consistently keeping the grass short – especially in areas which you or your pets access – you can make your property less hospitable for ticks.\n\n"
    
    #Removing leaves
    if data['courtyard_fallen_leaves'] in yes_property_management:
        sentence += "* Well done for regularly removing leaves on your property! Leaf litter provides a safe environment for ticks, keeping them warm in the winter and preventing them from drying out in the summer. By removing leaf litter, you are reducing one of the most important habitats for ticks in your property. Depending on the size of you property, you may wish to focus on the areas you or your pets like to spend time in.n\n"
    else:
        sentence += "* Leaf litter provides a safe environment for ticks, keeping them warm in the winter and preventing them from drying out in the summer. By removing leaf litter, you can reduce one of the most important habitats for ticks in your property. Depending on the size of you property, you may wish to focus on the areas you or your pets like to spend time in.\n\n"
    
    #Brush and branches
    if data['courtyard_clearing_herbaceous'] in yes_property_management:
        sentence += "* Well done for regularly clearing herbaceous brush and trimming branches! These habitats provide a suitable environment for small rodents, which not only carry ticks but are vital in the life cycle of the bacteria which cause Lyme disease and other diseases spread by ticks. By removing herbaceous areas in the areas where you or your pets spend a lot of time, you are making these areas less hospitable for mice and ticks, reducing the chance of them venturing close to your house.\n\n"
    else :
        sentence += "* Herbaceous brush and long branches provide a suitable environment for small rodents, which not only carry ticks but are vital in the life cycle of the bacteria which cause Lyme disease and other diseases spread by ticks. By removing herbaceous areas in the areas where you or your pets spend a lot of time, you can make these areas less hospitable for mice and ticks, reducing the chance of them venturing close to your house.\n\n"
    
    sentence += "Bear in mind that yard work, time spent in vegetation and general outdoor activity can increase your risk of getting a disease spread by ticks, so remember to protect yourself while working on your property by wearing long clothes and applying bug repellent, and to perform a tick check and take a bath or shower afterwards. Many people are concerned outdoor measures to reduce the risk of tick exposure may have negative environmental consequence. To learn more about this and other FAQs, check ‘[What can I do to reduce ticks in my yard?] (https://ticktool.etick.ca/what-can-i-do-to-reduce-ticks-in-my-yard/).\n\n"
    
    sentence += "\n\n\n\n"
    
    
    ###############################################################################
    # 4 Prior tick exposure ??????
    ###############################################################################
    
    ###############################################################################
    # 5 A note about pets
    ###############################################################################
    
    sentence += "### A note about pets\n\n"
    
    #Dog anti-tick treatnment
    if data['anti_tick_treatment_dog'] in no_anti_ticks :
        sentence += "* You reported **taking care of at least one dog**. Dogs are at risk for tick bites, and **just like people, can suffer from Lyme disease** and other diseases transmitted by ticks.  Fortunately, there are several species-specific products available for pets to protect them from ticks and Lyme disease, including **tablets, spot-on treatments, and vaccines**. Some of these products can also protect your pet from other parasites such as **fleas and worms**. Your veterinarian is the best person to advise you on these so you can choose what is right for you and your situation. Ticks are **active above 4°C/ 39°F**, so depending on where you live, tick prevention may be recommended for your dog **all year round**. There is no evidence to suggest that having a dog increases your risk of getting a disease spread by ticks. However, **people who have dogs may spend more time outdoors** in tick habitats, so it is important for you to protect yourself from ticks.\n\n"
    elif data['anti_tick_treatment_dog'] == 'yes':
        sentence += "* You reported **taking care of at least one dog and providing them with anti-tick products** – well done! Dogs are at risk for tick bites, and **just like people, can suffer from Lyme disease** and other diseases transmitted by ticks. By administering a tick preventive product, you are helping to keeping them safe. There are several species-specific products available for pets to protect them from ticks and Lyme disease, including **tablets, spot-on treatments, and vaccines**. Some of these products can also protect your pet from other parasites such as **fleas and worms**. Your veterinarian is the best person to advise you on these so you can choose what is right for you and your situation. Ticks are **active above 4°C/ 39°F**, so depending on where you live, tick prevention may be recommended for your dog **all year round**. There is no evidence to suggest that having a dog increases your risk of getting a disease spread by ticks. However, **people who have dogs may spend more time outdoors** in tick habitats, so it is important for you to protect yourself from ticks.\n\n"
    
    #Cats anti-tick treatments 
    if data['anti_tick_treatment_cat'] in no_anti_ticks :
        sentence += "* You reported **taking care of at least one cat**. Cats are at risk for tick bites, so it is important to protect them with species-specific tick preventive products. By administering a tick preventive product, you are helping to keeping them safe. There are several species-specific products available for pets to protect them from ticks, including **tablets and spot-on treatments**. Some of these products can also protect your pet from other parasites such as **fleas and worms**. Your veterinarian is the best person to advise you on these so you can choose what is right for you and your situation. Ticks are **active above 4°C/ 39°F**, so depending on where you live, tick prevention may be recommended for your cat **all year round**. Interestingly, **cat ownership has been associated with an increased risk of diseases spread by ticks**, whereas this has not been found with dog ownership.  This may be due to differences in preventive behaviours between cat and dog owners, differences in administration of tick preventive products, reduced tick checks in cats, increased grooming behaviour in cats or because cats are **more likely to roam in long grass**. Regardless of why this association has been found, **applying tick preventive products to your cat, and checking them for ticks is always recommended**.\n\n"
    elif  data['anti_tick_treatment_cat'] == 'yes':
        sentence += "* You reported taking care of at least one cat and providing them with anti-tick products – well done!  Cats are at risk for tick bites, so it is important to protect them with species-specific tick preventive products. There are several species-specific products available for pets to protect them from ticks, including **tablets and spot-on treatments**. Some of these products can also protect your pet from other parasites such as **fleas and worms**. Your veterinarian is the best person to advise you on these so you can choose what is right for you and your situation. Ticks are **active above 4°C/ 39°F**, so depending on where you live, tick prevention may be recommended for your cat **all year round**.Interestingly, **cat ownership has been associated with an increased risk of diseases spread by ticks**, whereas this has not been found with dog ownership.  This may be due to differences in preventive behaviours between cat and dog owners, differences in administration of tick preventive products, reduced tick checks in cats, increased grooming behaviour in cats or because cats are **more likely to roam in long grass**. Regardless of why this association has been found, **applying tick preventive products to your cat, and checking them for ticks is always recommended**.\n\n"
    
    #Horse
    if data['horse'] == 'yes':
        sentence += "* **Horses can suffer from Lyme disease too**, and as there is **no vaccine licensed for horses**, tick prevention is important. **Grooming and checking for ticks daily, appropriate pasture management, and the use of species-specific bug repellents** can all help to reduce the risk of tick bites. For more information on diseases spread by ticks and tick bite prevention, speak to your veterinarian. Some studies have found that owning or riding horses has been associated with an increased risk of tick bites and disease spread by ticks. This is most likely due to riders and horses being in the same environment and having the same risk of tick exposure.\n"
    if data['dog'] == 'yes' or data['cat'] == 'yes' or data['horse'] == 'yes':
        sentence += "* Pets are **not able to transmit Lyme disease or other tick-borne diseases to humans. Having a pet has been associated with an increased risk of tick bites or disease spread by ticks. This is usually because having a pet means you spend more time outdoors and therefore closer to ticks**. It does not mean you should avoid having pets! If you see ticks on your pet, this suggests that you may also have been in a tick habitat and that you should take steps to protect both you, your pet(s), and your family.\n\n"
    
    sentence += "* For more information on pets and ticks, visit [How can I protect my pets?] (https://ticktool.etick.ca/how-can-i-protect-my-pets/)\n\n"
    
    
    ###############################################################################
    # 6 Gaining confidence with ticks\
    ###############################################################################
   
    
    sentence += "### Gaining confidence with ticks\n\n"
    sentence += "* Confidence in preventing tick bites will increase with the consistent implementation of tick preventive behaviours and experience. No method of tick bite prevention is 100% effective, and despite your best efforts, you may still find ticks on yourself, family members and pets. This does not mean you are doing something wrong!\n\n"
    sentence += "* Finding ticks is not always easy. Nymphs may be especially difficult to detect as they can be the size of a poppy seed. Again, practice and experience will help. If you are not physically able to detect a tick (e.g., due to poor eyesight or restricted movement), mirrors and a magnifying glass can make it easier, or if possible, asking someone to help.\n\n"
    sentence += "* Understandably, some people do not feel confident removing an attached tick. Common concerns include tick mouthparts being left in the skin or incorrect handling of the tick. For information on how to remove a tick and what not to do, check [TickTool] (https://ticktool.etick.ca/what-should-i-do-if-i-find-a-tick/).\n\n"
    
    ###############################################################################
    # 7 Conclusion
    ###############################################################################
    
    sentence += "### Conclusion\n\n"
    
    sentence += "* We hope this report is helpful to you and enables you to feel more prepared and confident when spending time outdoors. For more information on ticks and tick-borne diseases in Canada, you can consult the following resources: \n\n [Government of Canda] (https://www.canada.ca/en/public-health/services/diseases/ticks-tick-borne-diseases.html)\n\n [TickTool] (https://ticktool.etick.ca/)\n\n\n\n"
    
    sentence += "* To learn how your risk leves were calculated, please click here :  LINK TO A NEW WEBPAGE\n\n\n\n"
    
    
    return dcc.Markdown(sentence)
    


# Display data dictionnary for dev


    
# @callback(
#     Output('display-answers_p8', 'children'),
#     Input('record_answers', 'data')
# )

# def display_answers_p8(data):
#     if data:
#         return html.Pre(json.dumps(data, indent=2))
#     return "No data recorded yet."






