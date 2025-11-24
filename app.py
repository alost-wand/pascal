import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import plotly
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Hydraulic Power Lab",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def calculate_missing_value(force, area, pressure):
    """
    Calculate the missing value using Pascal's Law: P = F / A
    Returns: (calculated_force, calculated_area, calculated_pressure, message)
    """
    filled_count = sum([force is not None, area is not None, pressure is not None])
    
    if filled_count < 2:
        return None, None, None, "Need at least two values to calculate"
    
    if filled_count == 3:
        return force, area, pressure, "Got all three values"
    
    if force is None:
        if area > 0:
            force = pressure * area
            return force, area, pressure, f"Calculated Force: {force:.2f} N"
        else:
            return None, None, None, "Area needs to be greater than zero"
    
    if area is None:
        if pressure > 0:
            area = force / pressure
            return force, area, pressure, f"Calculated Area: {area:.4f} m²"
        else:
            return None, None, None, "Pressure needs to be greater than zero"
    
    if pressure is None:
        if area > 0:
            pressure = force / area
            return force, area, pressure, f"Calculated Pressure: {pressure:.2f} Pa"
        else:
            return None, None, None, "Area needs to be greater than zero"
    
    return force, area, pressure, "Done"


def get_pressure_level(pressure):
    """Determine pressure level and return color and label."""
    if pressure < 20000:
        return "LOW", "#87CEEB", "light blue"
    elif pressure < 80000:
        return "MEDIUM", "#4682B4", "medium blue"
    else:
        return "HIGH", "#00008B", "dark blue"


