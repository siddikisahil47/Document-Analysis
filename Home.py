import streamlit as st

st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_title="Get Your Professional Answers Here!",
    page_icon="pages/icon.png",
) 
main_page_markdown = """
<style>
.header {
    font-size: 60px;
    font-weight: 800;
    padding-right: -5px;
    padding-bottom: 25px;
}
.header:hover {
    font-weight:900;
    transition: 0.2s;
}
.text {
    padding-top: 0px;
}

</style>
<h1 class="header">Get Your Professional Answers Here!</h1>
<div class="text">For all your legal and scholarly needs, we are here to help you. Ask us anything and we will provide you with the best possible answer.</div>

"""
st.image(
            "pages/illustration.gif", # I prefer to load the GIFs using GIPHY
        )
st.markdown(main_page_markdown, unsafe_allow_html=True)

st.markdown(
    """
    <style>
	[data-testid="stDecoration"] {
		display: none;
	}
    </style>""",
    unsafe_allow_html=True,
)


st.markdown(
    """

<button>
<a href="/Doc_Analysis" target = _self>
  <div class="svg-wrapper-1">
    <div class="svg-wrapper">
    </div>
  </div>
  <span>Continue</span>
</a>
</button>
<style>
button {
  font-family: inherit;
  font-size: 20px;
  background: #212121;
  color: white;
  margin-top: 15px;
  fill: rgb(155, 153, 153);
  padding: 0.7em 1em;
  padding-left: 0.9em;
  display: flex;
  align-items: center;
  cursor: pointer;
  border: none;
  border-radius: 15px;
  font-weight: 1000;
}
a {
  color: white;
  text-decoration: none;
}
a:visited {
  color: white;
  text-decoration: none;
}
a:hover {
  color: grey;
  text-decoration: none;
}
a:active {
  color: white;
  text-decoration: none;
}


</style>
            
 """,
    unsafe_allow_html=True,
)
