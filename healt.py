import customtkinter
import google.generativeai as genai


class ChatBotGui(customtkinter.CTk):
    customtkinter.set_appearance_mode("white")
    customtkinter.set_default_color_theme("blue")
    chat_started = False

    def __init__(self):
        super().__init__()

        my_width = self.winfo_screenwidth()
        my_height = self.winfo_screenheight()

        self.title("Health Chatbot")
        self.geometry(f"{my_width}x{my_height}")

        self.Chat_label = customtkinter.CTkLabel(
            self,
            text="Medi.py - Your Health Assistant",
            text_color="black",
            font=("Arial", 30),
        )
        self.Chat_label.place(relx=0.25, rely=0.03)

        self.Show_Message_Box = customtkinter.CTkTextbox(
            self,
            fg_color='light blue',
            text_color="black",
            font=("Arial", 20),
            corner_radius=25,
            border_width=2,
            border_color='black'
        )
        self.Show_Message_Box.insert("1.0", "Hello, How are you feeling today?")
        self.Show_Message_Box.place(relheight=0.6, relwidth=0.66, relx=0.17, rely=0.1)

        self.Message_Box = customtkinter.CTkEntry(
            self,
            fg_color='white',
            text_color="black",
            corner_radius=25,
            font=("Arial", 20),
            border_color="black",
            border_width=2,
            placeholder_text="Type your message here"
        )
        self.Message_Box.place(relx=0.17, rely=0.75, relheight=0.08, relwidth=0.66)

        self.Send_Button = customtkinter.CTkButton(
            self,
            text="Send",
            fg_color='blue',
            text_color='white',
            font=("Arial", 20),
            corner_radius=25,
            command=self.Send_message
        )
        self.Send_Button.place(relx=0.84, rely=0.75, relheight=0.08, relwidth=0.1)

        self.mainloop()

    def Send_message(self):
        message = self.Message_Box.get()
        self.Message_Box.delete(0, customtkinter.END)

        if not self.chat_started:
            self.Show_Message_Box.delete("1.0", customtkinter.END)

        self.Show_Message_Box.insert(customtkinter.END, f"\nUser: {message}\n")
        self.chat_started = True
        response, accuracy = self.get_res(message)
        self.Show_Message_Box.insert(customtkinter.END, f"Bot: {response}\nAccuracy: {accuracy}\n")

    def get_res(self, user_input):
        key = "AIzaSyDdyDb0WR7cJBwT6Zj4Kbu9mV_f80Fy-zA"
        genai.configure(api_key=key)

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])

        extra = """You are a health specialist AI.
        Provide your answer in the user's language.
        Give short answers only for diagnosis or remedies.
        Don't say things like 'Got it' or 'Okay', just give the answer."""

        response = chat_session.send_message(user_input + " " + extra)
        verify_percent = chat_session.send_message("verify data if it's correct: " + response.text)

        return response.text, verify_percent.text


def main():
    ChatBotGui()


main()
