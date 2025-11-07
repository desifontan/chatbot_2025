import streamlit as st
import groq

def configurar_pagina():
    st.title("Mi super chat de Desiree")
    
    st.sidebar.title("Selección de modelos")

    modelos = {
        "Llama 3.3 - 70B (Versátil)": "llama-3.3-70b-versatile",
        "Llama 3.3 - 70B (Específico)": "llama-3.3-70b-specdec",
        "Mixtral 8x7B (Razonamiento avanzado)": "mixtral-8x7b-32768",
        "Gemma 9B (Conversacional)": "gemma2-9b-it",
        "GPT-OSS 20B (OpenAI OSS)": "openai/gpt-oss-20b"
    }

    modelo_visible = st.sidebar.selectbox("Elegí un modelo", list(modelos.keys()), key="selector_modelo")
    return modelos[modelo_visible]

def crear_usuario():
    clave_secreta = st.secrets["clave_api"]
    return groq.Groq(api_key=clave_secreta)

stream_status = True
def configurar_modelos(cliente, modelo_elegido, prompt_usuario):
    return cliente.chat.completions.create(
        model=modelo_elegido,
        messages=[{"role": "user", "content": prompt_usuario}],
        stream= stream_status
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"],avatar=mensaje["avatar"]):
            st.write(mensaje["content"])

def area_chat():
    altura_contenedor_chat = 600
    contenedor = st.container(height=altura_contenedor_chat, border=True)
    with contenedor:
        mostrar_historial()

def generar_respuesta(respuesta_del_bot):
    respuesta_verdad = ""
    for frase in respuesta_del_bot:
        if frase.choices[0].delta.content:
            respuesta_verdad += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_verdad

def main():
    modelo_elegido_por_usuario = configurar_pagina()
    cliente_usuario = crear_usuario()
    inicializar_estado()

    area_chat()

    prompt_de_usuario = st.chat_input("Escribí tu prompt:")

    if prompt_de_usuario:
        actualizar_historial("user", prompt_de_usuario, "😠")
        respuesta_bot = configurar_modelos(cliente_usuario, modelo_elegido_por_usuario, prompt_de_usuario)

        if respuesta_bot:
            with st.chat_message("assistant"):
                respuesta_posta = st.write_stream(generar_respuesta(respuesta_bot))
                actualizar_historial("assistant", respuesta_posta, "👻")
                st.rerun()
if __name__ == "__main__":
    main()