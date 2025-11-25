#!/usr/bin/env python
# coding: utf-8

# ## Helpers
# 
# null

# In[1]:


import ipywidgets as widgets
from IPython.display import HTML, display
import joblib
import numpy as np
import pandas as pd
import os

def create_gauge_html(title, value, color_hex, bg_color="#ffffff"):
    """Generates a smaller-height SVG Gauge for compact dashboard tiles."""
    percentage = max(0, min(100, value * 100))
    dash = (percentage / 100) * 158
    
    html = f"""
    <div style="
        background-color: {bg_color}; 
        border-radius: 10px; 
        padding: 6px 10px;
        box-shadow: 0 3px 5px rgba(0,0,0,0.08); 
        text-align: center; 
        font-family: sans-serif;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        border: 1px solid rgba(0,0,0,0.05);
    ">
        <h3 style="
            margin: 0 0 4px 0;
            color: #444; 
            font-size: 12px;
            text-transform: uppercase; 
            letter-spacing: .5px;
        ">
            {title}
        </h3>
        
        <svg viewBox="0 0 100 60" width="95px" height="55px">
            <path d="M 10 50 A 40 40 0 0 1 90 50"
                  fill="none"
                  stroke="rgba(0,0,0,0.1)"
                  stroke-width="7"
                  stroke-linecap="round"/>
            
            <path d="M 10 50 A 40 40 0 0 1 90 50"
                  fill="none"
                  stroke="{color_hex}"
                  stroke-width="7"
                  stroke-linecap="round"
                  stroke-dasharray="158"
                  stroke-dashoffset="{158 - dash}"
                  style="transition: stroke-dashoffset .9s ease-out;"/>
            
            <text x="50" y="44" 
                  text-anchor="middle" 
                  font-size="11" 
                  font-weight="bold" 
                  fill="#333">
                  {percentage:.1f}%
            </text>
        </svg>
    </div>
    """
    return html


