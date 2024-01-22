"""
PYTHON FILE FOR EXPORT CHAT FUNCTION
"""

from datetime import datetime

import streamlit as st


def export_chat():
    if "generated" in st.session_state:
        # save message in reverse order frist message always bot
        # the chat is stored in a html file format
        html_chat = ""
        html_chat += "<html><head><title>IA GUI</title>"
        # create two simply css box for bot and user like whatsapp
        html_chat += "<style> .bot { background-color: #e5e5ea; padding: 10px; border-radius: 10px; margin: 10px; width: 50%; float: left; } .user { background-color: #dcf8c6; padding: 10px; border-radius: 10px; margin: 10px; width: 50%; float: right; } </style>"
        html_chat += "</head><body>"
        # add header
        html_chat += "<center><h1>IA GUI </h1>"
        # add link for danation
        # add subheader with date and time
        html_chat += (
            "<br><br><h5>"
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + "</h5></center><br><br>"
        )
        # add chat
        # add solid container
        html_chat += '<div style="padding: 10px; border-radius: 10px; margin: 10px; width: 100%; float: left;">'
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            html_chat += (
                '<div class="bot">' + st.session_state["generated"][i] + "</div><br>"
            )
            html_chat += (
                '<div class="user">' + st.session_state["past"][i] + "</div><br>"
            )
        html_chat += "</div>"
        # add footer
        html_chat += "<br><br><center><small>Thanks you for testing a GUI </small>"
        # add link for danation

        html_chat += "</body></html>"

        # save file
        with open("chat.html", "w") as f:
            f.write(html_chat)
        # download file
        st.download_button(
            label="📚 Download chat",
            data=html_chat,
            file_name="chat.html",
            mime="text/html",
        )
