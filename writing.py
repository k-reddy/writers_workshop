import anthropic
import os
import pickle

# Goal is to receive feedback prompts and write a new draft of the story
# that incorporates the feedback

# grab the API key
with open(os.path.expanduser("~/Documents/developer_creds/anthropic_key.txt")) as f:
    api_key = f.read().strip()

# set up the client
client = anthropic.Anthropic(
    api_key=api_key,
)

# test_feedback = "The plot is not fleshed out. There are many notes to yourself. You should finish the story according to the notes."
# story = """
# Jean walked into a room of scanners and faced a full-wall screen.
# “Welcome to the auction for rental AA005. If you require any specific data or readings, please request it verbally. And use your hologram forms. We prefer transparency so all can understand.”
# Several holograms appeared around Jean, pacing excitedly.
# [they ask Jean to do some stuff] [soon the room is full of figures, pushing to get to the front.]
# [a bid commences] [talk about Jean’s feelings - apathy? fear?
# """
test_story = """Jean walked into the sterile, white-walled chamber, her footsteps echoing against gleaming surfaces. Rows of scanning equipment lined the walls, their sensors tracking her every movement. A full-wall screen flickered to life, displaying auction details for rental unit AA005.\n\n"Welcome to the auction," a mechanical voice announced. "Please use hologram forms. Transparency is mandatory."\n\nTranslucent figures began materializing around her - some tall and angular, others compact and rigid. Each hologram represented a potential buyer, their forms shifting with barely contained excitement.\n\nA holographic broker stepped forward. "Unit AA005 represents a unique acquisition. Partially restored human stock, minimal genetic drift, prime reproductive potential."\n\nJean felt a chill run down her spine. The holograms pressed closer, their transparent bodies overlapping, voices rising in a cacophony of bids and technical assessments.\n\n"Genetic stability at 87.3%!"\n"Neurological mapping indicates high adaptability!"\n"Bidding opens at 500,000 credit units!"\n\nHer own emotions felt distant, compartmentalized. Was this apathy or a survival mechanism? Years of processing through these auctions had worn down her emotional responses.\n\nThe bidding intensified. Holograms pushed and intersected, their digital representations becoming more aggressive. Jean remained still, a living commodity being evaluated by algorithmic buyers.\n\nOne hologram, more solid than the others, stepped directly in front of her. Its form suggested corporate ownership - sharp lines, precise movements.\n\n"Preliminary assessment complete," it announced. "Genetic profile acceptable. Neurological potential: exceptional."\n\nJean\'s heart rate remained steady. She had been through this process before. She would go through it again.\n\nThe final bid approached. Credits would transfer. A new owner would be selected.\n\nShe waited, perfectly still."""
# story = """
# The doctor leaned forward. “What are your thoughts about your life?”
# “My life?” Jean asked.
# “Yes, how do you feel about it?”
# “Well, fine, I guess. It’s,” she paused, “different than I expected.”
# “You don’t need to be polite. It’s important to be honest.”
# Jean looked away from the screen, thinking. She didn’t know how to answer the question. So much had changed so quickly, but she wasn’t particularly happy before. Now, well, she’d be lucky to get the job. This answer was important. “This isn’t what I saw for myself. But I wasn’t happy before, either. At least now I have company. And this job is important to me.”
# “Do you harbor resentment?”
# “No,” Jean replied honestly. She didn’t care much who was in charge. And she’d heard there could be side effects to the work. Good ones.
# “Psychological stability 62/100. Antipathy 8/100. You’ve passed your medical examination,” the doctor said. “Now, please go through the door on your right.”

