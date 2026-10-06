# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  Overall, the UI looked convincing, but playing the game you could tell something is wrong. 
  1. The hints were not always correct. I would guess below or above the correct answer and it would tell me to go the opposite way. For example, if the number was 11 and I guessed 10, it told me to guess lower. I think this involves the check_guess function in app.py, specifically lines 38, 40, 44, and 46.
  2. I was able to guess outside of the 1-100 range, for example, 0 or 101. I think this should be a bug as players should be limited to the guessing range. The error could either be in parse_guess() or check_guess() function in app.py
  3. The game doesn't let me play again. I was expecting to hit the new game button and be able to submit a new first guess after finishing a game, but nothing happens when I hit the submit button after a game has ended and I hit the new game button. I think this could come from the st.stop() in line 145 in app.py, but I'm not sure.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|-------|-------------------|-----------------|------------------------|-------------------------|
| Guess 10 when answer is 11 | "Guess Higher" hint | "Guess lower" hint shown| none | check_guess() in app.py |
| Guess 0 when range is 1-100| Answer out of range, try again | Goes through and gets "Guess lower" hint| none | could either be in parse_guess() or check_guess() functions in app.py|
| New game and submit guess button | Starts new game with hints | Nothing happens | None | Line 145 in app.py |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude Code for this project. 

An example of an AI suggestion that was correct was that the high/low bug was caused by the hint messages being swapped, so to switch that around to make it work. After switching it, I verified the result by running the app and seeing what message it now output.

An example of an AI suggestion that wasn't completely correct (at least for my best guess) was for the scoring. The AI wanted to make the maximum score 90 when fixing the scoring system, but from the previous code, it seemed like the maximum score should be 100. I updated the AI's directions to implement this and tested it by correctly guessing the number on the first try and verifying that the score was 100. Also used new tests in test_game_logic.py to ensure the logic worked correctly.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided whether a bug was really fixed by using test functions as well as by playing the game and observing the behavior. I used pytests to determine if the hints were working correctly. At first, they were not, but after fixing the bug the tests passed (it correctly told the user to guess higher or guess lower). AI helped me write all the tests and think of edge scenarios to test on.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit "reruns" are when streamlit literally reruns all the code for a page whenever a widget is interacted with. Session state is how streamlit saves the data in the widgets over multiple reruns. It stores it so it can be used by the reruns later on.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

I want to get in the habit of making smaller commits when using git and not saving it all for the end. This makes it easier to track changes and to save more work if you mess something up.
One thing I would do differently next time I work with AI is to take an even closer look at what all the agent is changing, as it can be tempting to walk away and let it do all the work.
This project changed the way I think about AI generated code because it showed me that it only knows so much, and it needs my direction to help it out sometimes. Without direction, it can make up its own rules for your application, which could be a bug in the best of cases, and a security vulnerability in worse cases.