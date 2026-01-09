import streamlit as st
import pandas as pd
import joblib

# =========================
# Configuração da página
# =========================
st.set_page_config(
    page_title="Predição de Obesidade",
    layout="centered"
)

st.title("🩺 Sistema Preditivo de Obesidade")
st.markdown(
    """
    Esta aplicação utiliza **Machine Learning** para apoiar a identificação
    de **riscos relacionados à obesidade**, considerando dados físicos
    e hábitos de vida.
    """
)

# =========================
# Carrega modelo
# =========================
model = joblib.load("obesity_pipeline.pkl")

# =========================
# Dicionários de conversão
# =========================
yes_no_map = {
    "Sim": "yes",
    "Não": "no"
}

gender_map = {
    "Masculino": "Male",
    "Feminino": "Female"
}

caec_map = {
    "Não": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always"
}

calc_map = {
    "Não": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always"
}

mtrans_map = {
    "Transporte Público": "Public_Transportation",
    "Automóvel": "Automobile",
    "Caminhada": "Walking",
    "Motocicleta": "Motorbike",
    "Bicicleta": "Bike"
}

# Tradução das classes finais
class_map = {
    "Insufficient_Weight": "Baixo Peso",
    "Normal_Weight": "Peso Normal",
    "Overweight_Level_I": "Sobrepeso Grau I",
    "Overweight_Level_II": "Sobrepeso Grau II",
    "Obesity_Type_I": "Obesidade Grau I",
    "Obesity_Type_II": "Obesidade Grau II",
    "Obesity_Type_III": "Obesidade Grau III"
}

# =========================
# Formulário
# =========================
st.header("📋 Dados do Paciente")

with st.form("form_paciente"):

    col1, col2 = st.columns(2)

    with col1:
        Gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
        Age = st.number_input("Idade", 5, 100, 25)
        Height = st.number_input("Altura (m)", 1.30, 2.20, 1.70)
        Weight = st.number_input("Peso (kg)", 30.0, 200.0, 70.0)
        family_history = st.selectbox("Histórico familiar de excesso de peso?", ["Sim", "Não"])
        FAVC = st.selectbox("Consome alimentos altamente calóricos?", ["Sim", "Não"])
        FCVC = st.slider("Consumo de vegetais (1 = baixo, 3 = alto)", 1, 3, 2)
        NCP = st.slider("Número de refeições principais por dia", 1, 4, 3)

    with col2:
        CAEC = st.selectbox("Come entre as refeições?", ["Não", "Às vezes", "Frequentemente", "Sempre"])
        SMOKE = st.selectbox("Fuma?", ["Sim", "Não"])
        CH2O = st.slider("Consumo diário de água (1 = pouco, 3 = alto)", 1, 3, 2)
        SCC = st.selectbox("Monitora calorias ingeridas?", ["Sim", "Não"])
        FAF = st.slider("Frequência de atividade física (0 = nunca, 3 = frequente)", 0, 3, 1)
        TUE = st.slider("Tempo em dispositivos tecnológicos (0 = pouco, 2 = muito)", 0, 2, 1)
        CALC = st.selectbox("Consumo de álcool", ["Não", "Às vezes", "Frequentemente", "Sempre"])
        MTRANS = st.selectbox("Meio de transporte", list(mtrans_map.keys()))

    submit = st.form_submit_button("🔍 Avaliar Risco")

# =========================
# Avaliação
# =========================
if submit:

    # -------------------------
    # Regra clínica de IMC
    # -------------------------
    imc = Weight / (Height ** 2)

    st.subheader("📊 Resultado da Avaliação")

    if imc < 16:
        st.error("⚠️ **Alerta Clínico:** Baixo Peso Grave detectado (IMC extremamente baixo).")
        st.warning("Recomenda-se avaliação médica imediata.")

    elif imc > 40:
        st.error("⚠️ **Alerta Clínico:** Obesidade Grave detectada (IMC extremamente elevado).")
        st.warning("Recomenda-se acompanhamento médico especializado.")

    else:
        # -------------------------
        # Entrada para o modelo
        # -------------------------
        input_data = pd.DataFrame([{
            "Gender": gender_map[Gender],
            "Age": Age,
            "Height": Height,
            "Weight": Weight,
            "family_history": yes_no_map[family_history],
            "FAVC": yes_no_map[FAVC],
            "FCVC": FCVC,
            "NCP": NCP,
            "CAEC": caec_map[CAEC],
            "SMOKE": yes_no_map[SMOKE],
            "CH2O": CH2O,
            "SCC": yes_no_map[SCC],
            "FAF": FAF,
            "TUE": TUE,
            "CALC": calc_map[CALC],
            "MTRANS": mtrans_map[MTRANS]
        }])

        prediction = model.predict(input_data)[0]
        resultado = class_map.get(prediction, prediction)

        if "Obesidade" in resultado or "Sobrepeso" in resultado:
            st.error(f"🚨 **Risco Identificado:** {resultado}")
        else:
            st.success(f"✅ **Classificação:** {resultado}")

        st.info("Este resultado é um apoio à decisão e não substitui avaliação médica.")