def run_app(model_folder_path='./builtin/Models', model_name='urban_planning_models.pkl'):
    
    os.makedirs(model_folder_path, exist_ok=True)
    model_path = os.path.join(model_folder_path, model_name)
    

    label_style = "font-size: 14px; font-family: sans-serif; color: #2c3e50; margin-bottom: 5px; display: block;"
    layout_full = widgets.Layout(width='98%', margin='0 0 15px 0')
    
    app_state = {'models': None}

    theme = {
        'sustain': {'color': '#2ca02c', 'bg': '#e8f5e9'},
        'infra':   {'color': '#1f77b4', 'bg': '#e3f2fd'},
        'safety':  {'color': '#ff7f0e', 'bg': '#fff3e0'},
        'live':    {'color': '#9467bd', 'bg': '#f3e5f5'}
    }

    map_quality = {'Bad': 0.2, 'Average': 0.5, 'Good': 0.7, 'Excellent': 0.9}
    map_density = {'Low': 0.1, 'Medium': 0.4, 'High': 0.7, 'Very High': 1.0}
    map_yn = {'No': 0.0, 'Yes': 1.0}
    map_risk = {'Low': 0.2, 'Moderate': 0.5, 'High': 0.8}
    map_air = {'Good': 0.1, 'Moderate': 0.4, 'Unhealthy': 0.7, 'Hazardous': 0.9} 
    
    def make_label(text):
        return widgets.HTML(f"<div style='{label_style}'>{text}</div>")

    #Input Widgets

    l_zone = make_label("🏗️ <b>Zone Type</b>")
    w_zone = widgets.ToggleButtons(options=['Residential', 'Commercial', 'Industrial', 'Green Space'], value='Residential', style={'button_width':'auto'}, layout=layout_full)
    
    l_density = make_label("🏙️ <b>Building Density</b>")
    w_density = widgets.ToggleButtons(options=map_density.keys(), value='Medium', style={'button_width':'auto'}, layout=layout_full)
    
    l_road = make_label("🛣️ <b>Road Quality</b>")
    w_road = widgets.ToggleButtons(options=map_quality.keys(), value='Average', style={'button_width':'auto'}, layout=layout_full)
    
    l_transport = make_label("🚇 <b>Public Transport</b>")
    w_transport = widgets.ToggleButtons(options=map_quality.keys(), value='Average', style={'button_width':'auto'}, layout=layout_full)
    
    l_renewable = make_label("⚡ <b>Renewable Energy</b>")
    w_renewable = widgets.ToggleButtons(options=['No', 'Yes'], value='No', style={'button_width':'auto'}, layout=layout_full)
    
    l_green = make_label("🌲 <b>Green Cover</b>")
    w_green = widgets.ToggleButtons(options=map_quality.keys(), value='Average', style={'button_width':'auto'}, layout=layout_full)
    
    l_air = make_label("🌫️ <b>Air Quality</b>")
    w_air = widgets.ToggleButtons(options=map_air.keys(), value='Moderate', style={'button_width':'auto'}, layout=layout_full)
    
    l_crime = make_label("🛡️ <b>Crime Rate</b>")
    w_crime = widgets.ToggleButtons(options=['Low', 'Average', 'High'], value='Average', style={'button_width':'auto'}, layout=layout_full)
    
    l_income = make_label("💰 <b>Avg. Income Index</b>")
    w_income = widgets.FloatSlider(value=0.5, min=0.0, max=1.0, step=0.01, layout=layout_full, readout_format='.2f')
    
    l_risk = make_label("🌊 <b>Disaster Risk</b>")
    w_risk = widgets.ToggleButtons(options=map_risk.keys(), value='Moderate', style={'button_width':'auto'}, layout=layout_full)
    
    # Layout
    col1 = widgets.VBox([l_zone, w_zone, l_density, w_density, l_road, w_road, l_transport, w_transport, l_renewable, w_renewable], 
                        layout=widgets.Layout(width='48%', padding='10px'))
    
    col2 = widgets.VBox([l_green, w_green, l_air, w_air, l_crime, w_crime, l_income, w_income, l_risk, w_risk], 
                        layout=widgets.Layout(width='48%', padding='10px'))
    
    inputs_ui = widgets.HBox([col1, col2], layout=widgets.Layout(
        background_color='white', 
        padding='20px', 
        margin='0 0 20px 0', 
        border='1px solid #eee',
        border_radius='8px',
        box_shadow='0 2px 4px rgba(0,0,0,0.05)'
    ))
    
    #Output Widgets
    out_sustain = widgets.HTML(create_gauge_html("Sustainability", 0, theme['sustain']['color'], theme['sustain']['bg']))
    out_infra = widgets.HTML(create_gauge_html("Infrastructure", 0, theme['infra']['color'], theme['infra']['bg']))
    out_safety = widgets.HTML(create_gauge_html("Safety", 0, theme['safety']['color'], theme['safety']['bg']))
    out_live = widgets.HTML(create_gauge_html("Livability", 0, theme['live']['color'], theme['live']['bg']))
    
    grid = widgets.GridBox([out_sustain, out_infra, out_safety, out_live], layout=widgets.Layout(grid_template_columns="1fr 1fr", grid_gap="15px", margin="20px 0"))
    
    btn_predict = widgets.Button(description="PREDICT SCORE", button_style='primary', layout=widgets.Layout(width='100%', height='50px', margin='10px 0'))
    btn_predict.style.font_weight = 'bold'
    
    # UI Loading
    load_header = widgets.HTML(f"<h3>⚠️ Model Not Found</h3><p>Could not find <b>{model_name}</b> in <b>{model_folder_path}</b>.<br>Please upload the .pkl file to continue.</p>")
    uploader = widgets.FileUpload(accept='.pkl', multiple=False, description='Upload Model')
    load_status = widgets.Label(value="")
    load_container = widgets.VBox([load_header, uploader, load_status], layout=widgets.Layout(align_items='center', padding='30px'))
    
    dashboard_container = widgets.VBox([inputs_ui, btn_predict, grid])
    
    # Logic
    def load_model_from_file(filepath):
        try:
            loaded = joblib.load(filepath)
            required_keys = ['Sustainability', 'Infrastructure', 'Safety', 'Livability']
            if isinstance(loaded, dict) and all(k in loaded for k in required_keys):
                app_state['models'] = loaded
                return True, "Model loaded successfully!"
            else:
                return False, "Invalid model format. Missing required keys."
        except Exception as e:
            return False, f"Error loading model: {str(e)}"

    def on_upload_change(change):
        if not change['new']: return
        load_status.value = "Processing upload..."
        try:
            uploaded_file = change['new'][0] if isinstance(change['new'], (list, tuple)) else change['new']
            content = uploaded_file.get('content') or list(uploaded_file.values())[0]['content']
            with open(model_path, 'wb') as f: f.write(content)
            success, msg = load_model_from_file(model_path)
            if success:
                load_status.value = "✅ " + msg
                load_container.layout.display = 'none'
                dashboard_container.layout.display = 'flex'
            else:
                load_status.value = "❌ " + msg
        except Exception as e:
            load_status.value = f"❌ Upload failed: {str(e)}"

    def on_predict_click(b):
        if app_state['models'] is None: return

        # 1. Map Widgets to Values
        val_density = map_density[w_density.value]
        val_road = map_quality[w_road.value]
        val_trans = map_quality[w_transport.value]
        val_air = map_air[w_air.value]
        val_green = map_quality[w_green.value]
        val_renew = map_yn[w_renewable.value]
        val_risk = map_risk[w_risk.value]
        val_crime_map = {'Low': 0.2, 'Average': 0.5, 'High': 0.8}
        val_crime = val_crime_map[w_crime.value]
        val_income = w_income.value
        
        # 2. On-the-fly Feature Engineering (Must match training logic)
        val_carbon = 0.5
        if w_renewable.value == 'Yes': val_carbon -= 0.2
        if w_density.value == 'Very High': val_carbon += 0.3
        val_pop = val_density 
        
        # 3. Create Inputs Dictionary (Standard Features)
        input_dict = {
            'building_density': val_density,
            'road_connectivity': val_road,
            'public_transport_access': val_trans,
            'air_quality_index': val_air,
            'green_cover_percentage': val_green,
            'carbon_emission': val_carbon,
            'population_density': val_pop,
            'crime_rate': val_crime,
            'avg_income': val_income,
            'renewable_energy_usage': val_renew,
            'disaster_risk_index': val_risk
        }
        
        # 4. Handle One-Hot Encoding for Zone Type
        current_zone = w_zone.value
        input_dict[f'Zone_Type_{current_zone}'] = 1.0
        
        # 5. DataFrame Alignment (The Fix)
        try:
            model_ref = app_state['models']['Sustainability']
            expected_features = model_ref.feature_names_in_
            
            input_df = pd.DataFrame([input_dict]).reindex(columns=expected_features, fill_value=0)
            
            # 6. Predict
            s_score = app_state['models']['Sustainability'].predict(input_df)[0]
            i_score = app_state['models']['Infrastructure'].predict(input_df)[0]
            saf_score = app_state['models']['Safety'].predict(input_df)[0]
            l_score = app_state['models']['Livability'].predict(input_df)[0]
            
            # 7. Update UI
            out_sustain.value = create_gauge_html("Sustainability", s_score, theme['sustain']['color'], theme['sustain']['bg'])
            out_infra.value = create_gauge_html("Infrastructure", i_score, theme['infra']['color'], theme['infra']['bg'])
            out_safety.value = create_gauge_html("Safety", saf_score, theme['safety']['color'], theme['safety']['bg'])
            out_live.value = create_gauge_html("Livability", l_score, theme['live']['color'], theme['live']['bg'])
            
        except Exception as e:
            btn_predict.description = "Error: Mismatched Features"
            print(f"Prediction Error: {e}")

    uploader.observe(on_upload_change, names='value')
    btn_predict.on_click(on_predict_click)
    
    initial_view = load_container
    if os.path.exists(model_path):
        success, msg = load_model_from_file(model_path)
        if success:
            initial_view = dashboard_container
            load_container.layout.display = 'none'
        else:
            load_status.value = "Found file but failed to load: " + msg
    else:
        dashboard_container.layout.display = 'none'
    
    header = widgets.HTML("""
    <div style="
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
        padding: 15px; 
        border-radius: 10px 10px 0 0; 
        display: flex; align-items: center; justify-content: center; gap: 15px;
        margin-bottom: 15px; box_shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <div style="font-size: 24px;">🏙️</div>
        <div>
            <h3 style="color: white; margin: 0; font-family: sans-serif; font-weight: 700; letter-spacing: 1.5px;">
                URBAN GROWTH PREDICTOR
            </h3>
        </div>
    </div>
    """)
    
    app = widgets.VBox(
        [header, load_container, initial_view], 
        layout=widgets.Layout(
            padding='0px 0px 20px 0px', 
            border='none', 
            width='860px', 
            background_color='#f4f4f9',
            align_items='stretch',
            box_shadow='0 0 20px rgba(0,0,0,0.1)',
            border_radius='10px'
        )
    )
    
    display(app)

