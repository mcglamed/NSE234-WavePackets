import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------

st.set_page_config(
    page_title="Wave Packet Builder",
    page_icon="〰️",
    layout="wide",
)

st.title("Wave Packet Builder")

st.markdown(
    """
    Explore how waves combine to form localized wave packets. Adjust the
    amplitude, central wavelength, wavelength bandwidth, and number of
    component waves using the controls on the left.
    """
)


# ------------------------------------------------------------
# Wave functions
# ------------------------------------------------------------

def generate_wave(amplitude, wavelength, x):
    """Generate a cosine wave."""
    return amplitude * np.cos(2.0 * np.pi * x / wavelength)


def sinc_envelope(amplitude, delta_lambda, wavelength, x):
    """
    Sinc envelope based on:

        (2/x) sin(delta_lambda*pi*x/wavelength^2)

    np.sinc(z) is defined as sin(pi*z)/(pi*z), which also
    handles the limit at x = 0.
    """
    argument = delta_lambda * x / wavelength**2

    return (
        amplitude
        * 2.0
        * np.pi
        * delta_lambda
        / wavelength**2
        * np.sinc(argument)
    )


def gaussian_envelope(amplitude, delta_lambda, wavelength, x):
    """Generate a Gaussian envelope."""
    return amplitude * np.exp(
        -2.0 * (delta_lambda * np.pi * x / wavelength**2) ** 2
    )


def create_wavelengths(center_wavelength, bandwidth, number_waves):
    """
    Distribute wavelengths symmetrically around the central wavelength.

    bandwidth is the total wavelength range:
        lambda_0 - bandwidth/2 through lambda_0 + bandwidth/2
    """
    return np.linspace(
        center_wavelength - bandwidth / 2.0,
        center_wavelength + bandwidth / 2.0,
        number_waves,
    )


# ------------------------------------------------------------
# Sidebar controls
# ------------------------------------------------------------

with st.sidebar:
    st.header("Wave Parameters")

    plot_type = st.selectbox(
        "Plot type",
        [
            "Single Wave",
            "Two-Wave Superposition",
            "N-Wave Superposition",
            "Sinc-Modulated Wave",
            "Gaussian-Modulated Wave",
        ],
        index=2,
    )

    amplitude = st.slider(
        "Amplitude, A",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
    )

    wavelength = st.slider(
        "Central wavelength, λ₀",
        min_value=1.0,
        max_value=30.0,
        value=10.0,
        step=0.1,
    )

    # This prevents lambda_0 - delta_lambda/2 from becoming zero.
    maximum_bandwidth = min(10.0, 1.8 * wavelength)

    delta_lambda = st.slider(
        "Wavelength bandwidth, Δλ",
        min_value=0.01,
        max_value=float(maximum_bandwidth),
        value=min(1.0, float(maximum_bandwidth)),
        step=0.01,
        help=(
            "The component wavelengths extend from "
            "λ₀ - Δλ/2 to λ₀ + Δλ/2."
        ),
    )

    number_waves = st.slider(
        "Number of component waves, N",
        min_value=2,
        max_value=100,
        value=10,
        step=1,
    )

    st.divider()
    st.header("Display Options")

    show_components = st.checkbox(
        "Show component waves",
        value=False,
    )

    show_envelope = st.checkbox(
        "Show envelope",
        value=True,
    )

    normalize_sum = st.checkbox(
        "Normalize wave superposition",
        value=True,
        help=(
            "Divides the summed wave amplitude by the number of "
            "component waves."
        ),
    )

    show_squared_amplitude = st.checkbox(
        "Show squared amplitude |ψ|²",
        value=False,
    )

    st.divider()
    st.header("Plot Range")

    x_limit = st.slider(
        "Position range, ±x",
        min_value=20.0,
        max_value=300.0,
        value=100.0,
        step=10.0,
    )


# ------------------------------------------------------------
# Position coordinates
# ------------------------------------------------------------

x = np.linspace(
    -x_limit,
    x_limit,
    5000,
)


# ------------------------------------------------------------
# Construct the selected wave
# ------------------------------------------------------------

components = None
envelope = None
component_wavelengths = None

if plot_type == "Single Wave":

    wave = generate_wave(
        amplitude,
        wavelength,
        x,
    )

    title = "Single Monochromatic Wave"

    equation = (
        r"\psi(x)=A\cos\left(\frac{2\pi x}{\lambda_0}\right)"
    )


elif plot_type == "Two-Wave Superposition":

    component_wavelengths = create
