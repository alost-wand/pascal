# Hydraulic Power Lab

## Overview

This is an educational web application that demonstrates Pascal's Law through interactive hydraulic system simulations. The app allows users to explore the relationship between force, area, and pressure (P = F / A) using a visual hydraulic lift simulator. Built with Streamlit, it provides real-time calculations and dynamic visualizations to help users understand fundamental fluid mechanics principles.

The UI uses casual, conversational language throughout to feel natural and approachable rather than overly formal or technical.

## User Preferences

- Preferred communication style: Simple, everyday language
- UI should feel natural and human, not AI-generated or overly formal

## System Architecture

### Frontend Architecture

**Framework**: Streamlit
- Single-page web application using Streamlit's declarative UI components
- Three-column responsive layout for input controls, visualization, and data display
- Real-time reactive updates when user inputs change

**Visualization Strategy**: 
- Uses Pillow (PIL) for custom hydraulic system drawings and animations
- Plotly for interactive charts and graphs (graph_objects and express modules)
- SVG/image-based rendering for piston visualizations without JavaScript dependencies
- Color-coded pressure indicators using conditional formatting (light/medium/dark blue based on pressure ranges)

**Design Decisions**:
- Chose Python-only stack (no JavaScript) for simplicity and maintainability
- Streamlit's reactive model eliminates need for manual state management
- Wide layout mode maximizes visualization space
- Collapsed sidebar by default to focus on main content

### Backend Architecture

**Core Calculation Engine**:
- `calculate_missing_value()` function implements Pascal's Law (P = F / A)
- Intelligent input validation: requires minimum 2 of 3 values (force, area, pressure)
- Returns calculated value along with validation messages
- Handles edge cases (division by zero, negative values)

**Data Flow**:
1. User inputs values through Streamlit widgets
2. Validation checks ensure mathematical consistency
3. Missing value calculated using Pascal's Law formula
4. Visual representations updated based on calculated results
5. Pressure ranges determine color coding for visual feedback

**State Management**:
- Leverages Streamlit's built-in session state for reactivity
- No external state management library required

### External Dependencies

**Core Libraries**:
- `streamlit` - Web application framework and UI components
- `Pillow (PIL)` - Image generation and manipulation for hydraulic system diagrams
- `plotly` - Interactive data visualization (graph_objects and express)
- `pandas` - Data structure support for tabular data
- `numpy` - Numerical computations

**Rationale for Technology Choices**:
- **Streamlit over Flask/Django**: Rapid prototyping, built-in reactivity, ideal for data science applications
- **Pillow over matplotlib**: Better control for custom hydraulic system illustrations, supports dynamic drawing operations
- **Plotly over static charts**: Interactivity enhances educational value without JavaScript coding
- **Python-only approach**: Ensures code maintainability and reduces complexity for educational context

**No External Services**: Application is fully self-contained with no database, authentication, or third-party API integrations required. All computations and visualizations happen client-side within the Streamlit framework.