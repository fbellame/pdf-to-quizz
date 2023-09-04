from langchain.output_parsers.regex import RegexParser


doc = 'question: Who was Louis IX of France?\n CHOICE_A: A ruler who cared for the governed and made successful crusades.\n CHOICE_B: A ruler who opposed expanding administrations and burned Jewish books.\n CHOICE_C: A ruler who had a strong sense of justice and always wanted to judge people himself before applying any sentence.\n CHOICE_D: A ruler who was praised for his administrative reforms and portrayed as a flawless character in history books.\n\r'

parsers = {
    "question": RegexParser(
        regex=r"question:\s*(.*?)\n+",
        output_keys=["question"]
    ),
    "A": RegexParser(
        regex=r"(?:\n)+\s*CHOICE_A:(.*?)\n+",
        output_keys=["choice_a"]
    ),
    "B": RegexParser(
        regex=r"(?:\n)+\s*CHOICE_B:(.*?)\n+",
        output_keys=["choice_b"]
    ),
    "C": RegexParser(
        regex=r"(?:\n)+\s*CHOICE_C:(.*?)\n+",
        output_keys=["choice_c"]
    ),
    "D": RegexParser(
        regex=r"(?:\n)+\s*CHOICE_D:(.*?)\n+",
        output_keys=["choice_d"]
    ),
    "reponse": RegexParser(
        regex=r"(?:\n)+reponse:\s?(.*)",
        output_keys=["answer"]
    )
}

def get_parsed_value(parser, key, doc):
    try:
        result = parser.parse(doc)
        value = result.get(key).strip()
        return {key: value}
    except Exception as e:
        print(f"Error processing doc: {str(e)}")
        print(f"Key {key}")
        return {key: "error"}

quizz = {}
for key, parser in parsers.items():
    quizz.update(get_parsed_value(parser, key, doc))

quizz_list = [quizz]

# Print the parsed output
print(quizz_list)