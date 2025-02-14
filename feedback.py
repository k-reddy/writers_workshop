import anthropic
import os
import pickle

# grab the API key
with open(os.path.expanduser("~/Documents/developer_creds/anthropic_key.txt")) as f:
    api_key = f.read().strip()

# set up the client
client = anthropic.Anthropic(
    api_key=api_key,
)

# test_story = """Jean walked into the sterile, white-walled chamber, her footsteps echoing against gleaming surfaces. Rows of scanning equipment lined the walls, their sensors tracking her every movement. A full-wall screen flickered to life, displaying auction details for rental unit AA005.\n\n"Welcome to the auction," a mechanical voice announced. "Please use hologram forms. Transparency is mandatory."\n\nTranslucent figures began materializing around her - some tall and angular, others compact and rigid. Each hologram represented a potential buyer, their forms shifting with barely contained excitement.\n\nA holographic broker stepped forward. "Unit AA005 represents a unique acquisition. Partially restored human stock, minimal genetic drift, prime reproductive potential."\n\nJean felt a chill run down her spine. The holograms pressed closer, their transparent bodies overlapping, voices rising in a cacophony of bids and technical assessments.\n\n"Genetic stability at 87.3%!"\n"Neurological mapping indicates high adaptability!"\n"Bidding opens at 500,000 credit units!"\n\nHer own emotions felt distant, compartmentalized. Was this apathy or a survival mechanism? Years of processing through these auctions had worn down her emotional responses.\n\nThe bidding intensified. Holograms pushed and intersected, their digital representations becoming more aggressive. Jean remained still, a living commodity being evaluated by algorithmic buyers.\n\nOne hologram, more solid than the others, stepped directly in front of her. Its form suggested corporate ownership - sharp lines, precise movements.\n\n"Preliminary assessment complete," it announced. "Genetic profile acceptable. Neurological potential: exceptional."\n\nJean\'s heart rate remained steady. She had been through this process before. She would go through it again.\n\nThe final bid approached. Credits would transfer. A new owner would be selected.\n\nShe waited, perfectly still."""


def generate_feedback(story, writer):
    # send a request and get a message back
    message = client.messages.create(
        # model="claude-3-5-haiku-latest",
        model="claude-3-5-sonnet-latest",
        max_tokens=1024,
        system="You are leading a writers' workshop at a top MFA program. Your goal is to take your knowledge of your craft and make your students the best writers they can be.",
        messages=[{"role": "user", "content": generate_message_prompt(story, writer)}],
    )
    print(f"----feedback from {writer}----")
    print(message.content[0].text)
    return message.content[0].text


def generate_message_prompt(story, writer):
    return f"""
    You are going to get a story from one of your students.
    You should read it and write 1 paragraph of feedback for your student.
    Make sure you're giving the feedback as though you are {writer}. 
    Consider {writer}'s strengths. 
    Of all the domains you could possibly give feedback on (plot, writing economy and elegance, character development and psychological depth, themes, world building, consistency, etc.), what does {writer} focus on most?
    What do they tend to lean into stylistically? Give feedback according to that. 
    Make sure the tone, style, and content of your feedback are consistent with {writer}'s writing.
    The feedback should clearly explain:
    - What's working well
    - What to do more of
    - What to do differently

    Use specific examples and explain very clearly what could be better.

    CRITICAL INSTRUCTIONS:
    - Only respond with feedback, no filler text
    - Do not rewrite any of the story - you want to guide your student, not write for them
    - Don't be too verbose. Focus your feedback concise and to the point so it's easy to act on.
    - Don't make reference to your own work or process. Just let it inform the feedback and aspects of the story you choose to focus on.
    STORY: {story}
    """


with open("story_drafts.pkl", "rb") as f:
    story_drafts = pickle.load(f)

latest_draft = story_drafts[-1]

feedback = []
for chosen_writer in ["Jamaica Kincaid", "Amy Hempel", "Teju Cole"]:
    feedback.append(generate_feedback(latest_draft, chosen_writer))

with open("story_feedback.pkl", "wb") as f:
    pickle.dump(feedback, f)