def draw_hydraulic_lift(pressure):
    """
    Draw hydraulic lift visualization with two pistons and fluid.
    Shows dynamic changes based on pressure.
    """
    width, height = 600, 400
    img = Image.new('RGB', (width, height), color='#1E1E1E')
    draw = ImageDraw.Draw(img)
    
    level, fluid_color, _ = get_pressure_level(pressure)
    
    small_piston_width = 60
    large_piston_width = 120
    piston_height = 40
    
    base_small_y = 200
    base_large_y = 200
    
    pressure_factor = min(pressure / 100000, 1.0)
    small_piston_offset = int(30 * pressure_factor)
    large_piston_offset = -int(40 * pressure_factor)
    
    small_piston_y = base_small_y + small_piston_offset
    large_piston_y = base_large_y + large_piston_offset
    
    fluid_top = max(small_piston_y + piston_height, large_piston_y + piston_height)
    fluid_bottom = height - 50
    
    draw.rectangle(
        [100, fluid_top, 500, fluid_bottom],
        fill=fluid_color,
        outline='#FFFFFF',
        width=2
    )
    
    small_piston_x = 150
    draw.rectangle(
        [small_piston_x - small_piston_width//2, small_piston_y, 
         small_piston_x + small_piston_width//2, small_piston_y + piston_height],
        fill='#808080',
        outline='#FFFFFF',
        width=2
    )
    draw.rectangle(
        [small_piston_x - 10, small_piston_y - 60, 
         small_piston_x + 10, small_piston_y],
        fill='#606060',
        outline='#FFFFFF',
        width=1
    )
    
    large_piston_x = 450
    draw.rectangle(
        [large_piston_x - large_piston_width//2, large_piston_y, 
         large_piston_x + large_piston_width//2, large_piston_y + piston_height],
        fill='#808080',
        outline='#FFFFFF',
        width=2
    )
    draw.rectangle(
        [large_piston_x - 15, large_piston_y - 80, 
         large_piston_x + 15, large_piston_y],
        fill='#606060',
        outline='#FFFFFF',
        width=1
    )
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    draw.text((small_piston_x, small_piston_y - 80), "Input\nPiston", fill='#FFFFFF', anchor="mm", font=small_font)
    draw.text((large_piston_x, large_piston_y - 100), "Output\nPiston", fill='#FFFFFF', anchor="mm", font=small_font)
    
    pressure_text = f"Pressure = {pressure:.0f} Pa"
    draw.text((300, fluid_top + 60), pressure_text, fill='#FFFFFF', anchor="mm", font=font)
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf


def draw_press_animation(pressure):
    """
    Draw hydraulic press visualization with dynamic compression effect.
    Shows soft press, strong press, or crush force based on pressure.
    """
    width, height = 400, 500
    img = Image.new('RGB', (width, height), color='#1E1E1E')
    draw = ImageDraw.Draw(img)
    
    level, _, _ = get_pressure_level(pressure)
    
    base_piston_y = 100
    box_y = 350
    box_height = 80
    
    if level == "LOW":
        piston_offset = 20
        shake_offset = 0
        box_compression = 0
        state_text = "Soft Press"
        state_color = "#87CEEB"
    elif level == "MEDIUM":
        piston_offset = 80
        shake_offset = int((pressure % 100) / 20)
        box_compression = 15
        state_text = "Strong Press"
        state_color = "#FFA500"
    else:
        piston_offset = 150
        shake_offset = int((pressure % 200) / 30)
        box_compression = 40
        state_text = "CRUSH FORCE!"
        state_color = "#FF0000"
    
    piston_y = base_piston_y + piston_offset
    
    draw.rectangle(
        [width//2 - 80 + shake_offset, 50, width//2 + 80 + shake_offset, piston_y],
        fill='#606060',
        outline='#FFFFFF',
        width=2
    )
    
    draw.rectangle(
        [width//2 - 60 + shake_offset, piston_y, width//2 + 60 + shake_offset, piston_y + 30],
        fill='#808080',
        outline='#FFFFFF',
        width=3
    )
    
    compressed_box_height = box_height - box_compression
    compressed_box_y = box_y + box_compression
    
    draw.rectangle(
        [width//2 - 70 + shake_offset, compressed_box_y, 
         width//2 + 70 + shake_offset, compressed_box_y + compressed_box_height],
        fill='#8B4513',
        outline='#FFFFFF',
        width=2
    )
    
    if level == "HIGH":
        for i in range(5):
            draw.line(
                [width//2 - 70 + shake_offset + i*35, compressed_box_y + compressed_box_height//2,
                 width//2 - 60 + shake_offset + i*35, compressed_box_y + compressed_box_height//2],
                fill='#FFFF00',
                width=2
            )
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((width//2, height - 50), state_text, fill=state_color, anchor="mm", font=font)
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf


def render_cards():
    """Render real-life application cards."""
    st.markdown("---")
    st.markdown("### Where You'll See This In Real Life")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: white;'>Car Lifts</h3>
            <p style='color: white;'>That's how mechanics lift your car with just a small pump.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: white;'>Brake Pedals</h3>
            <p style='color: white;'>A light tap on the pedal creates massive stopping power.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: white;'>Industrial Presses</h3>
            <p style='color: white;'>Can crush metal and shape materials with tons of force.</p>
        </div>
        """, unsafe_allow_html=True)


def create_pascal_law_3d_chart():
    """Create interactive 3D surface plot showing P = F/A relationship."""
    force_range = np.linspace(100, 10000, 50)
    area_range = np.linspace(0.01, 2.0, 50)
    
    F, A = np.meshgrid(force_range, area_range)
    P = F / A
    
    fig = go.Figure(data=[go.Surface(
        x=F,
        y=A,
        z=P,
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="Pressure (Pa)")
    )])
    
    fig.update_layout(
        title="Pascal's Law in 3D",
        scene=dict(
            xaxis_title="Force (N)",
            yaxis_title="Area (m²)",
            zaxis_title="Pressure (Pa)",
            bgcolor='#1E1E1E',
            xaxis=dict(gridcolor='#444'),
            yaxis=dict(gridcolor='#444'),
            zaxis=dict(gridcolor='#444')
        ),
        paper_bgcolor='#1E1E1E',
        plot_bgcolor='#1E1E1E',
        font=dict(color='white'),
        height=500
    )
    
    return fig


def create_pressure_force_chart(current_pressure):
    """Create chart showing Force vs Area at different pressure levels."""
    area_values = np.linspace(0.1, 2.0, 100)
    
    pressures = [10000, 30000, 50000, 80000, 100000]
    
    fig = go.Figure()
    
    for p in pressures:
        force_values = p * area_values
        fig.add_trace(go.Scatter(
            x=area_values,
            y=force_values,
            mode='lines',
            name=f'P = {p:,} Pa',
            line=dict(width=3 if p == int(current_pressure // 10000 * 10000) else 2)
        ))
    
    force_at_current = current_pressure * area_values
    fig.add_trace(go.Scatter(
        x=area_values,
        y=force_at_current,
        mode='lines',
        name=f'Current: {current_pressure:.0f} Pa',
        line=dict(width=4, dash='dash', color='#FF6B6B')
    ))
    
    fig.update_layout(
        title="Force vs Area",
        xaxis_title="Area (m²)",
        yaxis_title="Force (N)",
        paper_bgcolor='#1E1E1E',
        plot_bgcolor='#2E2E2E',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#444'),
        yaxis=dict(gridcolor='#444'),
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_piston_displacement_chart(current_pressure):
    """Create chart showing piston displacement vs pressure."""
    pressure_values = np.linspace(0, 120000, 100)
    
    small_piston_displacement = []
    large_piston_displacement = []
    
    for p in pressure_values:
        pressure_factor = min(p / 100000, 1.0)
        small_piston_displacement.append(30 * pressure_factor)
        large_piston_displacement.append(-40 * pressure_factor)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=pressure_values,
        y=small_piston_displacement,
        mode='lines',
        name='Input Piston (↓ Down)',
        line=dict(width=3, color='#4682B4')
    ))
    
    fig.add_trace(go.Scatter(
        x=pressure_values,
        y=large_piston_displacement,
        mode='lines',
        name='Output Piston (↑ Up)',
        line=dict(width=3, color='#87CEEB')
    ))
    
    pressure_factor = min(current_pressure / 100000, 1.0)
    small_current = 30 * pressure_factor
    large_current = -40 * pressure_factor
    
    fig.add_trace(go.Scatter(
        x=[current_pressure],
        y=[small_current],
        mode='markers',
        name='Current Input Position',
        marker=dict(size=12, color='#FF6B6B', symbol='diamond')
    ))
    
    fig.add_trace(go.Scatter(
        x=[current_pressure],
        y=[large_current],
        mode='markers',
        name='Current Output Position',
        marker=dict(size=12, color='#FFD700', symbol='diamond')
    ))
    
    fig.update_layout(
        title="How the Pistons Move",
        xaxis_title="Pressure (Pa)",
        yaxis_title="Displacement (pixels)",
        paper_bgcolor='#1E1E1E',
        plot_bgcolor='#2E2E2E',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#444'),
        yaxis=dict(gridcolor='#444'),
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_pressure_levels_gauge(current_pressure):
    """Create a gauge chart showing current pressure level."""
    level, color, _ = get_pressure_level(current_pressure)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_pressure,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Current Pressure", 'font': {'color': 'white', 'size': 20}},
        delta={'reference': 50000, 'suffix': ' Pa'},
        number={'suffix': ' Pa', 'font': {'color': 'white', 'size': 30}},
        gauge={
            'axis': {'range': [None, 120000], 'tickcolor': 'white'},
            'bar': {'color': color},
            'bgcolor': '#2E2E2E',
            'borderwidth': 2,
            'bordercolor': 'white',
            'steps': [
                {'range': [0, 20000], 'color': '#87CEEB'},
                {'range': [20000, 80000], 'color': '#4682B4'},
                {'range': [80000, 120000], 'color': '#00008B'}
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': current_pressure
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#1E1E1E',
        plot_bgcolor='#1E1E1E',
        font={'color': 'white'},
        height=300
    )
    
    return fig


def main():
    st.markdown("""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; text-align: center; margin: 0;'>
            Hydraulic Power Lab
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #2E2E2E; padding: 20px; border-radius: 10px; 
                border-left: 5px solid #667eea; margin-bottom: 30px;'>
        <h3 style='color: #667eea; margin-top: 0;'>What's Pascal's Law?</h3>
        <p style='color: white; font-size: 16px;'>
            When you apply pressure to a fluid in a closed space, that pressure spreads equally in every direction.
        </p>
        <p style='color: #B0B0B0; font-size: 14px; margin-bottom: 0;'>
            The math: <strong style='color: white;'>P = F / A</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col1:
        st.markdown("### Calculator")
        st.markdown("Fill in any two fields")
        
        force_input_str = st.text_input(
            "Force (N)", 
            value="",
            placeholder="Leave blank",
            help="Measured in Newtons"
        )
        
        area_input_str = st.text_input(
            "Area (m²)", 
            value="",
            placeholder="Leave blank",
            help="Measured in square meters"
        )
        
        pressure_input_str = st.text_input(
            "Pressure (Pa)", 
            value="",
            placeholder="Leave blank",
            help="Measured in Pascals"
        )
        
        calculate_button = st.button("Calculate", width='stretch', type="primary")
        
        if calculate_button:
            force_input = None
            area_input = None
            pressure_input = None
            
            try:
                if force_input_str.strip():
                    force_input = float(force_input_str)
                    if force_input < 0:
                        st.error("Force can't be negative")
                        force_input = None
            except ValueError:
                st.error("That's not a valid number for Force")
            
            try:
                if area_input_str.strip():
                    area_input = float(area_input_str)
                    if area_input < 0:
                        st.error("Area can't be negative")
                        area_input = None
            except ValueError:
                st.error("That's not a valid number for Area")
            
            try:
                if pressure_input_str.strip():
                    pressure_input = float(pressure_input_str)
                    if pressure_input < 0:
                        st.error("Pressure can't be negative")
                        pressure_input = None
            except ValueError:
                st.error("That's not a valid number for Pressure")
            
            force, area, pressure, message = calculate_missing_value(
                force_input, area_input, pressure_input
            )
            
            if force is not None and area is not None and pressure is not None:
                st.success(message)
                
                st.markdown("#### Results")
                st.metric("Force", f"{force:.2f} N")
                st.metric("Area", f"{area:.4f} m²")
                st.metric("Pressure", f"{pressure:.2f} Pa")
                
                level, color, color_name = get_pressure_level(pressure)
                
                st.markdown(f"""
                <div style='background-color: {color}; padding: 15px; 
                            border-radius: 8px; text-align: center; margin-top: 15px;'>
                    <h4 style='color: white; margin: 0;'>Pressure Level: {level}</h4>
                    <p style='color: white; margin: 5px 0 0 0;'>({color_name})</p>
                </div>
                """, unsafe_allow_html=True)
                
                rounded_pressure = int((pressure + 500) // 1000) * 1000
                st.session_state['current_pressure'] = max(0, min(rounded_pressure, 120000))
            else:
                st.error(message)
        
        if 'current_pressure' not in st.session_state:
            st.session_state['current_pressure'] = 50000
    
    with col2:
        st.markdown("### Hydraulic Lift")
        
        current_pressure = st.session_state.get('current_pressure', 50000)
        
        lift_img = draw_hydraulic_lift(current_pressure)
        st.image(lift_img, width='stretch')
        
        st.markdown(f"""
        <div style='background-color: #2E2E2E; padding: 10px; border-radius: 5px; text-align: center;'>
            <p style='color: white; margin: 0;'>
                <strong>Current Pressure:</strong> {current_pressure:.0f} Pa
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("### Hydraulic Press")
        
        current_pressure = st.session_state.get('current_pressure', 50000)
        
        press_img = draw_press_animation(current_pressure)
        st.image(press_img, width='stretch')
        
        level, _, _ = get_pressure_level(current_pressure)
        if level == "LOW":
            description = "Light compression - material barely affected"
        elif level == "MEDIUM":
            description = "Strong force - material deforming"
        else:
            description = "Maximum force - crushing material!"
        
        st.markdown(f"""
        <div style='background-color: #2E2E2E; padding: 10px; border-radius: 5px; text-align: center;'>
            <p style='color: white; margin: 0;'>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Pressure Controls")
    
    col_slider, col_gauge = st.columns([2, 1])
    
    with col_slider:
        st.markdown("#### Adjust Pressure")
        st.markdown("Drag the slider to see everything update")
        
        slider_pressure = st.slider(
            "Pressure (Pa)",
            min_value=0,
            max_value=120000,
            value=int(st.session_state.get('current_pressure', 50000)),
            step=1000,
            help="Adjust the pressure level"
        )
        
        if slider_pressure != st.session_state.get('current_pressure', 50000):
            st.session_state['current_pressure'] = slider_pressure
            st.rerun()
        
        level, color, color_name = get_pressure_level(slider_pressure)
        st.markdown(f"""
        <div style='background-color: {color}; padding: 12px; border-radius: 8px; text-align: center;'>
            <h4 style='color: white; margin: 0;'>Current Level: {level}</h4>
            <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>({slider_pressure:,.0f} Pa - {color_name})</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_gauge:
        st.markdown("#### Gauge")
        gauge_fig = create_pressure_levels_gauge(slider_pressure)
        st.plotly_chart(gauge_fig, width='stretch')
    
    st.markdown("---")
    st.markdown("### Data Visualization")
    
    tab1, tab2, tab3 = st.tabs(["3D View", "Force vs Area", "Piston Movement"])
    
    with tab1:
        st.markdown("**The relationship between Force, Area, and Pressure in 3D**")
        chart_3d = create_pascal_law_3d_chart()
        st.plotly_chart(chart_3d, width='stretch')
        
        st.info("Drag to rotate • Scroll to zoom")
    
    with tab2:
        st.markdown("**How force changes with different areas**")
        force_area_chart = create_pressure_force_chart(slider_pressure)
        st.plotly_chart(force_area_chart, width='stretch')
        
        st.info("Each line shows a different pressure level. Your current setting is the red dashed line.")
    
    with tab3:
        st.markdown("**Watch the pistons move as you change pressure**")
        displacement_chart = create_piston_displacement_chart(slider_pressure)
        st.plotly_chart(displacement_chart, width='stretch')
        
        st.info("Higher pressure pushes the input piston down and lifts the output piston up.")
    
    render_cards()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #808080; padding: 20px;'>
        <p style='font-size: 14px;'>Made with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
