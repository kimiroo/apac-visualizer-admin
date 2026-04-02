import streamlit as st
import streamlit.components.v1 as components

import time

def auto_download(base64_string, filename, filetype):
    html = f'''
    <script>
        (function() {{
            const b64 = "{base64_string}";
            const fileName = "{filename}";

            // Convert base64 to raw binary data held in a string
            const byteCharacters = atob(b64);
            const byteNumbers = new Array(byteCharacters.length);

            for (let i = 0; i < byteCharacters.length; i++) {{
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }}

            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray], {{type: '{filetype}'}});

            // Create a link and trigger the download
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            a.click();

            // Cleanup
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }})();
    </script>
    '''

    placeholder = st.empty()

    with placeholder:
        components.html(html, height=0)

    time.sleep(0.1)

    placeholder.empty()