theme = {
    'sustain': {'color': '#2ca02c', 'bg': '#e8f5e9'},
    'infra':   {'color': '#1f77b4', 'bg': '#e3f2fd'},
    'safety':  {'color': '#ff7f0e', 'bg': '#fff3e0'},
    'live':    {'color': '#9467bd', 'bg': '#f3e5f5'}
}

def show_pillars():
    display(HTML(f"""
    <h3 style="text-align:center; font-family: 'Segoe UI', Arial; margin-top:15px; font-size:22px;">
        🌆 <b>The Cities of Tomorrow – Urban Growth & Sustainability</b>
    </h3>

    <div style="
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin-top: 18px;
        font-family: 'Segoe UI', Arial, sans-serif;
    ">

        <!-- Pillar 1 -->
        <div style="
            background: {theme['sustain']['bg']};
            border-left: 5px solid {theme['sustain']['color']};
            padding: 14px;
            border-radius: 8px;
            text-align: center;
        ">
            <h4 style="margin: 0; color: {theme['sustain']['color']}; font-size: 16px;">
                🌿 <b>Pillar 1</b><br>Sustainability
            </h4>
            <p style="margin: 6px 0 0; color: {theme['sustain']['color']}; font-size: 12px;">
                Environment • Energy • Ecology
            </p>
        </div>

        <!-- Pillar 2 -->
        <div style="
            background: {theme['infra']['bg']};
            border-left: 5px solid {theme['infra']['color']};
            padding: 14px;
            border-radius: 8px;
            text-align: center;
        ">
            <h4 style="margin: 0; color: {theme['infra']['color']}; font-size: 16px;">
                🏗️ <b>Pillar 2</b><br>Infrastructure
            </h4>
            <p style="margin: 6px 0 0; color: {theme['infra']['color']}; font-size: 12px;">
                Transport • Utilities • Urban Systems
            </p>
        </div>

        <!-- Pillar 3 -->
        <div style="
            background: {theme['safety']['bg']};
            border-left: 5px solid {theme['safety']['color']};
            padding: 14px;
            border-radius: 8px;
            text-align: center;
        ">
            <h4 style="margin: 0; color: {theme['safety']['color']}; font-size: 16px;">
                👥 <b>Pillar 3</b><br>Safety
            </h4>
            <p style="margin: 6px 0 0; color: {theme['safety']['color']}; font-size: 12px;">
                Crime Rate • Wage Gap • Risk
            </p>
        </div>

        <!-- Pillar 4 -->
        <div style="
            background: {theme['live']['bg']};
            border-left: 5px solid {theme['live']['color']};
            padding: 14px;
            border-radius: 8px;
            text-align: center;
        ">
            <h4 style="margin: 0; color: {theme['live']['color']}; font-size: 16px;">
                🛡️ <b>Pillar 4</b><br>Livability
            </h4>
            <p style="margin: 6px 0 0; color: {theme['live']['color']}; font-size: 12px;">
                Disaster Resilience
            </p>
        </div>

    </div>
    """))

