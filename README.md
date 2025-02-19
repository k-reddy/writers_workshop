# Writers' Workshop

## About
The writers' workshop is a tool to have fun with LLMs, spice up your creative process, and be "in conversation with" great writers in a new way. It's a pun on the idea of a workshop and has two parts:
- Writers' Workshop: an MFA-style writers' workshop, where users can have their writing critiqued by their favorite authors
- Draft Writing: Users input a story draft and feedback on how that draft could be better, and this system outputs a new draft. Think assembly-line workshop, but where each worker is a specialized writer that focuses on a specific part of the story.

At the moment, you run each of these as separate scripts in the terminal (feedback.py and writing.py, respectively). The long-term goal is to have this available on a website with a pretty front-end.

## Architecture & Challenges: Writers' Workshop
I'm going with a very straightforward API call to get feedback from LLMs cosplaying as famous writers, as there should be enough writing and critical review of any major writer in the LLM training data for the LLM to simulate that writer.

The main issue I'm troubleshooting currently is that for some reason the LLM tends to provide *very* similar feedback from each writer, even though it's prompted to give feedback according to the special skills and interests of each specified writer. I'm tackling this with prompt engineering.

## Architecture & Challenges: Draft Workshop
Editing a story is a complex task that requires you to focus on many things at once (e.g. plot, themes, character psychology, world building, stylistic consistency, writing precision, sentence-level elegance, etc.). LLMs tend to do best if such complexity is broken down so that each LLM can have one job and all those LLM agents can work together to create a final output. 

Currently, I have 6 different agents, each with their own focus and an in-depth explanation of what it means to have that focus. For example, one agent focuses on plot, which I explain as:
- Ensuring there's an overarching story 
- Having one or more interesting plot twists (depending on story length) 
- Plot seeding 
- Having both larger scope development and intimate character moments

The system iterates through each agent, feeding it the current story draft and the feedback and receiving a new story draft (which it then passes to the next agent, and so on). This way, the agents work iteratively, and the system returns the final story to the user. 

The main challenge with this portion of the workshop is that the writing is bad! Claude tends to be a very flowery writer and, despite my strong prompting, changes the style of the writing a good amount. I'm hoping to resolve this with different agents or agent ordering or different prompting. If that fails, I will explore fine tuning.