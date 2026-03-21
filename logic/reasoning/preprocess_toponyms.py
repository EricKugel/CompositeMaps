"""
This takes raw ocr output and uses an llm to generate search terms.
"""

from agent import Agent

llm = Agent("""
Your job is to generate toponym search terms based on the text on the map.
After reading the text provided from the map, you will pick out street names,
building names, natural feature names like lake names, river names, or mountain names,
etc. Each of the names you pick should be easily searchable to find their real life
locations. You never output a feature name that is not present in the text. You never
provide any extraneous formatting or commentary. You always put one searchable name per line.
""")

def prepare_for_search(text: str) -> str:
    return llm.query(text)