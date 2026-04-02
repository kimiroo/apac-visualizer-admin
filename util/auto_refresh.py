import streamlit.components.v1 as components

def auto_refresh():
    html = f'''
    <script>
        (function() {{
            window.parent.location.reload();
        }})();
    </script>
    '''

    components.html(html, height=0)