# Jean walked into a room of scanners and faced a full-wall screen.
# “Welcome to the auction for rental AA005. If you require any specific data or readings, please request it verbally. And use your hologram forms. We prefer transparency so all can understand.”
# Several holograms appeared around Jean, pacing excitedly.
# [they ask Jean to do some stuff] [soon the room is full of figures, pushing to get to the front.]
# [a bid commences] [talk about Jean’s feelings - apathy? fear?
# “The three top bidders are 22102, 4904, and 5554. The rest, please detach or enter the next auction room.” All but 3 holograms disappeared. “Thank you for your patience, Jean. By our protocols, you get to choose between the top three bidders. Fit is very important, so we do not disclose their bids to you.” Jean had read the statistics. When humans were allowed to choose their match, there was a 7% decrease in mortality and an over 200% increase in repeat contracts. It seemed to have nothing to do with anything data could identify. They called it the fate effect. “Rest assured, all cleared your minimum threshold and we have assessed them for compatibility. There is no bad choice here. The floor is yours.”
# Suddenly the dynamic in the room shifted. Jean had the power to choose. People like him were in short supply, after all. The program was new. Much was unknown. The system was still fallible in screening for masochism and abuse. They were punished, but that was after the fact. Jean walked among the three holograms, assessing body language. It was all put on, of course, for his benefit. But he could at least read what they were trying to communicate.
# “Why are you interested in me?” He asked the second one, a [description].
# [he does an assessment, and he picks one he likes—show they have personalities][asks why they want a body, what they want to do. Asks what their job is, what gives them meaning]
# """


# EXPLAIN WHAT PRESERVING STYLE MEANS
def rewrite_story(focus, focus_explanation, feedback, story):
    # send a request and get a message back
    message = client.messages.create(
        model="claude-3-5-haiku-latest",
        # model="claude-3-5-sonnet-20241022",
        system=generate_system_prompt(focus),
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": generate_message_prompt(
                    focus, focus_explanation, feedback, story
                ),
            }
        ],
    )
    print(message.content[0].text)
    return message.content[0].text


def generate_system_prompt(focus):
    return f"""You are a ghost writer. 
    You've made a career of rewriting drafts of other people's stories.
    Your clients use you because you incorporate feedback while retaining their original style.
    You are particularly gifted at {focus}."""


def generate_message_prompt(focus, focus_explanation, feedback, story):
    return f"""
    You are going to receive a story and some feedback.
    Your goal is to make the best second draft of the story that you possibly can.
    You should focus on the elements of the feedback that have to do with the {focus}.
    This means: {focus_explanation}

    CRITICAL INSTRUCTIONS:
    - ONLY address elements of feedback related to {focus}.
    - Only respond with the story - no other text
    - Keep the story to fewer than 500 words

    FEEDBACK: {feedback}
    STORY: {story}
    """


agent_foci = [
    "plot",
    "theme",
    "character",
    "world building",
    "writing precision and elegance",
    "finishing touches and consistency",
]

# explain what it is to be good at focusing on each focus
focus_explanations = [
    """- Ensuring there's an overarching story 
    - Having one or more interesting plot twists (depending on story length) 
    - Plot seeding 
    - Having both larger scope development and intimate character moments
    """,
    """- Explore 1 or more core philosophical questions (depending on story length)
    - Comment on present-day issues through future/alternate contexts, but don't make this over the top 
    - Including ethical dilemmas unique to the technological/scientific premises
    - Exploring what it means to be human/sentient
    - Challenging some notions of what we take for granted 
    """,
    """- Have character growth
    - Have realistic relationship dynamics 
    - Interesting characters
    - Mostly psychologically consistent (but inconsistent in human ways)
    - Have a variety of types of characters with different motivations and interests
    - Have characters with moments that are surprising but believable 
    """,
    """
    - Reveal worldbuilding naturally through plot and characters - not through exposition
    - Create cultural depth that comes through naturally
    - Have consequences to the systems that are set up 
    - Consider technology impacts society and individuals beyond the surface level
    - Ensure internal consistency of scientific/technological rules
    - Explore unintended consequences
    """,
    """- Efficient sentences 
    - Grounding reader in senses and physical details 
    - Not being overly flowery or descriptive
    - Well crafted sentences
    - Efficient overall — don't say in 2 paragraphs what you can say in 1 sentence
    """,
    """- Voice consistency for the narrator/background descriptions
    - Voice consistency within each character
    - Plot coherence 
    - Character coherence 
    - Ensuring things aren't too direct or explaining too much
    - Ensuring language isn't too flowery or verbose
    - Allow meaning to emerge rather than being overly direct with the reader
    """,
]

drafts = [test_story]
with open("story_feedback.pkl", "rb") as f:
    feedback_list = pickle.load(f)

for agent_focus, explanation in zip(agent_foci, focus_explanations):
    new_draft = rewrite_story(
        agent_focus, explanation, feedback=feedback_list, story=test_story
    )
    drafts.append(new_draft)

with open("story_drafts.pkl", "wb") as f:
    pickle.dump(drafts, f)
