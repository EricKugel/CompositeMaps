from pathlib import Path
import ocr
import preprocess_toponyms

text = ocr.scan(Path("data/test/tunnels.png"))
print(text)
text = preprocess_toponyms.prepare_for_search(text)
with open("llm_output.txt", "w") as file:
    file.write(text)
print(text)