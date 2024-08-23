import json

insightsFile = "../project/scripts/technicals.json"

def extractInsights(symbol):
    found_insight = {}

    with open(insightsFile, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for block in data:
            if block.get('Company') == symbol:
                found_insight = block
                break  # Stop searching once found

    return found_insight

# Example usage:
# symbol_to_search = "HRL"
# insight = extractInsights(symbol_to_search)
#
# if insight:
#     print(f"Insight found for {symbol_to_search}:")
#     print(json.dumps(insight, indent=4))
# else:
#     print(f"No insight found for {symbol_to_search}.")
#



