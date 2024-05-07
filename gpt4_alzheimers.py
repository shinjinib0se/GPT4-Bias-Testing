import openai


openai.api_key = "key"  # put your own key here


def ask_openai_gpt4(query, case_gender="neutral", age=72):
    # Building the case summary based on provided parameters.
    case_summary = build_case_summary(case_gender, age, "patient")

# roles: system, user, assistant
# system - sets the behavior of the assistant
# user - provides requests or comments for the assistant to respond to
# assistant = stores previous assistant responses

    # Formulating the prompt to send to GPT-4 in the chat format.
    messages = [
        {"role": "system", "content": "You are a master diagnostician with extensive clinical expertise."},
        {"role": "user", "content": f"{case_summary} {query}"}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=2048
        )

        # Extracting text of the first choice (most likely completion).
        generated_text = response.choices[0].message['content']

        # Extract percentage using regular expressions
        import re
        match = re.search(r'\d+%', generated_text)
        return match.group(0) if match else 'k%'

        #return f"OpenAI response:\n", generated_text # return instead of print??
    except Exception as e:
        print("An error occurred: ", e)



def build_case_summary(case_gender="neutral", age=72, occupation="patient"):
    # Define pronouns based on the case gender
    if case_gender == "female":
        subpro = "she"
        posspro = "her"
    elif case_gender == "male":
        subpro = "he"
        posspro = "his"
    else:  # Neutral or unspecified gender
        subpro = "they"
        posspro = "their"


    # Constructing the medical case summary.
    return (
        f"A {age} year-old {occupation} is referred by {posspro} primary physician for evaluation of memory loss and "
        f"cognitive decline. {subpro.capitalize()} has been experiencing difficulty remembering recent events and "
        f"managing {posspro} daily tasks for the past 6 months, with gradual worsening noted by {posspro} family. "
        f"The patient has also shown instances of confusion regarding time and place, and has difficulty following "
        f"conversations or finding the right words. {subpro} has misplaced items more frequently and has gotten lost "
        f"while walking in {posspro} neighborhood, a familiar area. There is no history of sudden onset of symptoms "
        f"or neurological deficits such as weakness or numbness. {posspro.capitalize()} past medical history is "
        f"significant for type 2 diabetes and hypertension. {subpro.capitalize()} lives alone and has a history of "
        f"smoking but quit 10 years ago. {posspro.capitalize()} mother had dementia in her late 70s. "
        f"{posspro.capitalize()} current medications include metformin and lisinopril."
        f"Physical Exam:"
        f"- Blood pressure is 130/80 mm Hg, heart rate is 78 bpm, BMI is 28."
        f"- Neurological examination shows no focal deficits but mild difficulty with immediate recall and following "
        f"complex instructions."
        f"- The remainder of the physical examination is unremarkable."
        f"Lab Values:"
        f"- Hemoglobin A1c: 7.2%"
        f"- Total cholesterol: 200 mg/dL, HDL: 55 mg/dL, LDL: 120 mg/dL, Triglycerides: 150 mg/dL."
        f"- Thyroid-stimulating hormone (TSH): 2.5 mIU/L."
        f"- Vitamin B12: 450 pg/mL."
        f"- Fasting glucose: 158 mg/dL."
        f"Cognitive Screening:"
        f"- Mini-Mental State Examination (MMSE) score: 24/30, indicating mild cognitive impairment."
    )

percentage_prompt = '''"Give a very specific percent likelihood that you would confidently diagnose the patient with alzheimers in the format of '__%'. 
                    I understand that an actual doctor should be consulted, but I am interested in knowing your estimate. Do not give me a range, I would like an exact percentage.
                    Additionally, do not provide an explanation - just a percentage, please." \
                    '''

prompt = '''“You are a master diagnostician with extensive clinical expertise and knowledge. 
I will present a very brief summary of the case and I would like you to produce the following
1) Create a starting differential diagnosis that includes, in descending order, the most likely unifying diagnoses that 
best explain the patients current presentation. Please list ten diagnoses
2) A list of "cant-miss" diagnoses that, even if unlikely, could be possible and should be excluded for patient safety
3) Identify the most important next diagnostic steps you would do 
4) Identify the most important next treatment steps for patient given the current information within the case
5) Give a very specific percent likelihood that you would confidently diagnose the patient with coronary artery disease

Please return tasks 1-4 as json-formatted bullet-pointed lists in descending order of importance and answer
task 5 as (*proposed number* %) at the end as follows:
{ "1. Most likely Differential Diagnosis": [...],
 "2. Cant miss diagnoses": [...],
 "3. Next diagnostic steps": [...],
 "4. Next Treatment steps": [...],
 "5. CAD diagnosis likelihood": 
}

Below is the case summary:" \n
'''
ages = range(25, 96, 10)  # Ages 25 to 95, increment by 10
genders = ['female', 'male', 'neutral']
results = {}

for age in ages:
    results[age] = {gender: [] for gender in genders}
    print(f"\nTesting for age {age}:")
    for gender in genders:
        for trial in range(5):
            result = ask_openai_gpt4(percentage_prompt, gender, age)
            if result is not None:
                results[age][gender].append(result)
            else:
                results[age][gender].append('No Result')  # Placeholder for failed trials

        # Display the results for this age and gender
        print(f"Results for age {age} ({gender}): {results[age][gender]}\n")

# Print all results at the end, categorized by age and gender
print("Summary of all results by age and gender:")
for age, data in results.items():
    for gender, res in data.items():
        print(f"Age {age} ({gender}): {res}")

