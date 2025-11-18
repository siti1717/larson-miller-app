import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from io import BytesIO

st.title("Larson–Miller Parameter - Mean 2 1/4 Cr - 1 Mo Steel")

uploaded_file = st.file_uploader("Upload file CSV (kolom pertama = Stress (ksi))", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    y_values = df.iloc[:, 0].to_numpy()

    # === DATA SPLINE MEAN 2 ===
    x1 = np.array([
        39.8883,39.6838,39.4668,39.2402,39.0706,38.8531,38.6098,38.3798,38.1496,37.9961,
        37.7635,37.5308,37.2859,37.1035,36.8707,36.6508,36.4078,36.1539,35.9769,35.7319,
        35.5679,35.3126,35.0561,34.8192,34.5701,34.3602,33.9454,33.7971,33.5262,33.2553,
        32.9838,32.7129,32.4414,32.1705,31.9732,31.7464,31.4693,31.1915,30.9146
    ])
    y1 = np.array([
        4.9361,5.3252,5.7681,6.1151,6.5289,6.9113,7.3236,7.7703,8.1920,8.8226,
        9.2531,9.6655,10.1046,10.8251,11.6403,12.5458,13.0940,13.9825,14.8317,15.4890,
        16.1627,16.9809,17.7295,18.6160,19.1549,20.0631,22.6244,23.2815,25.1173,27.0184,
        28.4837,30.3407,31.8034,33.6477,34.8566,36.2679,37.9977,39.2611,41.1690
    ])

    x2 = np.array([
        647.9949,723.1762,767.7412,809.5735,820.3247,831.0751,841.8221,852.5798,863.3143,
        874.0741,884.8185,895.5568,901.9223,904.9975,914.9440,924.7729,932.4329,941.6996,
        952.0689,960.2460,968.4736,977.3490,986.4627,995.9402,1005.9652,1016.5522,1026.9612,
        1038.0202,1048.5970,1059.1324,1068.6827,1078.2184,1087.7731,1095.3090,1104.3389
    ])
    y2 = np.array([
        41.1690,39.2611,38.4810,35.9467,34.2310,32.5018,30.7115,29.1077,27.1012,25.5356,
        23.7001,21.7600,20.9634,20.2910,19.6415,18.8058,18.2844,17.3915,16.6780,15.9696,
        15.3098,14.3734,13.4509,12.2937,11.2254,10.4440,9.7330,9.2334,8.8143,8.2791,
        7.8460,7.3721,6.9512,6.5986,6.1388
    ])
    offset = 459.76

    # === FIX: pastikan tidak ada duplikat & urutan naik ===
    y1_unique, idx1 = np.unique(y1[::-1], return_index=True)
    x1_unique = x1[::-1][idx1]
    cs1 = CubicSpline(y1_unique, x1_unique, extrapolate=True)

    y2_unique, idx2 = np.unique(y2[::-1], return_index=True)
    x2_unique = x2[::-1][idx2]
    cs2 = CubicSpline(y2_unique, x2_unique, extrapolate=True)

    # === HITUNG PARAMETER ===
    B = cs1(y_values)
    C = cs2(y_values) + offset
    D = 10 ** ((B * 1000 / C) - 20)
    E = D / (24 * 365)

    df_out = pd.DataFrame({
        "Stress (ksi)": y_values,
        "P": B,
        "T(R)": C,
        "t(Hours)": D,
        "t(Years)": E
    })

    st.write("### Hasil Perhitungan Mean 2")
    st.dataframe(df_out, height=400)

    # === DOWNLOAD EXCEL ===
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_out.to_excel(writer, index=False)
    st.download_button(
        label="Download Hasil Excel",
        data=output.getvalue(),
        file_name="hasil_mean2.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
