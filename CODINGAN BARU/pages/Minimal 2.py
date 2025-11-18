import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from io import BytesIO

st.title("Larson–Miller Parameter - Minimal 2 1/4 Cr - 1 Mo Steel")

uploaded_file = st.file_uploader("Upload file CSV (kolom pertama = Stress (ksi))", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    y_values = df.iloc[:, 0].to_numpy()

    # === DATA SPLINE MINIMAL 2 ===
    x1 = np.array([30.6625,31.0562,31.4498,31.8434,32.2678,32.6538,33.0399,33.3861,33.7710,34.2657,
                   34.6404,35.0144,35.3709,35.7269,36.2510,36.4571,36.7447,37.0968,37.4315,37.7836,
                   38.0677,38.4152,38.7630,39.0000,39.1413,39.4878,39.8159])
    y1 = np.array([35.9585,33.5698,31.1207,28.6354,26.0174,23.4356,20.9141,19.5263,18.3469,16.9571,
                   15.9009,14.6703,13.5972,12.3524,10.5886,9.9599,9.1266,8.4905,7.8459,7.2019,
                   6.6350,6.0095,5.3470,5.0037,4.7477,4.2508,3.7946])

    x2 = np.array([545.4056,653.9883,762.5498,808.4877,823.5477,838.5928,853.6395,862.5469,866.4920,
                   881.4903,893.0852,903.2626,918.0415,932.8253,946.9408,959.5696,969.2708,971.8810,
                   981.1416,996.1400,1008.9975,1024.1059,1038.5315,1052.9414,1062.2950,1081.0429,
                   1094.7411,1103.2065])
    y2 = np.array([36.2405,33.8943,31.4878,29.2222,26.9677,24.4092,21.8820,20.7189,19.8982,
                   18.7269,17.8577,17.1747,15.9895,14.8384,13.7647,12.7486,11.7622,11.5036,
                   10.6075,10.0793,9.3780,9.3780,8.0417,7.3799,6.9921,6.0820,5.4242,5.0151])

    offset = 459.76

    # === FIX: pastikan spline valid ===
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

    st.write("### Hasil Perhitungan Minimal 2")
    st.dataframe(df_out, height=400)

    # === DOWNLOAD EXCEL ===
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_out.to_excel(writer, index=False)
    st.download_button(
        label="Download Hasil Excel",
        data=output.getvalue(),
        file_name="hasil_minimal2.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
