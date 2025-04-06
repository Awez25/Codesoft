import re 
import random

class chatBot:
    negative_responses = ('no', 'nope', 'nah', 'not', 'never', 'not at all', 'not a chance', 'sorry')
    exit_commands = ('quit', 'exit', 'bye', 'goodbye', 'later', 'see you', 'farewell')
    random_questions = (
        'What is your favorite hobby?', 
        'Which book are you reading these days?', 
        'Do you enjoy traveling? Where did you last go?',
        'What’s your favorite movie or TV show?',
        'Do you have any pets?',
        'What kind of music do you like?'
    )

    def __init__(self):
        self.intents = {
            'introductory': r'.*(purpose|what.*do.*you.*do|why.*you.*here).*',
            'answer_why_intent': r'why\sare.*|why.*you.*exist.*',
            'about_chatbot': r'.*(chatbot|who.*are.*you).*',
            'thanks': r'(thanks|thank you|appreciate|thx)'
        }

    def greet(self):
        self.name = input("What's your name?\n").strip()
        if not self.name:
            self.name = "friend"
        
        will_help = input(f"Hi {self.name}, I'm chatBot. Would you like to chat with me? (yes/no)\n").strip().lower()
        if will_help in self.negative_responses:
            print("Okay, maybe another time. Have a great day!")
            return
        self.chat()

    def make_exit(self, reply):
        return any(command in reply.lower() for command in self.exit_commands)

    def chat(self):
        print("Let's chat! You can say 'quit' anytime to leave.\n")
        while True:
            reply = input(random.choice(self.random_questions) + "\n> ").strip().lower()
            if self.make_exit(reply):
                print(f"Goodbye {self.name}! It was nice talking to you.")
                break
            response = self.match_reply(reply)
            print(response)

    def match_reply(self, reply):
        for intent, pattern in self.intents.items():
            if re.search(pattern, reply, re.IGNORECASE):
                return getattr(self, intent)()
        return self.no_match_intent()

    def introductory(self):
        responses = (
            "I'm here to have interesting conversations with you!",
            "My purpose is to chat and learn from humans like you.",
            "I was created to make small talk more enjoyable."
        )
        return random.choice(responses)

    def answer_why_intent(self):
        responses = (
            "I exist to understand human conversations better.",
            "Curiosity about people brought me here!",
            "I want to learn what makes humans interesting."
        )
        return random.choice(responses)

    def about_chatbot(self):
        responses = (
            "I'm a simple chatbot who loves conversations!",
            "Just a friendly AI trying to have nice chats.",
            "I'm chatBot, your conversational partner."
        )
        return random.choice(responses)

    def thanks(self):
        responses = (
            "You're welcome! 😊",
            "Happy to chat!",
            "Anytime! What else would you like to talk about?"
        )
        return random.choice(responses)

    def no_match_intent(self):
        responses = (
            "That's interesting! Tell me more.",
            "I see. What else do you enjoy?",
            "Why do you say that?",
            "Can you elaborate on that thought?",
            "Fascinating! Could you explain more?"
        )
        return random.choice(responses)

if __name__ == "__main__":
    bot = chatBot()
    bot.greet()